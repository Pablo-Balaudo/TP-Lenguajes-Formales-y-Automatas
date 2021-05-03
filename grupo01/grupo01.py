import sys
import ply.lex as lex

# PALABRAS RESERVADAS DE UNA QUERY SQL (HAY QUE VER SI CON ESTAS ES SUFICIENTE O HABRIA QUE ADICIONAR TODAS LAS DEMÁS)
reserved = (
    'AS', 'DISTINCT', 'FROM', 'GROUP_BY', 'HAVING', 'INNER_JOIN', 'LEFT_JOIN', 'ORDER_BY', 'RIGHT_JOIN', 'SELECT',
    'WHERE')

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


def t_error(t):
    print("Caracter ilegal '%s" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
