from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv('C:/Users/David/Documents/Github/arquitectura_servicios/.env')

# Obtener las variables de entorno
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'arquitectura_servicios'

# Verificar que las variables de entorno se han cargado correctamente
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise Exception("Faltan variables de entorno requeridas")

print("Variables de entorno cargadas:")
print("DB_USER:", DB_USER)
print("DB_PASSWORD:", DB_PASSWORD)
print("DB_HOST:", DB_HOST)
print("DB_PORT:", DB_PORT)
print("DB_NAME:", DB_NAME)

user_types = ['RESIDENTE', 'CONSERJE', 'ADMINISTRADOR', 'ADMINISTRADOR_SISTEMA']

Base = declarative_base()

class Departamento(Base):
    __tablename__ = 'departamento'
    id_departamento = Column(Integer, primary_key=True)
    id_comunidad = Column(Integer, ForeignKey('comunidad.id_comunidad', onupdate='CASCADE', ondelete='SET NULL'))
    numero = Column(String(50))
    
    def to_dict(self):
        return {
            'id_departamento': self.id_departamento,
            'id_comunidad': self.id_comunidad,
            'numero': self.numero,
        }
    
class Comunidad(Base):
    __tablename__ = 'comunidad'
    id_comunidad = Column(Integer, primary_key=True)
    nombre_comunidad = Column(String(50))

    def to_dict(self):
        return {
            'id_comunidad': self.id_comunidad,
            'nombre_comunidad': self.nombre_comunidad
        }

class Usuario_Departamento(Base):
    __tablename__ = 'usuario_departamento'
    id_usuario_departamento = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario', onupdate='CASCADE', ondelete='SET NULL'))
    id_departamento = Column(Integer, ForeignKey('departamento.id_departamento', onupdate='CASCADE', ondelete='SET NULL'))
    
    def to_dict(self):
        return {
            'id_usuario_departamento': self.id_usuario_departamento,
            'id_usuario': self.id_usuario,
            'id_departamento': self.id_departamento
        }

class Foro(Base):
    __tablename__ = 'foro'
    id_foro = Column(Integer, primary_key=True)
    id_comunidad = Column(Integer, ForeignKey('comunidad.id_comunidad', onupdate='CASCADE', ondelete='SET NULL'))
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario', onupdate='CASCADE', ondelete='SET NULL'))
    tipo_foro = Column(String(50))
    estado_foro = Column(String(50))
    tema_foro = Column(String(50))
    
    def to_dict(self):
        return {
            'id_foro': self.id_foro,
            'id_comunidad': self.id_comunidad,
            'id_usuario': self.id_usuario,
            'tipo_foro': self.tipo_foro,
            'estado_foro': self.estado_foro,
            'tema_foro': self.tema_foro
        }

class Usuario(Base):
    __tablename__ = 'usuario'
    id_comunidad = Column(Integer, ForeignKey('comunidad.id_comunidad', onupdate='CASCADE', ondelete='SET NULL'))
    id_departamento = Column(Integer, ForeignKey('departamento.id_departamento', onupdate='CASCADE', ondelete='SET NULL'))
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    rut = Column(String(50))
    tipo_usuario = Column(String(50))
    correo = Column(String(100))
    fono = Column(String(20))
    nombre = Column(String(50))
    apellido_paterno = Column(String(50))
    apellido_materno = Column(String(50))
    estado_cuenta = Column(String(50), default='pendiente')  # estado predeterminado
    contrasena = Column(String(255))
    privacidad = Column(String(10), default='publica')  # Nueva columna para la privacidad
    
    def to_dict(self):
        return {
            'id_comunidad': self.id_comunidad,
            'id_departamento:': self.id_departamento,
            'id_usuario': self.id_usuario,
            'rut': self.rut,
            'tipo_usuario': self.tipo_usuario,
            'correo': self.correo,
            'fono': self.fono,
            'nombre': self.nombre,
            'apellido_paterno': self.apellido_paterno,
            'apellido_materno': self.apellido_materno,
            'estado_cuenta': self.estado_cuenta,
            'privacidad': self.privacidad
        }
    
    def to_dict_private(self):
        return {
            'id_usuario': self.id_usuario,
            'rut': self.rut,
            'tipo_usuario': self.tipo_usuario,
            'correo': self.correo,
            'fono': self.fono,
            'nombre': self.nombre,
            'apellido_paterno': self.apellido_paterno,
            'apellido_materno': self.apellido_materno,
            'estado_cuenta': self.estado_cuenta,
            'contrasena': self.contrasena,
            'privacidad': self.privacidad
        }

