import sys
import ply.lex as lex

# PALABRAS RESERVADAS DE UNA QUERY SQL (HAY QUE VER SI CON ESTAS ES SUFICIENTE O HABRIA QUE ADICIONAR TODAS LAS DEMÁS)
reserved = (
    'AS', 'COUNT', 'DISTINCT', 'FROM', 'GROUP_BY', 'HAVING', 'INNER_JOIN', 'LEFT_JOIN', 'MAX', 'MIN', 'ORDER_BY',
    'RIGHT_JOIN', 'SELECT', 'WHERE',
    # String Data Types
    'BINARY', 'BLOB', 'CHAR', 'ENUM', 'LONGBLOB', 'LONGTEXT', 'MEDIUMBLOB', 'MEDIUMTEXT', 'SET', 'TEXT', 'TINYBLOB',
    'TINYTEXT', 'VARBINARY', 'VARCHAR',
    # Numeric Data Types
    'BIGINT', 'BIT', 'BOOL', 'BOOLEAN', 'DEC', 'DECIMAL', 'DOUBLE', 'DOUBLE_PRECISION', 'FLOAT', 'INT', 'INTEGER',
    'MEDIUMINT', 'SMALLINT', 'TINYINT',
    # Date and Time Data Types
    'DATE', 'DATETIME', 'TIME', 'TIMESTAMP', 'YEAR',
)

t_AS = r'AS'
t_COUNT = r'COUNT'
t_DISTINCT = r'DISTINCT'
t_FROM = r'FROM'
t_GROUP_BY = r'GROUP_BY'
t_HAVING = r'HAVING'
t_INNER_JOIN = r'INNER JOIN'
t_LEFT_JOIN = r'LEFT JOIN'
t_MAX = r'MAX'
t_MIN = r'MIN'
t_ORDER_BY = r'ORDER BY'
t_RIGHT_JOIN = r'RIGHT JOIN'
t_SELECT = r'SELECT'
t_WHERE = r'WHERE'

t_BINARY = r'BINARY'
t_BLOB = r'BLOB'
t_CHAR = r'CHAR'
t_ENUM = r'ENUM'
t_LONGBLOB = r'LONGBLOB'
t_LONGTEXT = r'LONGTEXT'
t_MEDIUMBLOB = r'MEDIUMBLOB'
t_MEDIUMTEXT = r'MEDIUMTEXT'
t_SET = r'SET'
t_TEXT = r'TEXT'
t_TINYBLOB = r'TINYBLOB'
t_TINYTEXT = r'TINYTEXT'
t_VARBINARY = r'VARBINARY'
t_VARCHAR = r'VARCHAR'

t_BIGINT = r'BIGINT'
t_BIT = r'BIT'
t_BOOL = r'BOOL'
t_BOOLEAN = r'BOOLEAN'
t_DEC = r'DEC'
t_DECIMAL = r'DECIMAL'
t_DOUBLE = r'DOUBLE'
t_DOUBLE_PRECISION = r'DOUBLE PRECISION'
t_FLOAT = r'FLOAT'
t_INT = r'INT'
t_INTEGER = r'INTEGER'
t_MEDIUMINT = r'MEDIUMINT'
t_SMALLINT = r'SMALLINT'
t_TINYINT = r'TINYINT'

t_DATE = r'DATE'
t_DATETIME = r'DATETIME'
t_TIME = r'TIME'
t_TIMESTAMP = r'TIMESTAMP'
t_YEAR = r'YEAR'

tokens = reserved + (
    # Arithmetic Operators (+, -, *, /, %)
    'ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', 'MODULO',
    # Bitwise Operators (&, |, ^)
    'BITWISE_AND', 'BITWISE_OR', 'BITWISE_EXCLUSIVE_OR',
    # Comparison Operators (=, >, <, >=, <=, <>)
    'EQUAL_TO', 'GREATER_THAN', 'LESS_THAN', 'GREATER_THAN_OR_EQUAL_TO', 'LESS_THAN_OR_EQUAL_TO', 'NOT_EQUAL_TO',
    # Compound Operators (+=, -=, *=, /=, %=, &=, ^-=, |*=)
    'ADD_EQUALS', 'SUBTRACT_EQUALS', 'MULTIPLY_EQUALS', 'DIVIDE_EQUALS', 'MODULO_EQUALS', 'BITWISE_AND_EQUALS',
    'BITWISE_EXCLUSIVE_EQUALS', 'BITWISE_OR_EQUALS',
    # Logical Operators (ALL, AND, ANY, BETWEEN, EXIST, IN, LIKE, NOT, OR, SOME)
    'ALL', 'AND', 'ANY', 'BETWEEN', 'EXIST', 'IN', 'LIKE', 'NOT', 'OR', 'SOME',

    # Other data (name of the table, name of the column)
    'TABLE_NAME', 'COLUMN_NAME'

    # DELIMITADORES (( ) [ ] , .)
                  'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'COMMA', 'PERIOD',
)

t_ADD = r'\+'
t_SUBTRACT = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_MODULO = r'\%'

t_BITWISE_AND = r'\&'
t_BITWISE_OR = r'\|'
t_BITWISE_EXCLUSIVE_OR = r'\^'

t_EQUAL_TO = r'\='
t_GREATER_THAN = r'\>'
t_LESS_THAN = r'\<'
t_GREATER_THAN_OR_EQUAL_TO = r'\>='
t_LESS_THAN_OR_EQUAL_TO = r'\<='
t_NOT_EQUAL_TO = r'\<>'

t_ADD_EQUALS = r'\+='
t_SUBTRACT_EQUALS = r'\-='
t_MULTIPLY_EQUALS = r'\*='
t_DIVIDE_EQUALS = r'\/='
t_MODULO_EQUALS = r'\%='
t_BITWISE_AND_EQUALS = r'\&='
t_BITWISE_EXCLUSIVE_EQUALS = r'\^-='
t_BITWISE_OR_EQUALS = r'\|*='

t_ALL = r'ALL'
t_AND = r'AND'
t_ANY = r'ANY'
t_BETWEEN = r'BETWEEN'
t_EXIST = r'EXIST'
t_IN = r'IN'
t_LIKE = r'LIKE'
t_NOT = r'NOT'
t_OR = r'OR'
t_SOME = r'SOME'

t_TABLE_NAME = r'[a-zA-Z_]'
t_COLUMN_NAME = r'[a-zA-Z_]'

t_ignore = " \t"  # ignoramos el espacio vacío (ver bien si sql ejecuta una query si le elimino los espacios vacíos)

# delimitadores
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_PERIOD = r'\.'


def t_error(t):
    print("Caracter ilegal '%s" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
