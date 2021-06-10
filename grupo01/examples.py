import os
import sys
import importlib

files = os.listdir('.')
module_file = [f.split('.')[0] for f in files if 'grupo' in f][0]
grupo = importlib.import_module(module_file)

examples = ("""SELECT eci.nro_contrato, oa.zona, oa.subzona, oa.nro_org, 
eci.nro_prod, oa.correo_electronico, eci.fecha_abm 
FROM EMIS_Contrato_Intermediarios AS eci INNER JOIN Organizadores_Aux AS oa ON 
eci.nro_empsoc = oa.nro_empsoc AND eci.nro_org = oa.nro_org 
WHERE eci.nro_org =244 ORDER BY eci.fecha_abm DESC""",

""" SELECT T.asd FROM Tabla AS T""",

'''SELECT c.first_name, c.last_name
FROM customers AS c''',

'''SELECT c.first_name, c.last_name
FROM customers AS c
WHERE c.id = 2''',

'''SELECT DISTINCT c.first_name, c.last_name, p.number
FROM customers AS c
LEFT JOIN phones_numbers AS p ON
c.id = p.customer_id
WHERE c.first_name = 'hola que tal 123'
AND (p.number = 123)
''')

for num, example in enumerate(examples):
    print(f'-- RUNNING EXAMPLE { num + 1 } --')
    result = grupo.parse_select_statement(example, debug = True)
    print('\n Result: ', result, '\n')
