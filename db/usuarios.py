import sys
import os
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.modelos import Usuario,Comunidad, get_session

def create_usuario(id_comunidad, rut, tipo_usuario, correo, fono, nombre, apellido_paterno, apellido_materno, estado_cuenta, contrasena):
    session = get_session()
    if session.query(Usuario).filter(Usuario.rut == rut).count() > 0:
        return {'error': 'Usuario ya existe'}
    #verificar comunidad q existe
    if session.query(Comunidad).filter(Comunidad.id_comunidad == id_comunidad).count() == 0:
        return {'error': 'Comunidad no existe'}
    try:
        hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        usuario = Usuario(
            id_comunidad=id_comunidad,
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
        return {'message': 'Usuario creado con exito'}
    finally:
        session.close()

def get_usuario(id_usuario):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).one()
        return usuario.to_dict()
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

def get_usuario_by_comunidad(comunidad):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id_comunidad == comunidad).all()
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
        
        # Solo actualizar los campos que no son vacios
        if rut != '':
            usuario.rut = rut
        if tipo_usuario != '':
            usuario.tipo_usuario = tipo_usuario
        if correo != '':
            usuario.correo = correo
        if fono != '':
            usuario.fono = fono
        if nombre != '':
            usuario.nombre = nombre
        if apellido_paterno != '':
            usuario.apellido_paterno = apellido_paterno
        if apellido_materno != '':
            usuario.apellido_materno = apellido_materno
        if estado_cuenta != '':
            usuario.estado_cuenta = estado_cuenta
        
        session.commit()
        return usuario
    except NoResultFound:
        return {'error': 'Usuario no encontrado'}
    finally:
        session.close()

#----------
def update_privacidad_usuario(id_usuario, privacidad):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).one()
        usuario.privacidad = privacidad
        session.commit()
        return usuario
    finally:
        session.close()

def get_usuario_visible(id_usuario, requestor_id):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).one()
        requestor = session.query(Usuario).filter(Usuario.id_usuario == requestor_id).one()

        if usuario.privacidad == 'publica' or usuario.id_usuario == requestor.id_usuario or requestor.tipo_usuario in ['ADMINISTRADOR', 'ADMINISTRADOR_SISTEMA']:
            return usuario.to_dict()
        else:
            # Return limited information
            return {
                'id_usuario': usuario.id_usuario,
                'rut': usuario.rut,
                'nombre': usuario.nombre,
                'apellido_paterno': usuario.apellido_paterno,
                'apellido_materno': usuario.apellido_materno
            }
    finally:
        session.close()
#-------------

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
