import sys
import ply.lex as lex

#PALABRAS RESERVADAS DE UNA QUERY SQL (HAY QUE VER SI CON ESTAS ES SUFICIENTE O HABRIA QUE ADICIONAR TODAS LAS DEMÁS)
reserved=('SELECT','FROM', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'AS','WHERE','IN','GROUP BY','HAVING','ORDER BY')

tokens= reserved + (
#OPERADORES (or, and, not in, is null, is not null, <, <=, >, >=, count, min, max)
    'or', 'and', 'not in', 'is null', 'is not null', 'LT', 'LE', 'GT', 'GE', 'count', 'min', 'max'
#demás datos (nombres de tablas, campos, etc)
    'NAME'
)

t_NAME = r'[a-zA-Z_]*'
t_ignore=" \t" #ignoramos el espacio vacío (ver bien si sql ejecuta una query si le elimino los espacios vacíos)

def t_error(t):
    print ("Caracter ilegal '%s" % t.value[0])
    t.lexer.skip(1)

lexer=lex.lex()



