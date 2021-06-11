import ply.lex as lex
import ply.yacc as yacc
import re


class SelectState:
    def __init__(self, input=None):
        self.parsing = input


class Table:
    def __init__(self, name, alias=None):
        self.name = name
        self.alias = alias

    def is_name(self, value):
        return self.name == value or self.alias == value

    def __repr__(self):
        if not self.alias:
            return f'Table({self.name})'
        else:
            return f'Table({self.name} \'{self.alias}\')'


class Column:
    def __init__(self, table, name):
        self.table = table
        self.name = name

    def __repr__(self):
        return f'Column({self.table}->{self.name})'


reserved = {
    'AS': 'AS',
    'ASC': 'ASC',
    'BY': 'BY',
    'COUNT': 'COUNT',
    'DESC': 'DESC',
    'DISTINCT': 'DISTINCT',
    'FROM': 'FROM',
    'GROUP': 'GROUP',
    'HAVING': 'HAVING',
    'INNER': 'INNER',
    'JOIN': 'JOIN',
    'LEFT': 'LEFT',
    'MAX': 'MAX',
    'MIN': 'MIN',
    'ON': 'ON',
    'IN': 'IN',
    'ORDER': 'ORDER',
    'SELECT': 'SELECT',
    'WHERE': 'WHERE',

    # Logical Operators (AND, OR)
    'AND': 'AND',
    'OR': 'OR',
}

tokens = list(reserved.values()) + [
    # Comparison Operators (=, >, <, >=, <=, <>)
    'EQUAL_TO', 'GREATER_THAN', 'LESS_THAN', 'GREATER_THAN_OR_EQUAL_TO', 'LESS_THAN_OR_EQUAL_TO', 'NOT_EQUAL_TO',

    # Delimiters (( ) , .)
    'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS', 'COMMA', 'PERIOD',

    # Other data (name of the table, name of the column, ID for reserved words lookup)
    'TABLE_NAME', 'COLUMN_NAME', 'STRING', 'NUMBER'
]

# Definitions of Regular Expressions

# Operators
t_EQUAL_TO = r'\='
t_GREATER_THAN = r'\>'
t_LESS_THAN = r'\<'
t_GREATER_THAN_OR_EQUAL_TO = r'\>='
t_LESS_THAN_OR_EQUAL_TO = r'\<='
t_NOT_EQUAL_TO = r'\<>'

# Delimiters
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_COMMA = r'\,'
COMMA_CHAR = ','
t_PERIOD = r'\.'
PERIOD_CHAR = '.'

# Simple REs
RE_Number = r'\d+'
RE_Newline = r'\n+'
NEW_LINE_CHAR = '\n'

# Complex REs
RE_String = r'\'[a-zA-Z_0-9_ ]*\''
RE_Table = r'[a-zA-Z][\_a-zA-Z0-9]*'
RE_Column = RE_Table + t_PERIOD + RE_Table


@lex.TOKEN(RE_String)
def t_STRING(t):
    t.type = reserved.get(t.value, 'STRING')  # Check for reserved words
    return t


@lex.TOKEN(RE_Column)
def t_COLUMN_NAME(t):
    t.type = reserved.get(t.value, 'COLUMN_NAME')  # Check for reserved words
    return t


@lex.TOKEN(RE_Table)
def t_TABLE_NAME(t):
    t.type = reserved.get(t.value, 'TABLE_NAME')  # Check for reserved words
    return t


@lex.TOKEN(RE_Number)
def t_NUMBER(t):
    t.value = int(t.value)
    return t


# Ignore newline
@lex.TOKEN(RE_Newline)
def t_newline(t):
    t.lexer.lineno += len(t.value)


# Ignore whitespace
t_ignore = ' \t'


# Get column for parsed token
def get_column(parsing, pos=0):
    start = parsing.rfind(NEW_LINE_CHAR, 0, pos) + 1

    if start < 0:
        start = 0

    offset = pos - start

    return 1 if offset == 0 else offset


def get_info(token):
    val = token.value
    line = token.lineno
    column = get_column(token.lexer.select_state.parsing, token.lexpos)
    return val, line, column


# Error handling rule
def t_error(token):
    if not token:
        raise EOFError("Unexpected EOF")

    char, line, column = get_info(token)

    raise Exception(f"Ilegal character '{char[0]}' at ({line}, {column})")


# YACC & GRAMMAR

def p_axiom(p):
    """
    Axiom : NT_Select NT_From
    """
    p[0] = parse_tuple(p)


def p_nt_select(p):
    """
    NT_Select : SELECT NT_Columns_Select
              | SELECT DISTINCT NT_Columns_Select
    """
    p[0] = parse_tuple(p)


