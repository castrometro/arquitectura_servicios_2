import sys
import os
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.bus as bus
from db.departamentos import create_departamento, delete_departamento, update_departamento, add_usuario_to_departamento, remove_usuario_from_departamento, get_usuarios_by_departamento, validate_usuario, delete_usuario, update_usuario, get_departamento

# Configurar logging
logging.basicConfig(filename='departamento_service.log', level=logging.INFO, format='%(asctime)s %(message)s')

def handle_create_departamento(data):
    required_fields = ['id_comunidad', 'numero', 'id_usuario_propietario']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    departamento = create_departamento(data['id_comunidad'], data['numero'], data['id_usuario_propietario'])
    return 'OK'

def handle_delete_departamento(data):
    required_fields = ['id_departamento']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    departamento = delete_departamento(data['id_departamento'])
    return json.dumps(departamento.to_dict())

def handle_update_departamento(data):
    required_fields = ['id_departamento']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    departamento = update_departamento(data['id_departamento'], data.get('numero'), data.get('id_usuario_propietario'))
    return 'OK'

def handle_add_usuario_to_departamento(data):
    required_fields = ['id_usuario', 'id_departamento']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    usuario_departamento = add_usuario_to_departamento(data['id_usuario'], data['id_departamento'])
    return 'OK'

def handle_remove_usuario_from_departamento(data):
    required_fields = ['id_usuario', 'id_departamento']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    usuario_departamento = remove_usuario_from_departamento(data['id_usuario'], data['id_departamento'])
    return 'OK'

def handle_get_usuarios_by_departamento(data):
    required_fields = ['id_departamento']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    usuarios = get_usuarios_by_departamento(data['id_departamento'])
    return json.dumps(usuarios)

def handle_validate_usuario(data):
    required_fields = ['id_usuario']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    usuario = validate_usuario(data['id_usuario'])
    return 'OK'

def handle_delete_usuario(data):
    required_fields = ['id_usuario']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    usuario = delete_usuario(data['id_usuario'])
    return json.dumps(usuario.to_dict())

def handle_update_usuario(data):
    required_fields = ['id_usuario']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    usuario = update_usuario(data['id_usuario'], data.get('rut'), data.get('tipo_usuario'), data.get('correo'), data.get('fono'), data.get('nombre'), data.get('apellido_paterno'), data.get('apellido_materno'), data.get('estado_cuenta'), data.get('contrasena'))
    return 'OK'

def process_departamento_service(data):
    name_function = data['name_function']
    data = data['data']

    if name_function == 'create':
        return handle_create_departamento(data)
    elif name_function == 'delete':
        return handle_delete_departamento(data)
    elif name_function == 'update':
        return handle_update_departamento(data)
    elif name_function == 'add_usuario':
        return handle_add_usuario_to_departamento(data)
    elif name_function == 'remove_usuario':
        return handle_remove_usuario_from_departamento(data)
    elif name_function == 'get_usuarios':
        return handle_get_usuarios_by_departamento(data)
    elif name_function == 'validate_usuario':
        return handle_validate_usuario(data)
    elif name_function == 'delete_usuario':
        return handle_delete_usuario(data)
    elif name_function == 'update_usuario':
        return handle_update_usuario(data)
    else:
        return json.dumps({'error': 'Invalid function name'})

if __name__ == "__main__":
    logging.info('Departamento service started')
    bus.run_service(process_departamento_service, 'departamento')
