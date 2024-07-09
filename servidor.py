
#message = b'Hello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHOLA

import socket
import sys

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket al puerto donde el bus está escuchando
bus_address = ('localhost', 5000)
print('Conectando a {} puerto {}'.format(*bus_address))
sock.connect(bus_address)

try:
    # Enviar datos
    message = b'00010sinitservi'
    print('Enviando {!r}'.format(message))
    sock.sendall(message)
    sinit = 1
    total_message = b''
    # largo_total = b''

    while True:
        # Esperar la transacción
        print("Esperando la transacción")
        amount_received = 0
        amount_expected = int(sock.recv(5))
        # service_name = sock.recv(5)
        # real_expected = sock.recv(5)
        # print(service_name, 'service name')
        # print(real_expected, 'real expected')
        # print(amount_expected, 'amount expected')
        message = b''
        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            name_function = data[0:5]
            if total_message == b'':
                largo_total = data[5:10]
                messaje = data
                total_message = messaje
            else:
                total_message += data[10:]

            amount_received += len(data)

        
        print ('-----------')
        print(message, 'message')
        print('-------------')
        # real_amout_expected = sock.recv(15)
        # substring = real_amout_expected[10:16]
        # print(substring, 'real amount expected')
        # real_amout_received = 0
        # print("Procesando...")
        # print('Recibido {!r}'.format(data))
        
        if sinit == 1:
            sinit = 0
            total_message = b''
            print('Respuesta sinit recibida')
        else:
            print (len(total_message), 'len total message')
            print (int(largo_total), 'largo total')
            print (len(total_message)-5 == int(largo_total) and total_message != b'')
            print(total_message, 'total message')
            if len(total_message)-5 == int(largo_total) and total_message != b'':
                print('ENTRE')
                messaje = b''
                total_message = total_message[10:]
                print('mensaje total:', total_message)
                total_message = b''
                print("Enviando respuesta")
                message = b'00013serviReceived'
                print('Enviando {!r}'.format(message))
                sock.sendall(message)
               
        
finally:
    print('Cerrando socket')
    sock.close()