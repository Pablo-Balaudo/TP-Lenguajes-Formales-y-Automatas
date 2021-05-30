import sys
import ply.lex as lex
import ply.yacc as yacc

reserved = {
    'AS': 'AS',
    'ASC': 'ASC',
    'BETWEEN': 'BETWEEN',
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
    'RIGHT': 'RIGHT',
    'SELECT': 'SELECT',
    'WHERE': 'WHERE',
    r'[a-zA-Z][\_a-zA-Z0-9]*':'TABLE_NAME',


    # Logical Operators (AND, OR)
    'AND': 'AND',
    'OR': 'OR',
}

tokens = list(reserved.values()) + [
    # Comparison Operators (=, >, <, >=, <=, <>)
    'EQUAL_TO', 'GREATER_THAN', 'LESS_THAN', 'GREATER_THAN_OR_EQUAL_TO', 'LESS_THAN_OR_EQUAL_TO', 'NOT_EQUAL_TO',

    # DELIMITADORES (( ) [ ] , .)
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COMMA', 'PERIOD',

    # Other data (name of the table, name of the column, ID for reserved words lookup)
     'COLUMN_NAME', 'STRING', 'NUMBER'
]

t_EQUAL_TO = r'\='
t_GREATER_THAN = r'\>'
t_LESS_THAN = r'\<'
t_GREATER_THAN_OR_EQUAL_TO = r'\>='
t_LESS_THAN_OR_EQUAL_TO = r'\<='
t_NOT_EQUAL_TO = r'\<>'

# delimitadores
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r'\,'
t_PERIOD = r'\.'


STRING = r'\'' + r'[a-zA-Z_0-9_ ]*' + r'\''
##COLUMNNAME= r'[a-zA-Z][\_a-zA-Z0-9]*' + r'\.' + r'[a-zA-Z][\_a-zA-Z0-9]*'


@lex.TOKEN(STRING)

def t_STRING(t):
    t.type = reserved.get(t.value, 'STRING')    # Check for reserved words
    return t

##@lex.TOKEN(COLUMNNAME)
def t_COLUMN_NAME(t):
    r"""[a-zA-Z][\_a-zA-Z0-9]*\.[a-zA-Z][\_a-zA-Z0-9]*"""
    t.type = reserved.get(t.value, 'COLUMN_NAME')    # Check for reserved words
    return t

def t_TABLE_NAME(t):
    r"""[a-zA-Z][\_a-zA-Z0-9]*"""
    t.type = reserved.get(t.value, 'TABLE_NAME')    # Check for reserved words
    return t


def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


# Ignore newline
def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


# Ignore whitespace
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Caracter ilegal '%s" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

example_1 = """SELECT COUNT (DISTINCT NombreProducto) FROM Productos"""
example_2 = ("""SELECT NombreProducto 
FROM Productos 
WHERE NombreProducto BETWEEN Pasta_Italiana AND Pizza 
ORDER BY NombreProducto ASC""")
example_3 = ("""SELECT fecha_operacion, fecha_presentacion_srt, tipo_operacion, tipo_operacion_modificacion AS Operacion_de, ectm.descripcion AS Tipo_de_Modificacion, ec.periodo_prima, ec.monto_fijo_alic, ec.porc_alic 
FROM EMIS_Contratos_SRT AS ec INNER JOIN EMIS_Contratos_Tipos_Modificaciones AS ectm ON tipo_modificacion = cod_tipo_modificacion 
WHERE nro_contrato = 753603 AND ec.Fecha_Baja = 0 
ORDER BY ec.fecha_operacion DESC""")
example_4 = """SELECT eci.nro_contrato, oa.zona, oa.subzona, oa.nro_org, 
eci.nro_prod, ia.razon_social, oa.correo_electronico, eci.fecha_abm 
FROM EMIS_Contrato_Intermediarios AS eci INNER JOIN Organizadores_Aux AS oa ON 
eci.nro_empsoc = oa.nro_empsoc AND eci.nro_org = oa.nro_org 
WHERE eci.nro_org =244 ORDER BY eci.fecha_abm DESC"""
example_5 = """ SELECT nro FROM Tabla AS T"""
example_6 = '''SELECT c.first_name, c.last_name
FROM customers AS c'''
example_7 = '''SELECT c.first_name, c.last_name
FROM customers AS c
WHERE c.id = 2'''
example_8 = '''SELECT DISTINCT c.first_name, c.last_name, p.number
FROM customers AS c
LEFT JOIN phones_numbers AS p ON
c.id = p.customer_id
WHERE c.first_name = 'hola que tal 123'
'''


lexer.input(example_4)

while True:
    tok = lexer.token()
    if not tok:
        break          # No more input
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
