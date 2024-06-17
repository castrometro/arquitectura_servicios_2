import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.modelos import ForoMensaje, get_session

def create_foro_message(id_usuario, id_foro, contenido):
    session = get_session()
    try:
        new_message = ForoMensaje(
            id_usuario=id_usuario,
            id_foro=id_foro,
            fecha=datetime.utcnow(),
            contenido=contenido
        )
        session.add(new_message)
        session.commit()
        # Acceder a los atributos antes de cerrar la sesión
        message_data = {
            "id_foro_mensaje": new_message.id_foro_mensaje,
            "id_usuario": new_message.id_usuario,
            "id_foro": new_message.id_foro,
            "fecha": new_message.fecha.isoformat(),  # Convertir a cadena
            "contenido": new_message.contenido
        }
        return message_data
    finally:
        session.close()
