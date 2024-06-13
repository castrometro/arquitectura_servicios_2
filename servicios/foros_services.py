import sys
import os
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.bus as bus
from db.foros import create_foro, get_foro, update_foro, delete_foro, get_foros
from db.usuarios import get_usuario # para verificar luego si es admin o no
from db.comunidad import get_comunidad # para ver la comunidad a que pertenece el usuario

# Configurar logging
logging.basicConfig(filename='foro_service.log', level=logging.INFO, format='%(asctime)s %(message)s')

def handle_create_foro(data):
    required_fields = ['id_comunidad', 'id_usuario', 'tipo_foro', 'estado_foro', 'tema_foro']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})

    # Obtener usuario y verificar si es administrador de la comunidad
    usuario = get_usuario(data['id_usuario'])
    if usuario.tipo_usuario != 'admin':
        return json.dumps({'error': 'Usuario no autorizado para crear foros'})
    
    comunidad = get_comunidad(data['id_comunidad'])
    if comunidad.id_usuario != data['id_usuario']:
        return json.dumps({'error': 'El usuario no es administrador de esta comunidad'})
    
    foro = create_foro(
        id_comunidad=data['id_comunidad'],
        id_usuario=data['id_usuario'],
        tipo_foro=data['tipo_foro'],
        estado_foro=data['estado_foro'],
        tema_foro=data['tema_foro']
    )
    return 'OK'

def handle_get_foro(data):
    required_fields = ['id_foro']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    foro = get_foro(data['id_foro'])
    return json.dumps(foro.to_dict())

# Funcion para ver todos los foros (pdte)
def handle_get_foros(data):
    foros = get_foros()
    return json.dumps([foro.to_dict() for foro in foros])

def handle_update_foro(data):
    required_fields = ['id_foro', 'tipo_foro', 'estado_foro', 'tema_foro']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    foro = update_foro(
        id_foro=data['id_foro'],
        tipo_foro=data['tipo_foro'],
        estado_foro=data['estado_foro'],
        tema_foro=data['tema_foro']

    )
    return 'OK'

def handle_delete_foro(data):
    required_fields = ['id_foro']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    foro = delete_foro(data['id_foro'])
    return json.dumps(foro.to_dict())

def process_foro_service(data):
    name_function = data['name_function']
    data = data['data']

    if name_function == 'create':
        return handle_create_foro(data)
    elif name_function == 'all':
        return handle_get_foros(data)
    elif name_function == 'get':
        return handle_get_foro(data)
    elif name_function == 'update':
        return handle_update_foro(data)
    elif name_function == 'delete':
        return handle_delete_foro(data)
    else:
        return json.dumps({'error': 'Invalid function name'})

if __name__ == "__main__":
    logging.info('Foro service started')
    bus.run_service(process_foro_service, 'foros')
