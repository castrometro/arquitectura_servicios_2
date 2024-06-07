import socket
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.bus as bus
from db.comunidad import create_comunidad, get_comunidades

# def process_data(data):
#     comunidad = create_comunidad('villa esperanza')
#     print(comunidad, data)
#     return json.dumps(comunidad.to_dict())
    
# bus.run_service(process_data, 'comun')

def process_comunidad_service(data):

    print(data, 'DATA QUE VIENE DEL CLIENTE')

    if(data['name_function'] == 'create'):
        comunidad = create_comunidad('villa esperanza')
        print(comunidad, data)
        return 'OK'
    if(data['name_function'] == 'all'):
        comunidades = get_comunidades()
        print(comunidades, data)
        return json.dumps([comunidad.to_dict() for comunidad in comunidades])
        # return json.dumps(comunidad.to_dict())
    
bus.run_service(process_comunidad_service, 'comun')

# def process_user_service(data):
#     json = {
#         "name_function": "create",
#         "data": {
#             "name": "comunidad",
#         }
#     }
#     if(json['name_function'] == 'create'):
#         comunidad = create_comunidad('villa esperanza')
#         print(comunidad, data)
#         return json.dumps(comunidad.to_dict())
#     if(json['name_function'] == 'all'):
#         comunidad = get_comunidades()
#         print(comunidad, data)
#         return json.dumps([comunidad.to_dict() for comunidad in comunidad])
#         # return json.dumps(comunidad.to_dict())
    
# bus.run_service(process_user_service, 'suser')


# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Conectar el socket al puerto donde el bus está escuchando
# bus_address = ('localhost', 5000)
# print('connecting to {} port {}'.format(*bus_address))
# sock.connect(bus_address)

# try:
#     # Enviar datos
#     transaction_data = dt.create_service_data("servi")
#     print('sending {!r}'.format(transaction_data))
#     sock.sendall(transaction_data)
#     sinit = 1

#     while True:
#         # Esperar la transacción
#         print("Waiting for transaction")
#         amount_received = 0
#         amount_expected = int(sock.recv(5))

#         while amount_received < amount_expected:
#             data = sock.recv(amount_expected - amount_received)
#             amount_received += len(data)
#         print("Procesing ...")
#         print('received {!r}'.format(data))
#         if sinit == 1:
#             sinit = 0
#             print('Received sinit answer')
#         else:
#             # Acá necesitamos que se pueda procesar data, en esta parte necesitamos poner código.


#             print("Send answer from comunidad")
#             message = b'00013serviReceived'
#             print('sending {!r}'.format(message))
#             sock.sendall(message)

# finally:
#     print('closing socket')
#     sock.close()
