from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from db.modelos import Chat, ChatMensaje, Usuario, get_session

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
