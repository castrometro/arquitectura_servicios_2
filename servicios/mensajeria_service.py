import sys
import os
import json
import logging
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.bus as bus
from db.modelos import get_foro, get_user, get_session, UsuarioSuspendido
from db.mensajes import create_foro_message

logging.basicConfig(filename='mensajeria_service.log', level=logging.INFO, format='%(asctime)s %(message)s')

def is_user_suspended(user_id, foro_id):
    session = get_session()
    try:
        suspension = session.query(UsuarioSuspendido).filter_by(
            id_usuario=user_id,
            id_foro=foro_id,
            estado='activo'
        ).first()
        if suspension:
            duracion = timedelta(days=suspension.duracion)
            fin_suspension = suspension.fecha_moderacion + duracion
            if datetime.now() <= fin_suspension:
                return True
        return False
    finally:
        session.close()

def handle_create_message(data):
    required_fields = ['id_usuario', 'id_foro', 'contenido']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return json.dumps({'error': 'Missing required fields', 'missing_fields': missing_fields})
    
    user_id = data['id_usuario']
    foro_id = data['id_foro']
    message_content = data['contenido']
    
    foro = get_foro(foro_id)
    if not foro:
        return json.dumps({"status": "error", "message": "Foro no encontrado"})
    
    user = get_user(user_id)
    if not user:
        return json.dumps({"status": "error", "message": "Usuario no encontrado"})

    if user.tipo_usuario != 'administrador':
        if foro.tipo_foro == 'lectura':
            return json.dumps({"status": "error", "message": "No tienes permiso para escribir en este foro, solo lectura"})
        
        if is_user_suspended(user_id, foro_id):
            return json.dumps({"status": "error", "message": "No tienes permiso para escribir en este foro, estás suspendido"})
    
    new_message_data = create_foro_message(user_id, foro_id, message_content)
    return json.dumps({"status": "success", "message": "Mensaje publicado con éxito", "data": new_message_data})

def process_msnforo_service(data):
    name_function = data['name_function']
    data = data['data']

    if name_function == 'create_message':
        return handle_create_message(data)
    else:
        return json.dumps({'error': 'Invalid function name'})

if __name__ == "__main__":
    logging.info('Mensajeria service started')
    bus.run_service(process_msnforo_service, 'msngr')
