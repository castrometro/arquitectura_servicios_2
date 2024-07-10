import sys
import os
import json
import bcrypt
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.bus as bus
from db.usuarios import *

# Configurar logging
logging.basicConfig(filename='user_service.log', level=logging.INFO, format='%(asctime)s %(message)s')

def handle_create_user(data):
    required_fields = ['rut', 'tipo_usuario', 'correo', 'fono', 'nombre', 'apellido_paterno', 'apellido_materno', 'estado_cuenta', 'contrasena']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    data = create_usuario(
        id_comunidad=data['id_comunidad'],
        rut=data['rut'],
        tipo_usuario=data['tipo_usuario'],
        correo=data['correo'],
        fono=data['fono'],
        nombre=data['nombre'],
        apellido_paterno=data['apellido_paterno'],
        apellido_materno=data['apellido_materno'],
        estado_cuenta=data['estado_cuenta'],
        contrasena=data['contrasena']
    )
    return json.dumps(data)

 

def handle_get_user(data):
    required_fields = ['id_usuario']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    usuario = get_usuario(data['id_usuario'])
    return json.dumps(usuario)
    

def handle_get_all_users():
    usuarios = get_usuarios()
    for usuario in usuarios:
        print(usuario)
    return json.dumps([usuario.to_dict() for usuario in usuarios])

def handle_update_user(data):
    required_fields = ['id_usuario', 'rut', 'tipo_usuario', 'correo', 'fono', 'nombre', 'apellido_paterno', 'apellido_materno', 'estado_cuenta']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    update_usuario(
        id_usuario=data['id_usuario'],
        rut=data['rut'],
        tipo_usuario=data['tipo_usuario'],
        correo=data['correo'],
        fono=data['fono'],
        nombre=data['nombre'],
        apellido_paterno=data['apellido_paterno'],
        apellido_materno=data['apellido_materno'],
        estado_cuenta=data['estado_cuenta']
    )
    usuario = get_usuario(data['id_usuario'])

    if isinstance(usuario, dict) and 'error' in usuario:
        return json.dumps(usuario)
    else:
        return json.dumps(usuario)

def handle_delete_user(data):
    required_fields = ['id_usuario']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    usuario = get_usuario(data['id_usuario'])

    if isinstance(usuario, dict) and 'error' in usuario:
        return json.dumps(usuario)
    else:
        delete_usuario(data['id_usuario'])
        return 'Usuario eliminado correctamente'

def handle_login_user(data):
    required_fields = ['rut', 'contrasena']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    usuario = login_usuario(rut=data['rut'], contrasena=data['contrasena'])
    if isinstance(usuario, dict) and ('error' in usuario):
        return json.dumps(usuario)
    return json.dumps(usuario.to_dict_private())

def handle_register_user(data):
    required_fields = ['rut', 'tipo_usuario', 'correo', 'fono', 'nombre', 'apellido_paterno', 'apellido_materno', 'contrasena']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    usuario = register_usuario(
        rut=data['rut'],
        tipo_usuario=data['tipo_usuario'],
        correo=data['correo'],
        fono=data['fono'],
        nombre=data['nombre'],
        apellido_paterno=data['apellido_paterno'],
        apellido_materno=data['apellido_materno'],
        contrasena=data['contrasena']
    )
    return json.dumps(usuario.to_dict_private())

def handle_add_admin_user(data):
    required_fields = ['id_asignador', 'id_usuario', 'id_comunidad']
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    asignador = get_usuario(data.get('id_asignador'))
    if(asignador.tipo_usuario == 'ADMINISTRADOR_SISTEMA'):
        return
    else:
        return 'No tiene permisos para realizar esta acción'

def handle_update_privacidad(data):
    required_fields = ['id_usuario', 'privacidad']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})

    usuario = update_privacidad_usuario(
        id_usuario=data['id_usuario'],
        privacidad=data['privacidad']
    )
    return 'OK'

def handle_get_user_visible(data):
    required_fields = ['id_usuario', 'requestor_id']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})

    usuario = get_usuario_visible(data['id_usuario'], data['requestor_id'])
    return json.dumps(usuario)

def process_user_service(data):
    name_function = data['name_function']
    data = data['data']
    print (name_function)
    print (data)
    if name_function == 'create':
        return handle_create_user(data)
    elif name_function == 'get':
        return handle_get_user(data)
    elif name_function == 'all':
        return handle_get_all_users()
    elif name_function == 'update':
        return handle_update_user(data)
    elif name_function == 'delete':
        return handle_delete_user(data)
    elif name_function == 'login':
        return handle_login_user(data)
    elif name_function == 'register':
        return handle_register_user(data)
    elif name_function == 'update_privacidad':
        return handle_update_privacidad(data)
    elif name_function == 'get_user_visible':
        return handle_get_user_visible(data)
    else:
        return json.dumps({'error': 'Invalid function name'})

if __name__ == "__main__":
    logging.info('User service started')
    bus.run_service(process_user_service, 'suser')
