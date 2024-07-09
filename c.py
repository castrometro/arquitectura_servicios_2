import socket
import sys
from time import sleep


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

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket al puerto donde el bus está escuchando
bus_address = ('localhost', 5000)
print('Conectando a {} puerto {}'.format(*bus_address))
sock.connect(bus_address)

try:
    while True:
        # Enviar "Hello world" al servidor
        if input('¿Enviar "Hello world" al servidor? y/n: ') != 'y':
            break
        message = b'Hello world Lorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet solliciLorem ipsum dolor sit amet, consectetur adipiscing elit. In mauris dui, luctus eget quam at, laoreet sollicitudin justo. Quisque dapibus nulla vel ultricies sagittis. Mauris ex est, dictum ac ex non, ullamcorper tempus risus. Cras lacinia interdum magna quis varius. Proin non lectus arcu. Nullam odio nisi, congue ac mi at, pellentesque fermentum quam. Nam quam mi, convallis sed diam et, facilisis feugiat mauris. Integer pellentesque mauris placerat massa eleifend, eget fermentum ex euismod. Mauris augue nisl, accumsan eu nisl eu, dignissim rutrum erat. Pellentesque libero quam, finibus quis dictum at, accumsan eu ex. Etiam in tellus viverra, euismod ante a, pharetra ligula.'
        service_name = "servi"
        total_length = len(message) + len(service_name)
        total_length_str = f"{total_length:05d}"
        full_message = total_length_str.encode() + service_name.encode() + message
        print('Enviando {!r}'.format(full_message))
        send_in_chunks(sock, total_length, service_name, message)

        # Esperar la respuesta
        print("Esperando la transacción")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
        print("Verificando respuesta del servidor...")
        print('Recibido {!r}'.format(data))
finally:
    print('Cerrando socket')
    sock.close()