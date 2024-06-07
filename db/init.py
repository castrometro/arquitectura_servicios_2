from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# Crear el engine con la cadena de conexión adecuada
engine = create_engine('postgresql://finflow:finflow@localhost:5432/arquitectura_servicios')

# Crear todas las tablas definidas en las clases que heredan de Base
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()
