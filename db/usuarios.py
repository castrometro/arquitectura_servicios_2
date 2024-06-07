import sys
import os
import bcrypt
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
    finally:
        session.close()

def get_usuarios():
    session = get_session()
    try:
        usuarios = session.query(Usuario).all()
        return usuarios
    finally:
        session.close()

def get_usuario_by_rut(rut):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.rut == rut).one()
        return usuario
    finally:
        session.close()

def delete_usuario(id_usuario):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).one()
        session.delete(usuario)
        session.commit()
        return usuario
    finally:
        session.close()

def update_usuario(id_usuario, rut, tipo_usuario, correo, fono, nombre, apellido_paterno, apellido_materno, estado_cuenta):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).one()
        usuario.rut = rut
        usuario.tipo_usuario = tipo_usuario
        usuario.correo = correo
        usuario.fono = fono
        usuario.nombre = nombre
        usuario.apellido_paterno = apellido_paterno
        usuario.apellido_materno = apellido_materno
        usuario.estado_cuenta = estado_cuenta
        session.commit()
        return usuario
    finally:
        session.close()

def login_usuario(rut, contrasena):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.rut == rut).one()
        if bcrypt.checkpw(contrasena.encode('utf-8'), usuario.contrasena.encode('utf-8')):
            return usuario
        else:
            return None
    finally:
        session.close()

def register_usuario(rut, tipo_usuario, correo, fono, nombre, apellido_paterno, apellido_materno, estado_cuenta, contrasena):
    return create_usuario(rut, tipo_usuario, correo, fono, nombre, apellido_paterno, apellido_materno, estado_cuenta, contrasena)
