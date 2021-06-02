import sys
import ply.lex as lex
import ply.yacc as yacc

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

    # Delimiters (( ) [ ] , .)
    'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS', 'LEFT_BRACKET', 'RIGHT_BRACKET', 'COMMA', 'PERIOD',

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
t_LEFT_BRACKET = r'\['
t_RIGHT_BRACKET = r'\]'
t_COMMA = r'\,'
t_PERIOD = r'\.'

# Simple REs
RE_Number = r'\d+'
RE_Newline = r'\n+'

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


# Error handling rule
def t_error(t):
    print("Caracter ilegal '%s" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

example_1 = """SELECT eci.nro_contrato, oa.zona, oa.subzona, oa.nro_org, 
eci.nro_prod, ia.razon_social, oa.correo_electronico, eci.fecha_abm 
FROM EMIS_Contrato_Intermediarios AS eci INNER JOIN Organizadores_Aux AS oa ON 
eci.nro_empsoc = oa.nro_empsoc AND eci.nro_org = oa.nro_org 
WHERE eci.nro_org =244 ORDER BY eci.fecha_abm DESC"""

example_2 = """ SELECT nro FROM Tabla AS T"""

example_3 = '''SELECT c.first_name, c.last_name
FROM customers AS c'''

example_4 = '''SELECT c.first_name, c.last_name
FROM customers AS c
WHERE c.id = 2'''

example_5 = '''SELECT DISTINCT c.first_name, c.last_name, p.number
FROM customers AS c
LEFT JOIN phones_numbers AS p ON
c.id = p.customer_id
WHERE [c.first_name = 'hola que tal 123']
AND (p.number = 123)
'''

lexer.input(example_5)

while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)

# dictionary of tables
tables = {}


def p_select(p):
    """query : SELECT column_names FROM tables_name"""
    tables[p[2]]  # """nombre de la tabla - VER BIEN"""


def p_select_where(p):
    """query : SELECT column_names FROM tables_name WHERE conditions"""
    tables[p[2]]


def p_select_where_in(p):
    """query : SELECT column_names FROM tables_name WHERE conditions IN (SELECT column_names FROM tables_name WHERE
    condition) """
    tables[p[2]]


def p_select_where_orderby(p):
    """query : SELECT column_names FROM tables_name WHERE conditions ORDER BY condition"""
    tables[p[2]]


def p_select_where_orderby_desc(p):
    """query : SELECT column_names FROM tables_name WHERE conditions ORDER BY condition DESC"""
    tables[p[2]]


def p_select_where_orderby_asc(p):
    """query : SELECT column_names FROM tables_name WHERE conditions ORDER BY condition ASC"""
    tables[p[2]]


def p_select_where_groupby_orderby_(p):
    """query : SELECT column_names FROM tables_name WHERE conditions GROUP BY column_names ORDER BY condition"""
    tables[p[2]]


def p_select_where_groupby_having_orderby_(p):
    """query : SELECT column_names FROM tables_name WHERE conditions GROUP BY column_names HAVING condition ORDER BY
    condition """
    tables[p[2]]


def p_select_innerjoin_where(p):
    """query : SELECT column_names FROM tables_name INNER JOIN tables_name WHERE conditions"""
    tables[p[2]]


def p_select_innerjoin_on_where(p):
    """query : SELECT column_names FROM tables_name INNER JOIN tables_name ON conditions WHERE conditions"""
    tables[p[2]]


def p_select_leftjoin_where(p):
    """query : SELECT column_names FROM tables_name LEFT JOIN tables_name WHERE conditions"""
    tables[p[2]]


def p_select_leftjoin_on_where(p):
    """query : SELECT column_names FROM tables_name LEFT JOIN tables_name ON conditions WHERE conditions"""
    tables[p[2]]


def p_select_rightjoin_where(p):
    """query : SELECT column_names FROM tables_name RIGHT JOIN tables_name WHERE conditions"""
    tables[p[2]]


def p_select_rightjoin_on_where(p):
    """query : SELECT column_names FROM tables_name RIGHT JOIN tables_name ON conditions WHERE conditions"""
    tables[p[2]]


def p_empty(p):
    """empty :"""
    pass


# Grammar
"""
Axiom : SELECT NT_Columns FROM NT_Tables NT_WHERE

NT_Columns : COLUMN_NAME NT_Auxiliary_Column 

NT_Auxiliary_Column : empty
                    | t_PERIOD COLUMN_NAME NT_Auxiliary_Column

NT_Tables : TABLE_NAME NT_Auxiliary_Table

NT_Auxiliary_Table : empty
                   | t_PERIOD TABLE_NAME NT_Auxiliary_Table
                   | AS TABLE_NAME NT_FIX_MULTIPLE_CONSECUTIVE_AS_PROBLEM

NT_FIX_MULTIPLE_CONSECUTIVE_AS_PROBLEM : empty
                                       | t_PERIOD TABLE_NAME NT_Auxiliary_Table

NT_WHERE : empty
         | ORDER_BY T_Condition_ORDER_BY
         | T_Condition_WHERE NT_Auxiliary_WHERE

NT_Auxiliary_WHERE : empty
                   | ORDER_BY T_Condition_ORDER_BY
                   | GROUP_BY T_Condition_GROUP_BY NT_Auxiliary_GROUP_BY

NT_Auxiliary_GROUP_BY : empty
                      | ORDER_BY T_Condition_ORDER_BY
                      | Having T_Condition_Having NT_Auxiliary_Having

NT_Auxiliary_Having : empty
                    | ORDER_BY T_Condition_ORDER_BY

ORDER_BY : ORDER BY

GROUP_BY : GROUP BY

INNER_JOIN : INNER JOIN

LEFT_JOIN : LEFT JOIN
"""
# Note 1: NT means "No Terminal", T means "Terminal", empty means "Lambda"
# Note 2: No need for NT_SELECT and NT_FROM because they must exist no matter what for the SQL query to work
