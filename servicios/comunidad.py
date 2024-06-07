import socket
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.bus as bus
from db.comunidad import create_comunidad, get_comunidades, get_comunidad

def process_comunidad_service(data):

    print(data, 'DATA QUE VIENE DEL CLIENTE')

    if(data['name_function'] == 'create'):
        comunidad = create_comunidad('villa esperanza')
        print(comunidad, data)
        return 'OK'
    if(data['name_function'] == 'all'):
        comunidades = get_comunidades()
        print(comunidades, data)
        return json.dumps([comunidad.to_dict() for comunidad in comunidades])
    if(data['name_function'] == 'put'):
        comunidades = get_comunidades()
        print(comunidades, data)
        return json.dumps([comunidad.to_dict() for comunidad in comunidades])
    if(data['name_function'] == 'get'):
        id_comunidad = data['data']['id']
        comunidad = get_comunidad(id_comunidad)
        print(comunidades, data)
        return json.dumps([comunidad.to_dict() for comunidad in comunidades])
        # return json.dumps(comunidad.to_dict())
    
bus.run_service(process_comunidad_service, 'comun')

def process_user_service(data):

    print(data, 'DATA QUE VIENE DEL CLIENTE')

    if(data['name_function'] == 'create'):
        comunidad = create_comunidad('villa esperanza')
        print(comunidad, data)
        return 'OK'
    if(data['name_function'] == 'all'):
        comunidades = get_comunidades()
        print(comunidades, data)
        return json.dumps([comunidad.to_dict() for comunidad in comunidades])
        # return json.dumps(comunidad.to_dict())
    
bus.run_service(process_user_service, 'suser')