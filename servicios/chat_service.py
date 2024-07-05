import sys
import os
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.modelos import Chat, ChatMensaje, Usuario, get_session
from db.chats import create_chat, get_chat, create_chat_mensaje, get_chat_mensajes
from db.usuarios import get_usuario
from db.comunidad import get_comunidad



import utils.bus as bus

# Configurar logging
logging.basicConfig(filename='chat_service.log', level=logging.INFO, format='%(asctime)s %(message)s')

def handle_create_chat(data):
    required_fields = ['id_usuario_remitente', 'id_usuario_receptor']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})

    usuario_remitente = get_usuario(data['id_usuario_remitente'])
    usuario_receptor = get_usuario(data['id_usuario_receptor'])

    # if usuario_remitente.tipo_usuario == 'ADMINISTRADOR':
    #     comunidad_remitente = get_comunidad(usuario_remitente.id_comunidad)
    #     if usuario_receptor.id_comunidad != comunidad_remitente.id_comunidad:
    #         return json.dumps({'error': 'El residente no pertenece a la comunidad del administrador'})

    # elif usuario_remitente.tipo_usuario == 'RESIDENTE':
    #     if usuario_receptor.tipo_usuario != 'ADMINISTRADOR' or usuario_remitente.id_comunidad != usuario_receptor.id_comunidad:
    #         return json.dumps({'error': 'El residente solo puede crear chats con el administrador de su comunidad'})
    
    # else:
    #     return json.dumps({'error': 'Solo los administradores y residentes pueden crear chats directos'})

    nuevo_chat = create_chat(data['id_usuario_remitente'], data['id_usuario_receptor'])
    return 'OK'

def handle_get_chat(data):
    required_fields = ['id_chat']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})

    chat = get_chat(data['id_chat'])
    print(chat)
    print(chat.to_dict())
    return json.dumps(chat.to_dict())

def handle_create_chat_mensaje(data):
    required_fields = ['id_chat', 'id_usuario', 'contenido']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})

    nuevo_mensaje = create_chat_mensaje(
        id_chat=data['id_chat'],
        id_usuario=data['id_usuario'],
        contenido=data['contenido'],
        archivo=data.get('archivo')
    )
    return 'OK'

def handle_get_chat_mensajes(data):
    required_fields = ['id_chat']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})

    mensajes = get_chat_mensajes(data['id_chat'])
    return json.dumps([mensaje.to_dict() for mensaje in mensajes])

def process_chat_service(data):
    name_function = data['name_function']
    data = data['data']

    if name_function == 'create':
        return handle_create_chat(data)
    elif name_function == 'get':
        return handle_get_chat(data)
    elif name_function == 'create_mensaje':
        return handle_create_chat_mensaje(data)
    elif name_function == 'get_mensajes':
        return handle_get_chat_mensajes(data)
    else:
        return json.dumps({'error': 'Invalid function name'})

if __name__ == "__main__":
    logging.info('Chat service started')
    bus.run_service(process_chat_service, 'chats')
