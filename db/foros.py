from modelos import Foro, get_session

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
    finally:
        session.close()

def get_foros():
    session = get_session()
    try:
        foros = session.query(Foro).all()
        return foros
    finally:
        session.close()

def delete_foro(id_foro):
    session = get_session()
    try:
        foro = session.query(Foro).filter(Foro.id_foro == id_foro).one()
        session.delete(foro)
        session.commit()
        return foro
    finally:
        session.close()

def update_foro(id_foro, id_comunidad, id_usuario, tipo_foro, estado_foro, tema_foro):
    session = get_session()
    try:
        foro = session.query(Foro).filter(Foro.id_foro == id_foro).one()
        foro.id_comunidad = id_comunidad
        foro.id_usuario = id_usuario
        foro.tipo_foro = tipo_foro
        foro.estado_foro = estado_foro
        foro.tema_foro = tema_foro
        session.commit()
        return foro
    finally:
        session.close()