class Chat(Base):
    __tablename__ = 'chat'
    id_chat = Column(Integer, primary_key=True)
    id_usuario_remitente = Column(Integer, ForeignKey('usuario.id_usuario', onupdate='CASCADE', ondelete='SET NULL'))
    id_usuario_receptor = Column(Integer, ForeignKey('usuario.id_usuario', onupdate='CASCADE', ondelete='SET NULL'))
    fecha_chat = Column(DateTime)
    
    def to_dict(self):
        return {
            'id_chat': self.id_chat,
            'id_usuario_remitente': self.id_usuario_remitente,
            'id_usuario_receptor': self.id_usuario_receptor,
            # 'fecha_chat': self.fecha_chat
        }

class ChatMensaje(Base):
    __tablename__ = 'chat_mensaje'
    id_chat_mensaje = Column(Integer, primary_key=True)
    contenido = Column(Text)
    archivo = Column(String(100))
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario', onupdate='CASCADE', ondelete='SET NULL'))
    id_chat = Column(Integer, ForeignKey('chat.id_chat', onupdate='CASCADE', ondelete='SET NULL'))
    fecha_mensaje = Column(DateTime)
    
    def to_dict(self):
        return {
            'id_chat_mensaje': self.id_chat_mensaje,
            'contenido': self.contenido,
            'archivo': self.archivo,
            'id_usuario': self.id_usuario,
            'id_chat': self.id_chat,
            # 'fecha_mensaje': self.fecha_mensaje
        }

class Notificacion(Base):
    __tablename__ = 'notificacion'
    id_notificacion = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    hora = Column(DateTime)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario', onupdate='CASCADE', ondelete='SET NULL'))
    id_foro = Column(Integer, ForeignKey('foro.id_foro', onupdate='CASCADE', ondelete='SET NULL'))
    
    def to_dict(self):
        return {
            'id_notificacion': self.id_notificacion,
            'fecha': self.fecha,
            'hora': self.hora,
            'id_usuario': self.id_usuario,
            'id_foro': self.id_foro
        }

class UsuarioSuspendido(Base):
    __tablename__ = 'usuario_suspendido'
    id_usuario_suspendido = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario', onupdate='CASCADE', ondelete='SET NULL'))
    id_foro = Column(Integer, ForeignKey('foro.id_foro', onupdate='CASCADE', ondelete='SET NULL'))
    duracion = Column(Integer)
    fecha_moderacion = Column(DateTime)
    estado = Column(String(50))
    razon = Column(String(250))
    
    def to_dict(self):
        return {
            'id_usuario_suspendido': self.id_usuario_suspendido,
            'id_usuario': self.id_usuario,
            'id_foro': self.id_foro,
            'duracion': self.duracion,
            'fecha_moderacion': self.fecha_moderacion,
            'estado': self.estado,
            'razon': self.razon
        }

class ForoMensaje(Base):
    __tablename__ = 'foro_mensaje'
    id_foro_mensaje = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario', onupdate='CASCADE', ondelete='SET NULL'))
    id_foro = Column(Integer, ForeignKey('foro.id_foro', onupdate='CASCADE', ondelete='SET NULL'))
    fecha = Column(DateTime)
    hora = Column(DateTime)
    contenido = Column(Text)
    archivo = Column(String(100))
    estado = Column(String(50))
    
    def to_dict(self):
        return {
            'id_foro_mensaje': self.id_foro_mensaje,
            'id_usuario': self.id_usuario,
            'id_foro': self.id_foro,
            'contenido': self.contenido,
            'archivo': self.archivo,
            'estado': self.estado
        }

def get_session():
    # Configuración de la base de datos
    DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(DATABASE_URL)

    # Crear todas las tablas
    Base.metadata.create_all(engine)

    # Crear una sesión
    Session = sessionmaker(bind=engine)
    """Crea y retorna una nueva sesión."""
    return Session()
    
def get_foro(id_foro):
    session = get_session()
    try:
        foro = session.query(Foro).filter(Foro.id_foro == id_foro).one_or_none()
        return foro
    finally:
        session.close()

def get_user(id_usuario):
    session = get_session()
    try:
        user = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).one()
        return user
    finally:
        session.close()

# Comprobar que la variable de entorno se cargue correctamente
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)

# Crear todas las tablas
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()
