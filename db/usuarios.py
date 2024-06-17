import sys
import os
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.modelos import Usuario, get_session

def create_usuario(rut, tipo_usuario, correo, fono, nombre, apellido_paterno, apellido_materno, estado_cuenta, contrasena):
    session = get_session()
    try:
        hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        usuario = Usuario(
            rut=rut,
            tipo_usuario=tipo_usuario,
            correo=correo,
            fono=fono,
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            estado_cuenta=estado_cuenta,
            contrasena=hashed_password
        )
        session.add(usuario)
        session.commit()
        return usuario
    finally:
        session.close()

def get_usuario(id_usuario):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).one()
        return usuario
    except NoResultFound:
        return {'error': 'Usuario no encontrado'}
    finally:
        session.close()

def get_usuarios():
    session = get_session()
    try:
        usuarios = session.query(Usuario).all()
        return usuarios
    except NoResultFound:
        return {'error': 'No hay usuarios'}
    finally:
        session.close()

def get_usuario_by_id(id):
    session = get_session()
    try:
        session.query(Usuario).filter(Usuario.id_usuario == id).one()
        return True
    except NoResultFound:
            return False
    finally:
        session.close()


def get_usuario_by_rut(rut):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.rut == rut).one()
        return usuario
    except NoResultFound:
            return {'error': 'Usuario no encontrado'}
    finally:
        session.close()

def delete_usuario(id_usuario):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).one()
        session.delete(usuario)
        session.commit()
        return usuario
    except NoResultFound:
            return {'error': 'Usuario no encontrado'}
    finally:
        session.close()


def update_usuario(id_usuario, rut, tipo_usuario, correo, fono, nombre, apellido_paterno, apellido_materno, estado_cuenta):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).one()
        
        # Solo actualizar los campos que no son 0
        if rut != '0':
            usuario.rut = rut
        if tipo_usuario != '0':
            usuario.tipo_usuario = tipo_usuario
        if correo != '0':
            usuario.correo = correo
        if fono != '0':
            usuario.fono = fono
        if nombre != '0':
            usuario.nombre = nombre
        if apellido_paterno != '0':
            usuario.apellido_paterno = apellido_paterno
        if apellido_materno != '0':
            usuario.apellido_materno = apellido_materno
        if estado_cuenta != '0':
            usuario.estado_cuenta = estado_cuenta
        
        session.commit()
        return usuario
    except NoResultFound:
        return {'error': 'Usuario no encontrado'}
    finally:
        session.close()



def login_usuario(rut, contrasena):
    session = get_session()
    try:
        try:
            usuario = session.query(Usuario).filter(Usuario.rut == rut).one()
        except NoResultFound:
            return {'error': 'Usuario no encontrado'}
        # Ver si el usuario existe
        if bcrypt.checkpw(contrasena.encode('utf-8'), usuario.contrasena.encode('utf-8')):
            if usuario.estado_cuenta != 'pendiente':
                return usuario
            else:
                return {'error': 'Usuario pendiente de aprobacion'}
        else:
            return {'error': 'Credenciales invalidas'}
    finally:
        session.close()


def register_usuario(rut, tipo_usuario, correo, fono, nombre, apellido_paterno, apellido_materno, estado_cuenta, contrasena):
    # estado de cuenta predeterminado como "pendiente"
    estado_cuenta = 'pendiente'
    return create_usuario(rut, tipo_usuario, correo, fono, nombre, apellido_paterno, apellido_materno, estado_cuenta, contrasena)
