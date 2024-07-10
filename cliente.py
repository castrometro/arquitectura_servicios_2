import socket
import utils.data_transaction as dt
from utils.fx import *
from colorama import Fore, Style, init
import os
init(autoreset=True)

def mostrar_menu(opciones):
    print("\nSeleccione un servicio:")
    for key, value in opciones.items():
        print(f"{key}. {value['nombre']}")
    len_opciones = len(opciones)
    print(f"{len_opciones + 1}. Salir")

def connect_to_bus():
    # Crear un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conectar el socket al puerto donde el bus está escuchando
    bus_address = ('localhost', 5000)
    print('connecting to {} port {}'.format(*bus_address))
    sock.connect(bus_address)
    return sock

def menu_inicio():
    print("Bienvenido al sistema de gestión de comunidad.")
    print("Por favor, inicie sesión para continuar.")
    print("Conectando al bus....")
    sock = connect_to_bus()
    try:
        datos = cliente_login(sock)
        #print(datos)
        if 'error' in datos:
            #print datos[error]con color rojo siguiendo el formato: f"{Fore.GREEN}Bot: {molly_response}{Style.RESET_ALL}")
            print(f"{Fore.RED}Intente de nuevo{Style.RESET_ALL}")
            sleep(2)
            print("-----------------------------------")
            menu_inicio()
        else:
            #salida con color
            
            data_usuario = datos
            main_menu(data_usuario, data_usuario['tipo_usuario'], sock)
        # main_menu(data_usuario,data_usuario['tipo_usuario'],sock)
    finally:
        print('closing socket')
        sock.close()
    # main_menu(data_usuario,data_usuario['tipo_usuario'],sock)




def main_menu(data_usuario, tipo_usuario, sock):
    # os.system('clear')
    print(f"{Fore.YELLOW}-------------------------------------------{Style.RESET_ALL}")
    string = f"{Fore.LIGHTBLUE_EX}Bienvenido: {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX}{data_usuario['nombre']} {data_usuario['apellido_paterno']} {data_usuario['apellido_materno']}{Style.RESET_ALL}"
    print(string)
    print(f"{Fore.YELLOW}-------------------------------------------{Style.RESET_ALL}")


    opciones_admin_sistema = {
        '1': {'nombre': 'Gestión de Usuarios', 'funcion': gestion_usuarios},
        '2': {'nombre': 'Gestión de Comunidad', 'funcion': gestion_comunidad},
        '3': {'nombre': 'Gestión de Foros', 'funcion': gestion_foros},
        '4': {'nombre': 'CHAT', 'funcion': chat},
        '5': {'nombre': 'Gestión de Departamentos', 'funcion': gestion_departamento}
    }

    opciones_admin = {
        '1': {'nombre': 'Gestión de Usuarios', 'funcion': gestion_usuarios},
        '2': {'nombre': 'Gestión de Comunidad', 'funcion': gestion_comunidad},
        '3': {'nombre': 'Gestión de Foros', 'funcion': gestion_foros},
        '4': {'nombre': 'CHAT', 'funcion': chat},
        '5': {'nombre': 'Gestión de Departamentos', 'funcion': gestion_departamento}
    }

    opciones_residente = {
        '1': {'nombre': 'Gestión de Comunidad', 'funcion': gestion_comunidad},
        '2': {'nombre': 'Gestión de Foros', 'funcion': gestion_foros},
        '3': {'nombre': 'CHAT', 'funcion': chat},
        '4': {'nombre': 'Gestión de Departamentos', 'funcion': gestion_departamento},
    }

    opciones_conserje = {
        '1': {'nombre': 'Gestión de Comunidad', 'funcion': gestion_comunidad},
        '2': {'nombre': 'Gestión de Foros', 'funcion': gestion_foros},
        '3': {'nombre': 'CHAT', 'funcion': chat},
        '4': {'nombre': 'Gestión de Departamentos', 'funcion': gestion_departamento},
    }

    if tipo_usuario == 'ADMINISTRADOR_SISTEMA':
        opciones = opciones_admin_sistema
    elif tipo_usuario == 'ADMINISTRADOR':
        opciones = opciones_admin
    elif tipo_usuario == 'RESIDENTE':
        opciones = opciones_residente
    elif tipo_usuario == 'CONSERJE':
        opciones = opciones_conserje
    else:
        #tipo de usuario no reconocido con color rojo
        print("\033[1;31;40mTipo de usuario no reconocido\033[m")
        
        return
    
    while True:
        mostrar_menu(opciones)
        servicio = input("Ingrese el número del servicio: ")

        if servicio in opciones:
            sock = connect_to_bus()
            try:
                #linea qla brigia la de abajo aguante chatgpt
                opciones[servicio]['funcion'](sock,data_usuario)
            finally:
                print('closing socket')
                sock.close()
        elif servicio == '5':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.") 
       


if __name__ == "__main__":
    menu_inicio()
    # data_usuario = {'id_usuario': 1, 'nombre': 'Esteban', 'apellido_paterno': 'Paredes', 'apellido_materno': 'Waren', 'tipo_usuario': 'ADMINISTRADOR_SISTEMA'}
    # aux = connect_to_bus()
    # main_menu(data_usuario, data_usuario['tipo_usuario'], aux)

