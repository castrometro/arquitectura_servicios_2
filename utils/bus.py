import socket
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.data_transaction as dt

def run_service(process_data, name_service):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectar el socket al puerto donde el bus está escuchando
    bus_address = ('localhost', 5000)
    print('connecting to {} port {}'.format(*bus_address))
    sock.connect(bus_address)

    try:
        # Enviar datos
        transaction_data = dt.create_service_data(name_service)
        print('sending {!r}'.format(transaction_data))
        sock.sendall(transaction_data)
        sinit = 1

        while True:
            # Esperar la transacción
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            data = b''
            while amount_received < amount_expected:
                chunk = sock.recv(amount_expected - amount_received)
                if not chunk:
                    break
                data += chunk
                amount_received += len(chunk)

            print("Processing ...")
            print('received {!r}'.format(data))
            if sinit == 1:
                sinit = 0
                print('Received sinit answer')
            else:
                # Procesar los datos recibidos
                content = data.decode()
                print(f'Received raw content: {content}')
                # Eliminar la parte no JSON si es necesario
                content = content[5:]
                print(f'Received raw content sin servicio: {content}')

                # Convertir el contenido a JSON válido
                try:
                    # Reemplazar comillas simples por comillas dobles para que sea un JSON válido
                    content = content.replace("'", '"')
                    content_json = json.loads(content)
                    print(content_json, 'FORMAT DATA')
                    processed_data = process_data(content_json)
                    print(processed_data, 'PROCESSED DATA')
                    
                    # Preparar y enviar la respuesta
                    message = dt.create_transaction_data(name_service, processed_data)
                    print('sending {!r}'.format(message))
                    sock.sendall(message)
                except json.JSONDecodeError as e:
                    print(f'Error decoding JSON: {e}')
                    # Manejar el error, por ejemplo, enviar una respuesta de error o continuar con el siguiente mensaje

    finally:
        print('closing socket')
        sock.close()
