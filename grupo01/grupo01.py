import sys
import ply.lex as lex

# PALABRAS RESERVADAS DE UNA QUERY SQL (HAY QUE VER SI CON ESTAS ES SUFICIENTE O HABRIA QUE ADICIONAR TODAS LAS DEMÁS)
reserved = {
    'AS': 'AS',
    'COUNT': 'COUNT',
    'DISTINCT': 'DISTINCT',
    'FROM': 'FROM',
    'GROUP_BY': 'GROUP_BY',
    'HAVING': 'HAVING',
    'INNER_JOIN': 'INNER_JOIN',
    'LEFT_JOIN': 'LEFT_JOIN',
    'MAX': 'MAX',
    'MIN': 'MIN',
    'ORDER_BY': 'ORDER_BY',
    'RIGHT_JOIN': 'RIGHT_JOIN',
    'SELECT': 'SELECT',
    'WHERE': 'WHERE',
    'ON':'ON',
    'DESC':'DESC',
    'ASC':'ASC',
    'DISTINCT':'DISTINCT',
    'BETWEEN':'BETWEEN',

    # String Data Types
    'BINARY': 'BINARY',
    'BLOB': 'BLOB',
    'CHAR': 'CHAR',
    'ENUM': 'ENUM',
    'LONGBLOB': 'LONGBLOB',
    'LONGTEXT': 'LONGTEXT',
    'MEDIUMBLOB': 'MEDIUMBLOB',
    'MEDIUMTEXT': 'MEDIUMTEXT',
    'SET': 'SET',
    'TEXT': 'TEXT',
    'TINYBLOB': 'TINYBLOB',
    'TINYTEXT': 'TINYTEXT',
    'VARBINARY': 'VARBINARY',
    'VARCHAR': 'VARCHAR',

    # Numeric Data Types
    'BIGINT': 'BIGINT',
    'BIT': 'BIT',
    'BOOL': 'BOOL',
    'BOOLEAN': 'BOOLEAN',
    'DEC': 'DEC',
    'DECIMAL': 'DECIMAL',
    'DOUBLE': 'DOUBLE',
    'DOUBLE_PRECISION': 'DOUBLE_PRECISION',
    'FLOAT': 'FLOAT',
    'INT': 'INT',
    'INTEGER': 'INTEGER',
    'MEDIUMINT': 'MEDIUMINT',
    'SMALLINT': 'SMALLINT',
    'TINYINT': 'TINYINT',
}

tokens = list(reserved.values()) + [
    # Comparison Operators (=, >, <, >=, <=, <>)
    'EQUAL_TO', 'GREATER_THAN', 'LESS_THAN', 'GREATER_THAN_OR_EQUAL_TO', 'LESS_THAN_OR_EQUAL_TO', 'NOT_EQUAL_TO',

    # Logical Operators (AND, OR)
    'AND', 'OR',

    # DELIMITADORES (( ) [ ] , .)
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COMMA', 'PERIOD',

    # Other data (name of the table, name of the column, ID for reserved words lookup)
    'TABLE_NAME', 'COLUMN_NAME', 'ID', 'NUMBER'
]

t_EQUAL_TO = r'\='
t_GREATER_THAN = r'\>'
t_LESS_THAN = r'\<'
t_GREATER_THAN_OR_EQUAL_TO = r'\>='
t_LESS_THAN_OR_EQUAL_TO = r'\<='
t_NOT_EQUAL_TO = r'\<>'

t_AND = r'AND'
t_OR = r'OR'

# delimitadores
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_PERIOD = r'\.'

# t_TABLE_NAME = r'[a-zA-Z_][a-zA-Z_0-9]*'
# t_COLUMN_NAME = r".[a-zA-Z_][a-zA-Z_0-9]*"

# Ignore whitespace
t_ignore = " \t"


# Ignore newline
# def t_newline(t):
#     r'\n+'
#     t.lexer.lineno += len(t.value)


# Check for reserved words
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Caracter ilegal '%s" % t.value[0])
    t.lexer.skip(1)


