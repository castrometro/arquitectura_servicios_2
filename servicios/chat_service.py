from datetime import datetime
import sys
import os
import json
from sqlalchemy.orm.exc import NoResultFound
from db.modelos import Chat, ChatMensaje, Usuario, get_session
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.bus as bus

def create_chat(id_usuario_remitente, id_usuario_receptor):
    session = get_session()
    try:
        nuevo_chat = Chat(
            id_usuario_remitente=id_usuario_remitente,
            id_usuario_receptor=id_usuario_receptor,
            fecha_chat=datetime.now()
        )
        session.add(nuevo_chat)
        session.commit()
        return nuevo_chat
    finally:
        session.close()

def get_chat(id_chat):
    session = get_session()
    try:
        chat = session.query(Chat).filter(Chat.id_chat == id_chat).one()
        return chat
    except NoResultFound:
        return {'error': 'Chat no encontrado'}
    finally:
        session.close()

def create_chat_mensaje(id_chat, id_usuario, contenido, archivo=None):
    session = get_session()
    try:
        nuevo_mensaje = ChatMensaje(
            id_chat=id_chat,
            id_usuario=id_usuario,
            contenido=contenido,
            archivo=archivo,
            fecha_mensaje=datetime.now()
        )
        session.add(nuevo_mensaje)
        session.commit()
        return nuevo_mensaje
    finally:
        session.close()

def get_chat_mensajes(id_chat):
    session = get_session()
    try:
        mensajes = session.query(ChatMensaje).filter(ChatMensaje.id_chat == id_chat).all()
        return mensajes
    except NoResultFound:
        return {'error': 'Mensajes no encontrados'}
    finally:
        session.close()

def process_chat_service(data):
    name_function = data['name_function']
    data = data['data']

    if name_function == 'create':
        return create_chat(data)
    elif name_function == 'get':
        return get_chat(data)
    elif name_function == 'create_mensaje':
        return create_chat_mensaje(data)
    elif name_function == 'get_mensajes':
        return get_chat_mensajes(data)

    else:
        return json.dumps({'error': 'Invalid function name'})

if __name__ == "__main__":
    logging.info('User service started')
    bus.run_service(process_chat_service, 'schat')
