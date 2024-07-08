import sys
import os
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.bus as bus
from db.comunidad import *

# Configurar logging
logging.basicConfig(filename='comunidad_service.log', level=logging.INFO, format='%(asctime)s %(message)s')

def handle_create_comunidad(data):
    required_fields = ['nombre_comunidad']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    create_comunidad(data['nombre_comunidad'])
    comunidad = get_comunidad_by_nombre(data['nombre_comunidad'])
    if isinstance(comunidad, dict) and 'error' in comunidad:
        return json.dumps(comunidad)
    else:
        return json.dumps(comunidad.to_dict())

def handle_get_comunidad(data):
    required_fields = ['id_comunidad']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    comunidad = get_comunidad(data['id_comunidad'])
    if isinstance(comunidad, dict) and 'error' in comunidad:
        return json.dumps(comunidad)
    else:
        return json.dumps(comunidad.to_dict())

def handle_get_all_comunidades(data):
    comunidades = get_comunidades()
    return json.dumps([comunidad.to_dict() for comunidad in comunidades])

def handle_update_comunidad(data):
    required_fields = ['id_comunidad', 'nombre_comunidad']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    update_comunidad(data['id_comunidad'], data['nombre_comunidad'])
    print ('------')
    print (data['id_comunidad'], data['nombre_comunidad'])
    print ('------')
    comunidad = get_comunidad(data['id_comunidad'])

    if isinstance(comunidad, dict) and 'error' in comunidad:
        return json.dumps(comunidad)
    else:
        return json.dumps(comunidad.to_dict())

def handle_delete_comunidad(data):
    required_fields = ['id_comunidad']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
     
    delete_comunidad(data['id_comunidad'])
    return 'Comunidad eliminada correctamente'
   


def process_comunidad_service(data):
    name_function = data['name_function']
    data = data['data']

    if name_function == 'create':
        return handle_create_comunidad(data)
    elif name_function == 'get':
        return handle_get_comunidad(data)
    elif name_function == 'all':
        return handle_get_all_comunidades(data)
    elif name_function == 'update':
        return handle_update_comunidad(data)
    elif name_function == 'delete':
        return handle_delete_comunidad(data)
    else:
        return json.dumps({'error': 'Invalid function name'})

if __name__ == "__main__":
    logging.info('Comunidad service started')
    bus.run_service(process_comunidad_service, 'comun')
