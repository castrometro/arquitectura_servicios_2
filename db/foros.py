import sys
import os
from sqlalchemy.orm.exc import NoResultFound
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.modelos import Foro, get_session

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
        foro = session.query(Foro).filter(Foro.id_usuario == data['id_usuario'], Foro.tipo_foro == data['tipo_foro'], Foro.estado_foro == data['estado_foro'], Foro.tema_foro == data['tema_foro']).one()
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

def update_foro(id_foro,tipo_foro, estado_foro, tema_foro):
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