def p_nt_columns_select(p):
    """
    NT_Columns_Select : COLUMN_NAME
                      | COLUMN_NAME COMMA NT_Columns_Select
                      | NT_Function LEFT_PARENTHESIS COLUMN_NAME RIGHT_PARENTHESIS
                      | NT_Function LEFT_PARENTHESIS COLUMN_NAME RIGHT_PARENTHESIS COMMA NT_Columns_Select

    """
    p[0] = parse_columns(p)


def p_nt_function(p):
    """
    NT_Function : COUNT
                | MAX
                | MIN
    """
    p[0] = parse_tuple(p)


def p_nt_from(p):
    """
    NT_From : FROM NT_Tables
            | FROM NT_Tables NT_Select_Optional
    """
    p[0] = parse_tuple(p)


def p_nt_tables(p):
    """
    NT_Tables : TABLE_NAME
              | TABLE_NAME NT_Joins
              | TABLE_NAME COMMA NT_Tables
              | TABLE_NAME TABLE_NAME
              | TABLE_NAME TABLE_NAME NT_Joins
              | TABLE_NAME TABLE_NAME COMMA NT_Tables
              | TABLE_NAME AS TABLE_NAME
              | TABLE_NAME AS TABLE_NAME NT_Joins
              | TABLE_NAME AS TABLE_NAME COMMA NT_Tables
    """
    value = parse_tuple(p)
    pos_alias = 1
    name, alias = value[0], value[pos_alias]

    if alias=='AS':
        pos_alias = 2
        alias = value[pos_alias]
    
    if type(alias) is tuple or alias == COMMA_CHAR:
        pos_alias = 0
        alias = None

    if len(value) > 2:
        p[0] = (Table(name, alias), *value[pos_alias + 1:])
    else:
        p[0] = (Table(name, alias),)


def p_nt_joins(p):
    """
    NT_Joins : LEFT NT_Join
             | LEFT NT_Join NT_Joins
             | INNER NT_Join
             | INNER NT_Join NT_Joins
             | NT_Join NT_Joins
             | JOIN TABLE_NAME ON NT_Conditions
             | JOIN TABLE_NAME TABLE_NAME ON NT_Conditions
             | JOIN TABLE_NAME AS TABLE_NAME ON NT_Conditions
    """
    p[0] = parse_tuple(p)


def p_nt_join(p):
    """
    NT_Join : JOIN TABLE_NAME ON NT_Conditions
            | JOIN TABLE_NAME TABLE_NAME ON NT_Conditions
            | JOIN TABLE_NAME AS TABLE_NAME ON NT_Conditions
    """
    value = parse_tuple(p)

    pos_alias=2
    name, alias = value[1], value[pos_alias]

    if alias=='AS':
        pos_alias=3
        alias=value[pos_alias]

    if alias=='ON':
        pos_alias=1
        alias=None

    p[0] = (value[0], Table(name, alias), *value[pos_alias + 1:])



def p_nt_select_optional(p):
    """
    NT_Select_Optional : WHERE NT_Conditions
                       | WHERE NT_Conditions GROUP BY NT_Columns_Group_By
                       | WHERE NT_Conditions GROUP BY NT_Columns_Group_By HAVING NT_Conditions
                       | WHERE NT_Conditions GROUP BY NT_Columns_Group_By HAVING NT_Conditions ORDER BY NT_Aux_Order_By
                       | WHERE NT_Conditions GROUP BY NT_Columns_Group_By ORDER BY NT_Aux_Order_By
                       | WHERE NT_Conditions ORDER BY NT_Aux_Order_By
                       | GROUP BY NT_Columns_Group_By
                       | GROUP BY NT_Columns_Group_By HAVING NT_Conditions
                       | ORDER BY NT_Aux_Order_By
    """
    p[0] = parse_tuple(p)


def p_nt_columns_group_by(p):
    """
    NT_Columns_Group_By : COLUMN_NAME
                        | COLUMN_NAME COMMA NT_Columns_Group_By
    """
    p[0] = parse_columns(p)


def p_nt_aux_order_by(p):
    """
    NT_Aux_Order_By : COLUMN_NAME
                    | COLUMN_NAME  ASC
                    | COLUMN_NAME  DESC
                    | COLUMN_NAME COMMA NT_Aux_Order_By
                    | COLUMN_NAME  ASC COMMA NT_Aux_Order_By
                    | COLUMN_NAME  DESC COMMA NT_Aux_Order_By
                    | NT_Function LEFT_PARENTHESIS COLUMN_NAME RIGHT_PARENTHESIS
                    | NT_Function LEFT_PARENTHESIS COLUMN_NAME RIGHT_PARENTHESIS COMMA NT_Aux_Order_By
    """
    p[0] = parse_columns(p)


def p_nt_data_types(p):
    """
    NT_Data_Types : STRING
                  | NUMBER
                  | COLUMN_NAME
    """
    p[0] = parse_columns(p)

