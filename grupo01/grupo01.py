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
    'TABLE_NAME', 'COLUMN_NAME', 'ID'
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


def t_error(t):
    print("Caracter ilegal '%s" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

# lexer.input(""" SELECT nro FROM Tabla T""")
#
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)
