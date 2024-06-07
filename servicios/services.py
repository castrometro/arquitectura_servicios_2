import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.bus as bus

from user_service import process_user_service
from comunidad_service import process_comunidad_service

    
if __name__ == "__main__":
    bus.run_service(process_comunidad_service, 'comun')
    bus.run_service(process_user_service, 'suser')