def p_nt_conditions(p):
    """
    NT_Conditions : COLUMN_NAME EQUAL_TO NT_Data_Types
                  | COLUMN_NAME NOT_EQUAL_TO NT_Data_Types
                  | COLUMN_NAME GREATER_THAN NT_Data_Types
                  | COLUMN_NAME LESS_THAN NT_Data_Types
                  | COLUMN_NAME GREATER_THAN_OR_EQUAL_TO NT_Data_Types
                  | COLUMN_NAME LESS_THAN_OR_EQUAL_TO NT_Data_Types
                  | LEFT_PARENTHESIS NT_Conditions RIGHT_PARENTHESIS
                  | COLUMN_NAME IN LEFT_PARENTHESIS Axiom RIGHT_PARENTHESIS
                  | COLUMN_NAME EQUAL_TO NT_Data_Types OR NT_Conditions
                  | COLUMN_NAME NOT_EQUAL_TO NT_Data_Types OR NT_Conditions
                  | COLUMN_NAME GREATER_THAN NT_Data_Types OR NT_Conditions
                  | COLUMN_NAME LESS_THAN NT_Data_Types OR NT_Conditions
                  | COLUMN_NAME GREATER_THAN_OR_EQUAL_TO NT_Data_Types OR NT_Conditions
                  | COLUMN_NAME LESS_THAN_OR_EQUAL_TO NT_Data_Types OR NT_Conditions
                  | LEFT_PARENTHESIS NT_Conditions RIGHT_PARENTHESIS OR NT_Conditions
                  | COLUMN_NAME IN LEFT_PARENTHESIS Axiom RIGHT_PARENTHESIS OR NT_Conditions
                  | COLUMN_NAME EQUAL_TO NT_Data_Types AND NT_Conditions
                  | COLUMN_NAME NOT_EQUAL_TO NT_Data_Types AND NT_Conditions
                  | COLUMN_NAME GREATER_THAN NT_Data_Types AND NT_Conditions
                  | COLUMN_NAME LESS_THAN NT_Data_Types AND NT_Conditions
                  | COLUMN_NAME GREATER_THAN_OR_EQUAL_TO NT_Data_Types AND NT_Conditions
                  | COLUMN_NAME LESS_THAN_OR_EQUAL_TO NT_Data_Types AND NT_Conditions
                  | LEFT_PARENTHESIS NT_Conditions RIGHT_PARENTHESIS AND NT_Conditions
                  | COLUMN_NAME IN LEFT_PARENTHESIS Axiom RIGHT_PARENTHESIS AND NT_Conditions
    """
    p[0] = parse_columns(p)


# Error handling rule
def p_error(p):
    if not p:
        raise EOFError("Unexpected EOF")

    val, line, column = get_info(p)

    raise SyntaxError(f"Syntax Error '{val}' at ({line}, {column})")


def parse_tuple(p, reduce=False):
    result = tuple(p[1:])

    if len(result) == 1:
        value = result[0]

        if value is None:
            result = value

        if reduce and type(value) is tuple:
            result = value

    return result

def is_column_token(token):
    return type(token) is str and re.match(RE_Column, token)

def parse_columns(p):
    value = parse_tuple(p)

    return tuple(
        Column(*(token.split(PERIOD_CHAR))) if is_column_token(token) else token 
        for token in value if type(value) is tuple
    )

def reduced(objects):
    result = []

    try:
        for element in objects:
            if type(element) is list:
                result = [*result, *reduced(element)]
            else:
                result.append(element)
    except TypeError:
        return objects

    return result


def filter_select_report(parsed_result):
    result = reduced(
        [
            reduced(filter_select_report(obj)) if type(obj) is tuple else obj

            for obj in parsed_result
            if type(obj) is Table
            or type(obj) is Column
            or type(obj) is tuple
        ])

    tables = [table for table in result if type(table) is Table]
    columns = [table for table in result if type(table) is Column]

    return tables, columns


def build_select_report(tables, columns):
    report = dict()

    for column in columns:
        try:
            table = next(filter(lambda table: table.is_name(column.table), tables))

            if table.name not in report:
                report[table.name] = []

            table_columns = report[table.name]

            if column.name not in table_columns:
                table_columns.append(column.name)

        except StopIteration:
            raise Exception(f"table '{column.table}' of '{column.table}.{column.name}' must be on FROM clause")

    for table in report:
        report[table].sort()

    return report


lexer = lex.lex()
parser = yacc.yacc()


def parse_select_statement(select_input, debug=False):
    lexer.lineno = 1

    parser_state = SelectState(select_input)
    lexer.select_state = parser_state
    parser.select_state = parser_state

    parsed = parser.parse(select_input)

    if debug:
        print('DEBUG PARSER:', parsed)

    return build_select_report(*filter_select_report(parsed))
