import sys
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from sqlalchemy.orm import joinedload
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.modelos import Foro, ForoMensaje, Usuario, get_session

DEFAULT_CONFIG_MAILER = {
    'host': "smtp.hostinger.com",
    'port': 465,
    'secure': True,
    'auth': {
        'user': "comprobantes@proliftingenieria.cl",
        'pass': "v10l3t488@V",
    },
}

def enviar_correo(correo_destinatario, asunto, mensaje):
    smtp_server = DEFAULT_CONFIG_MAILER['host']
    smtp_port = DEFAULT_CONFIG_MAILER['port']
    smtp_usuario = DEFAULT_CONFIG_MAILER['auth']['user']
    smtp_contrasena = DEFAULT_CONFIG_MAILER['auth']['pass']

    # Crear el objeto MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = smtp_usuario
    msg['To'] = correo_destinatario
    msg['Subject'] = asunto

    # Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        # Configurar la conexión al servidor SMTP
        server = smtplib.SMTP_SSL(smtp_server, smtp_port) if DEFAULT_CONFIG_MAILER['secure'] else smtplib.SMTP(smtp_server, smtp_port)
        server.login(smtp_usuario, smtp_contrasena)
        
        # Enviar el correo
        server.sendmail(smtp_usuario, correo_destinatario, msg.as_string())
        server.quit()
        
        print(f'Correo enviado a {correo_destinatario}')
    except Exception as e:
        print(f'Error al enviar el correo: {e}')

def enviar_notificacion(id_usuario, mensaje):
    # Implementar lógica de envío de notificaciones aquí
    pass

def create_foro(id_comunidad, id_usuario, tipo_foro, estado_foro, tema_foro):
    session = get_session()
    try:
        nuevo_foro = Foro(
            id_comunidad=id_comunidad,
            id_usuario=id_usuario,
            tipo_foro=tipo_foro,
            estado_foro=estado_foro,
            tema_foro=tema_foro
        )
        session.add(nuevo_foro)
        session.commit()
        return nuevo_foro
    finally:
        session.close()

def get_foro(id_foro):
    session = get_session()
    try:
        foro = session.query(Foro).filter(Foro.id_foro == id_foro).one()
        return foro
    except NoResultFound:
        return {'error': 'Foro no encontrado'}
    finally:
        session.close()

def get_foro_by_all_not_id(data):
    session = get_session()
    try:
        foro = session.query(Foro).filter(
            Foro.id_usuario == data['id_usuario'],
            Foro.tipo_foro == data['tipo_foro'],
            Foro.estado_foro == data['estado_foro'],
            Foro.tema_foro == data['tema_foro']
        ).one()
        return foro
    except NoResultFound:
        return {'error': 'Foro no encontrado'}
    finally:
        session.close()

def get_foros():
    session = get_session()
    try:
        foros = session.query(Foro).all()
        return foros
    except NoResultFound:
        return {'error': 'No hay foros'}
    finally:
        session.close()

def delete_foro(id_foro):
    session = get_session()
    try:
        foro = session.query(Foro).filter(Foro.id_foro == id_foro).one()
        session.delete(foro)
        session.commit()
        return foro
    except NoResultFound:
        return {'error': 'Foro no encontrado'}
    finally:
        session.close()

def update_foro(id_foro, tipo_foro, estado_foro, tema_foro):
    session = get_session()
    try:
        foro = session.query(Foro).filter(Foro.id_foro == id_foro).one()
        if tipo_foro != '0':
            foro.tipo_foro = tipo_foro
        if estado_foro != '0':
            foro.estado_foro = estado_foro
        if tema_foro != '0':
            foro.tema_foro = tema_foro
        session.commit()
        return foro
    except NoResultFound:
        return {'error': 'Foro no encontrado'}
    finally:
        session.close()

# Métodos para enviar mensajes a un foro

def create_foro_mensaje(id_usuario, id_foro, contenido, archivo=None):
    session = get_session()
    try:
        foro = session.query(Foro).options(joinedload(Foro.id_comunidad)).filter(Foro.id_foro == id_foro).one()
        usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).one()

        if foro.tipo_foro == 'importante' and usuario.tipo_usuario != 'ADMINISTRADOR':
            return {'error': 'Solo el Administrador de Comunidad puede enviar mensajes en foros importantes'}

        nuevo_mensaje = ForoMensaje(
            id_usuario=id_usuario,
            id_foro=id_foro,
            fecha=datetime.now(),
            hora=datetime.now(),
            contenido=contenido,
            archivo=archivo,
            estado='activo'
        )
        session.add(nuevo_mensaje)
        session.commit()

        # Enviar notificaciones si el foro es de tipo importante
        if foro.tipo_foro == 'importante':
            residentes = session.query(Usuario).filter(
                Usuario.tipo_usuario == 'RESIDENTE',
                Usuario.id_comunidad == foro.id_comunidad
            ).all()
            for residente in residentes:
                enviar_correo(residente.correo, 'Nuevo mensaje importante', contenido)
                enviar_notificacion(residente.id_usuario, contenido)

        return nuevo_mensaje
    finally:
        session.close()

def get_foro_mensajes(id_foro):
    session = get_session()
    try:
        mensajes = session.query(ForoMensaje).filter(ForoMensaje.id_foro == id_foro).all()
        return mensajes
    except NoResultFound:
        return {'error': 'No se encontraron mensajes para este foro'}
    finally:
        session.close()

# Ejemplo de uso de los nuevos métodos:
# nuevo_mensaje = create_foro_mensaje(id_usuario=1, id_foro=1, contenido='Este es un nuevo mensaje.')
# mensajes = get_foro_mensajes(id_foro=1)
# for mensaje in mensajes:
#     print(mensaje.to_dict())
