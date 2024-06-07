import socket
import utils.data_transaction as dt
from utils.fx import *

def connect_to_bus():
    # Crear un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conectar el socket al puerto donde el bus está escuchando
    bus_address = ('localhost', 5000)
    print('connecting to {} port {}'.format(*bus_address))
    sock.connect(bus_address)
    return sock


def main_menu():
    while True:
        # Menú principal de selección de servicios
        print("\nSeleccione un servicio:")
        print("1. Gestión de Usuarios")
        print("2. Gestión de Comunidad")
        print("3. Gestion de Foros")
        print("4. Salir")
        
        servicio = input("Ingrese el número del servicio: ")
        
        if servicio == '1':
            sock = connect_to_bus()
            try:
                gestion_usuarios(sock)
            finally:
                print('closing socket')
                sock.close()
        
        elif servicio == '4':
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main_menu()
