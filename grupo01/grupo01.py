import sys
import ply.lex as lex
import ply.yacc as yacc

class SelectState:
    def __init__(self, input = None):
        self.parsing = input
        self.parsed_tables = dict()

    def add_table(self, table):
        parsed = self.parsed_tables.get(table)

        if not parsed:
            self.parsed_tables[table] = []

    def add_column(self, table, column):
        self.add_table(table)
        table_columns = self.parsed_tables[table]
        if column not in table_columns:
            table_columns.append(column)
    
    def get_report(self):
        return self.parsed_tables

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
t_PERIOD = r'\.'

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
def get_column(parsing, pos = 0):
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
# Note 1: NT means "No Terminal", empty means "Lambda"
# Note 2: No need for NT_SELECT and NT_FROM because they must exist no matter what for the SQL query to work

# Error handling rule
def p_error(p):
    if not p:
        raise EOFError("Unexpected EOF")
    
    val, line, column = get_info(p)

    raise SyntaxError(f"Sintax Error '{ val }' at ({line}, {column})")

def parse_tuple(p, reduce = False):
    result = tuple(p[1:])

    if len(result) == 1:
        value = result[0]

        if value is None:
            return value
        
        if reduce and type(value) is tuple:
            return value

    return result

def p_axiom_select(p):
    '''
    Axiom : SELECT NT_AUX_SELECT NT_Columns FROM NT_Tables NT_SELECT_OPTIONAL
    '''
    p[0] = parse_tuple(p)

def p_nt_aux_select(p):
    '''
    NT_AUX_SELECT : empty
                  | DISTINCT
    '''
    p[0] = parse_tuple(p)

def p_nt_select_optional(p):
    '''
    NT_SELECT_OPTIONAL : empty
                       | NT_WHERE
                       | NT_WHERE ORDER_BY
                       | NT_WHERE GROUP_BY
                       | ORDER_BY
                       | ORDER_BY GROUP_BY
                       | GROUP_BY
                       | NT_WHERE ORDER_BY GROUP_BY
    '''
    p[0] = parse_tuple(p)

def p_nt_column(p):
    '''
    NT_COLUMN : TABLE_NAME PERIOD COLUMN_NAME
              | COLUMN_NAME
              | STRING
              | NUMBER
    '''
    p[0] = parse_tuple(p)

def p_nt_columns(p):
    '''
    NT_Columns : NT_COLUMN
               | NT_FUNCTION LEFT_PARENTHESIS NT_COLUMN RIGHT_PARENTHESIS
               | NT_Columns COMMA NT_Columns
    '''
    p[0] = parse_tuple(p, reduce = True)

def p_nt_function(p):
    '''
    NT_FUNCTION : COUNT
                | MAX
                | MIN
    '''
    p[0] = parse_tuple(p)

def p_nt_tables(p):
    '''
    NT_Tables : TABLE_NAME NT_Auxiliary_Table
              | TABLE_NAME NT_Auxiliary_Table NT_JOINS
              | TABLE_NAME NT_Auxiliary_Table COMMA NT_Tables
    '''
    p[0] = parse_tuple(p)

def p_nt_auxiliary_table(p):
    '''
    NT_Auxiliary_Table : empty
                       | AS TABLE_NAME
                       | TABLE_NAME
    '''
    p[0] = parse_tuple(p)

def p_nt_where(p):
    '''
    NT_WHERE : WHERE NT_Conditions
    '''
    p[0] = parse_tuple(p)

def p_nt_condition(p):
    '''
    NT_Condition : NT_COLUMN EQUAL_TO NT_COLUMN
                 | NT_COLUMN GREATER_THAN NT_COLUMN
                 | NT_COLUMN LESS_THAN NT_COLUMN
                 | NT_COLUMN GREATER_THAN_OR_EQUAL_TO NT_COLUMN
                 | NT_COLUMN LESS_THAN_OR_EQUAL_TO NT_COLUMN
                 | NT_COLUMN NOT_EQUAL_TO NT_COLUMN
                 | NT_COLUMN AND NT_COLUMN
                 | NT_COLUMN OR NT_COLUMN
                 | NT_COLUMN IN LEFT_PARENTHESIS Axiom RIGHT_PARENTHESIS
    '''
    p[0] = parse_tuple(p)

def p_nt_conditions(p):
    '''
    NT_Conditions : NT_Condition NT_AUX_Conditions
                  | LEFT_PARENTHESIS NT_Condition RIGHT_PARENTHESIS NT_AUX_Conditions
                  | LEFT_PARENTHESIS NT_Condition NT_AUX_Conditions RIGHT_PARENTHESIS
    '''
    p[0] = parse_tuple(p)

def p_nt_aux_conditions(p):
    '''
    NT_AUX_Conditions : empty
                      | AND NT_Conditions
                      | OR NT_Conditions
    '''
    p[0] = parse_tuple(p)

def p_order_by(p):
    '''
    ORDER_BY : ORDER BY NT_AUX_ORDER_BY
    '''
    p[0] = parse_tuple(p)

def p_nt_aux_order_by(p):
    '''
    NT_AUX_ORDER_BY : NT_COLUMN
                    | NT_COLUMN ASC
                    | NT_COLUMN DESC
                    | NT_COLUMN COMMA NT_AUX_ORDER_BY
    '''
    p[0] = parse_tuple(p)

def p_group_by(p):
    '''
    GROUP_BY : GROUP BY NT_Columns AUX_HAVING
    '''
    p[0] = parse_tuple(p)

def p_aux_having(p):
    '''
    AUX_HAVING : empty
               | HAVING NT_Conditions
    '''
    p[0] = parse_tuple(p)

def p_nt_join(p):
    '''
    NT_JOIN : JOIN TABLE_NAME NT_Auxiliary_Table ON NT_Conditions
    '''
    p[0] = parse_tuple(p)

def p_nt_joins(p):
    '''
    NT_JOINS : empty
             | NT_JOIN NT_JOINS
             | INNER NT_JOIN NT_JOINS
             | LEFT NT_JOIN NT_JOINS
    '''
    p[0] = parse_tuple(p)

def p_empty(p):
    """empty :"""
    pass

lexer  = lex.lex()
parser = yacc.yacc()

def build_select_report(parsed_result):
    pass

def parse_select_statement(select_input, debug = False):
    lexer.lineno = 1

    parser_state = SelectState(select_input)
    lexer.select_state  = parser_state
    parser.select_state = parser_state

    parsed = parser.parse(select_input)

    if debug:
        print('DEBUG PARSER:', parsed)

    return build_select_report(parsed)
