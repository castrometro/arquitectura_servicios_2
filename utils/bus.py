import socket
import sys
import os
import json
import signal
from time import sleep

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.data_transaction as dt

# Manejar la interrupción del teclado (Ctrl+C)
def signal_handler(sig, frame):
    print('Interrupción del teclado recibida. Cerrando el socket y saliendo...')
    if 'sock' in globals():
        sock.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def send_in_chunks(sock, total_length, service_name, message, chunk_size=500):
    total_length_str = f"{total_length:05d}"
    service_name_bytes = service_name.encode()
    sent_length = 0

    while sent_length < len(message):
        chunk_data = message[sent_length:sent_length + chunk_size - len(total_length_str) - len(service_name_bytes)]
        chunk = total_length_str.encode() + service_name_bytes + total_length_str.encode() + chunk_data
        print('Enviando {!r}'.format(chunk))
        sock.sendall(chunk)
        
        sleep(0.1)
        sent_length += len(chunk_data)


def run_service(process_data, name_service):
    global sock  # Declarar el socket como global para acceder a él en el manejador de señales
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
            print(f'amount_expected: {amount_expected}')

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
                    # message = dt.create_transaction_data(name_service, processed_data)
                    longitud_init = len(processed_data) + 10
                    send_in_chunks(sock, longitud_init, name_service, processed_data.encode(), chunk_size=500)
                    # print('sending {!r}'.format(message))
                    # sock.sendall(message)
                except json.JSONDecodeError as e:
                    print(f'Error decoding JSON: {e}')
                    # Manejar el error, por ejemplo, enviar una respuesta de error o continuar con el siguiente mensaje
                except KeyError as e:
                    print(f'KeyError: {e}')
                    # Manejar el error de clave faltante
                except Exception as e:
                    print(f'Unhandled exception: {e}')
                    # Manejar cualquier otra excepción

    finally:
        print('closing socket')
        sock.close()


