import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.foros import create_foro, get_foro, get_foros, delete_foro, update_foro
from utils.bus import run_service

def process_foro_service(data):
    action = data.get('action')
    if action == 'create':
        return create_foro(data['id_comunidad'], data['id_usuario'], data['tipo_foro'], data['estado_foro'], data['tema_foro']).to_dict()
    elif action == 'get':
        return get_foro(data['id_foro']).to_dict()
    elif action == 'list':
        return [foro.to_dict() for foro in get_foros()]
    elif action == 'delete':
        return delete_foro(data['id_foro']).to_dict()
    elif action == 'update':
        return update_foro(data['id_foro'], data['id_comunidad'], data['id_usuario'], data['tipo_foro'], data['estado_foro'], data['tema_foro']).to_dict()
    else:
        return {'error': 'Invalid action'}

if __name__ == "__main__":
    run_service(process_foro_service, 'foros')
