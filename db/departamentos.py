import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.modelos import Departamento, Usuario_Departamento, Usuario, get_session, Comunidad

# Funciones de Departamento
def create_departamento(id_comunidad, numero):
    session = get_session()
    try:
        departamento = Departamento(id_comunidad=id_comunidad, numero=numero)
        session.add(departamento)
        session.commit()
        return {'message': 'Departamento creado con exito'}
    finally:
        session.close()

def delete_departamento(id_departamento):
    session = get_session()
    try:
        departamento = session.query(Departamento).filter(Departamento.id_departamento == id_departamento).one()
        session.delete(departamento)
        session.commit()
        return 'OK'
    finally:
        session.close()

def update_departamento(id_departamento, numero=None ):
    session = get_session()
    try:
        departamento = session.query(Departamento).filter(Departamento.id_departamento == id_departamento).one()
        if numero:
            departamento.numero = numero
        session.commit()
        return departamento
    finally:
        session.close()

# Funciones de Usuario en Departamento
def add_usuario_to_departamento(id_usuario, id_departamento):
    session = get_session()
    try:
        usuario_departamento = Usuario_Departamento(id_usuario=id_usuario, id_departamento=id_departamento)
        session.add(usuario_departamento)
        session.commit()
        return usuario_departamento
    finally:
        session.close()

def remove_usuario_from_departamento(id_usuario, id_departamento):
    session = get_session()
    try:
        usuario_departamento = session.query(Usuario_Departamento).filter(
            Usuario_Departamento.id_usuario == id_usuario,
            Usuario_Departamento.id_departamento == id_departamento
        ).one()
        session.delete(usuario_departamento)
        session.commit()
        return usuario_departamento
    finally:
        session.close()

def get_usuarios_by_departamento(id_departamento):
    session = get_session()
    try:
        usuarios_departamento = session.query(Usuario_Departamento).filter(
            Usuario_Departamento.id_departamento == id_departamento
        ).all()
        usuarios = [session.query(Usuario).filter(Usuario.id_usuario == ud.id_usuario).one().to_dict() for ud in usuarios_departamento]
        return usuarios
    finally:
        session.close()

def validate_usuario(id_usuario):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).one()
        usuario.estado_cuenta = 'validado'
        session.commit()
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

def update_usuario(id_usuario, rut=None, tipo_usuario=None, correo=None, fono=None, nombre=None, apellido_paterno=None, apellido_materno=None, estado_cuenta=None, contrasena=None):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).one()
        if rut:
            usuario.rut = rut
        if tipo_usuario:
            usuario.tipo_usuario = tipo_usuario
        if correo:
            usuario.correo = correo
        if fono:
            usuario.fono = fono
        if nombre:
            usuario.nombre = nombre
        if apellido_paterno:
            usuario.apellido_paterno = apellido_paterno
        if apellido_materno:
            usuario.apellido_materno = apellido_materno
        if estado_cuenta:
            usuario.estado_cuenta = estado_cuenta
        if contrasena:
            usuario.contrasena = contrasena
        session.commit()
        return usuario
    finally:
        session.close()