#lexer = lex.lex()

#lexer.input("""SELECT COUNT (DISTINCT NombreProducto) FROM Productos""")
    #("""SELECT NombreProducto FROM Productos WHERE NombreProducto BETWEEN Pasta_Italiana AND Pizza ORDER_BY NombreProducto ASC""")
    #("""SELECT fecha_operacion, fecha_presentacion_srt, tipo_operacion, tipo_operacion_modificacion AS Operacion_de, ectm.descripcion AS Tipo_de_Modificacion, ec.periodo_prima, ec.monto_fijo_alic, ec.porc_alic FROM EMIS_Contratos_SRT ec INNER_JOIN EMIS_Contratos_Tipos_Modificaciones ectm ON tipo_modificacion = cod_tipo_modificacion WHERE nro_contrato = 753603 AND ec.Fecha_Baja = 0 ORDER_BY ec.fecha_operacion DESC""")
    #("SELECT eci.nro_contrato, oa.zona, oa.subzona, oa.nro_org, eci.nro_prod, ia.razon_social, oa.correo_electronico, eci.fecha_abm FROM EMIS_Contrato_Intermediarios AS eci INNER_JOIN Organizadores_Aux AS oa ON eci.nro_empsoc = oa.nro_empsoc AND eci.nro_org = oa.nro_org WHERE nro_contrato = eci.nro_org =244 ORDER BY eci.fecha_abm DESC")
    #(""" SELECT nro FROM Tabla T""")
#
#while True:
#    tok = lexer.token()
#    if not tok:
#        break
#    print(tok)





import ply.yacc as yacc
# dictionary of tables
tables = {}

def p_select(p):
    'query : SELECT column_names FROM tables_name'
    tables[p[2]]#"""nombre de la tabla - VER BIEN"""

def p_select_where(p):
    'query : SELECT column_names FROM tables_name WHERE conditions'
    tables[p[2]]

def p_select_where_in(p):
    'query : SELECT column_names FROM tables_name WHERE conditions IN (SELECT column_names FROM tables_name WHERE condition)'
    tables[p[2]]

def p_select_where_orderby(p):
    'query : SELECT column_names FROM tables_name WHERE conditions ORDER_BY condition'
    tables[p[2]]

def p_select_where_orderby_desc(p):
    'query : SELECT column_names FROM tables_name WHERE conditions ORDER_BY condition DESC'
    tables[p[2]]

def p_select_where_orderby_asc(p):
    'query : SELECT column_names FROM tables_name WHERE conditions ORDER_BY condition ASC'
    tables[p[2]]

def p_select_where_groupby_orderby_(p):
    'query : SELECT column_names FROM tables_name WHERE conditions GROUP_BY column_names ORDER_BY condition'
    tables[p[2]]

def p_select_where_groupby_having_orderby_(p):
    'query : SELECT column_names FROM tables_name WHERE conditions GROUP_BY column_names HAVING condition ORDER_BY condition'
    tables[p[2]]

def p_select_innerjoin_where(p):
    'query : SELECT column_names FROM tables_name INNER_JOIN tables_name WHERE conditions'
    tables[p[2]]

def p_select_innerjoin_on_where(p):
    'query : SELECT column_names FROM tables_name INNER_JOIN tables_name ON conditions WHERE conditions'
    tables[p[2]]

def p_select_leftjoin_where(p):
    'query : SELECT column_names FROM tables_name LEFT_JOIN tables_name WHERE conditions'
    tables[p[2]]

def p_select_leftjoin_on_where(p):
    'query : SELECT column_names FROM tables_name LEFT_JOIN tables_name ON conditions WHERE conditions'
    tables[p[2]]

def p_select_rightjoin_where(p):
    'query : SELECT column_names FROM tables_name RIGHT_JOIN tables_name WHERE conditions'
    tables[p[2]]

def p_select_rightjoin_on_where(p):
    'query : SELECT column_names FROM tables_name RIGHT_JOIN tables_name ON conditions WHERE conditions'
    tables[p[2]]



