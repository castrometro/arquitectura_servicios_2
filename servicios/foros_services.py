import sys
import os
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.bus as bus
from db.foros import create_foro, get_foro, get_foro_by_all_not_id, get_foros, update_foro, delete_foro, create_foro_mensaje, get_foro_mensajes
from db.usuarios import get_usuario  # para verificar luego si es admin o no
from db.comunidad import get_comunidad  # para ver la comunidad a que pertenece el usuario

# Configurar logging
logging.basicConfig(filename='foro_service.log', level=logging.INFO, format='%(asctime)s %(message)s')

def handle_create_foro(data):
    required_fields = ['id_comunidad', 'id_usuario', 'tipo_foro', 'estado_foro', 'tema_foro']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})

    # Obtener usuario y verificar si es administrador de la comunidad
    usuario = get_usuario(data['id_usuario'])
    if usuario.tipo_usuario != 'ADMINISTRADOR':
        return json.dumps({'error': 'Usuario no autorizado para crear foros'})

    comunidad = get_comunidad(data['id_comunidad'])
    if comunidad.id_usuario != data['id_usuario']:
        return json.dumps({'error': 'El usuario no es administrador de esta comunidad'})

    create_foro(
        id_comunidad=data['id_comunidad'],
        id_usuario=data['id_usuario'],
        tipo_foro=data['tipo_foro'],
        estado_foro=data['estado_foro'],
        tema_foro=data['tema_foro']
    )
    foro = get_foro_by_all_not_id(data)
    if isinstance(foro, dict) and 'error' in foro:
        return json.dumps(foro)
    else:
        return json.dumps(foro.to_dict())

def handle_get_foro(data):
    required_fields = ['id_foro']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    foro = get_foro(data['id_foro'])
    return json.dumps(foro.to_dict())

def handle_get_foros(data):
    foros = get_foros()
    return json.dumps([foro.to_dict() for foro in foros])

def handle_update_foro(data):
    required_fields = ['id_foro', 'tipo_foro', 'estado_foro', 'tema_foro']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    update_foro(
        id_foro=data['id_foro'],
        tipo_foro=data['tipo_foro'],
        estado_foro=data['estado_foro'],
        tema_foro=data['tema_foro']
    )
    foro = get_foro(data['id_foro'])
    if isinstance(foro, dict) and 'error' in foro:
        return json.dumps(foro)
    else:
        return json.dumps(foro.to_dict())

def handle_delete_foro(data):
    required_fields = ['id_foro']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    delete_foro(data['id_foro'])
    foro = get_foro(data['id_foro'])
    if isinstance(foro, dict) and 'error' in foro:
        return json.dumps(foro)
    else:
        return json.dumps(foro.to_dict())

def handle_create_foro_mensaje(data):
    required_fields = ['id_usuario', 'id_foro', 'contenido']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    nuevo_mensaje = create_foro_mensaje(
        id_usuario=data['id_usuario'],
        id_foro=data['id_foro'],
        contenido=data['contenido'],
        archivo=data.get('archivo')
    )
    if isinstance(nuevo_mensaje, dict) and 'error' in nuevo_mensaje:
        return json.dumps(nuevo_mensaje)
    else:
        return json.dumps(nuevo_mensaje.to_dict())

def handle_get_foro_mensajes(data):
    required_fields = ['id_foro']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    mensajes = get_foro_mensajes(data['id_foro'])
    if isinstance(mensajes, dict) and 'error' in mensajes:
        return json.dumps(mensajes)
    else:
        return json.dumps([mensaje.to_dict() for mensaje in mensajes])

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
    elif name_function == 'create_mensaje':
        return handle_create_foro_mensaje(data)
    elif name_function == 'get_mensajes':
        return handle_get_foro_mensajes(data)
    else:
        return json.dumps({'error': 'Invalid function name'})

if __name__ == "__main__":
    logging.info('Foro service started')
    bus.run_service(process_foro_service, 'foros')
