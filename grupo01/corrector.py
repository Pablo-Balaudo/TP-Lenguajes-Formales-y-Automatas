import importlib
import os

files = os.listdir('.')
module_file = [f.split('.')[0] for f in files if 'grupo' in f][0]

grupo = importlib.import_module(module_file)

samples = [
    ('''SELECT c.first_name,
               c.last_name
        FROM customers AS c''', {'customers': ['first_name', 'last_name']}),
    ('''SELECT c.first_name,
               c.last_name
        FROM customers AS c
        WHERE c.id = 2''', {'customers': ['first_name', 'id', 'last_name']}),
    ('''SELECT DISTINCT c.first_name,
                        c.last_name,
                        p.number
        FROM customers AS c
            LEFT JOIN phones_numbers AS p ON
                c.id = p.customer_id
        ''', {'customers': ['first_name', 'id', 'last_name'],
              'phones_numbers': ['customer_id', 'number']}),
    ("""SELECT eci.nro_contrato, 
               oa.zona, 
               oa.subzona, 
               oa.nro_org, 
               eci.nro_prod, 
               oa.correo_electronico, 
               eci.fecha_abm 
        FROM EMIS_Contrato_Intermediarios AS eci 
            INNER JOIN Organizadores_Aux AS oa ON 
                eci.nro_empsoc = oa.nro_empsoc AND eci.nro_org = oa.nro_org 
        WHERE eci.nro_org = 244 
        ORDER BY eci.fecha_abm DESC""",
     {'EMIS_Contrato_Intermediarios': ['fecha_abm', 'nro_contrato', 'nro_empsoc', 'nro_org', 'nro_prod'],
      'Organizadores_Aux': ['correo_electronico', 'nro_empsoc', 'nro_org', 'subzona', 'zona']}),
    ("""SELECT T.asd 
        FROM Tabla AS T""", {'Tabla': ['asd']}),

    ('''SELECT DISTINCT c.first_name, 
                        c.last_name, 
                        p.number
        FROM customers AS c
            LEFT JOIN phones_numbers AS p ON
                c.id = p.customer_id
        WHERE c.first_name = 'hola que tal 123' AND (p.number = 123)
    ''', {'customers': ['first_name', 'id', 'last_name'],
          'phones_numbers': ['customer_id', 'number']})

]

for ix, sample in enumerate(samples):
    print('***** Resultados test parsing ejemplo {} *****'.format(ix + 1))
    print(sample[0])
    print('-' * 3, ' Fin consulta ', '-' * 3)

    try:
        result = grupo.parse_select_statement(sample[0])

        if result != sample[1]:
            resultStr = 'incorrecto'
        else:
            resultStr = 'correcto'

        print('El resultado de la comprobación fue {} !'.format(resultStr))
        print('Resultado entregado: ', result)
        print('Resultado esperado:  ', sample[1])

    except Exception as e:
        print('''Se produjo una excepción al intentar parsear el ejemplo y/o 
                 comprobar el resultado !''')
        print(e)
    print('')
