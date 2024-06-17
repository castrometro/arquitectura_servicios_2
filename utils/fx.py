import socket
import json as js
import sys
from time import sleep
import utils.data_transaction as dt


def handle_data(data, clase):
    decoded_data = data.decode('utf-8',errors = 'ignore')
    
    prefix = clase + 'OK'
    
    if len(decoded_data) > len(prefix):
        json_str = decoded_data[len(prefix):]
        try:
            data_dict = js.loads(json_str)
        except js.JSONDecodeError:
            print("OK, no hay json")
            return {}
        
        for key, value in data_dict.items():
            print(key, ":", value)
        return data_dict
    else:
        print("No hay datos después de 'OK'")
        return {}

def transaction(sock, clase, json):
    message = dt.create_transaction(clase, json)
    print('sending {!r}'.format(message))
    sock.sendall(message)

    # Esperar la respuesta
    print("...Esperando transaccion")
    amount_received = 0
    amount_expected = int(sock.recv(5))

    while amount_received < amount_expected:
        data = sock.recv(amount_expected - amount_received)
        amount_received += len(data)
    print("Esperando Respuesta ...")
    if clase == "suser":
        return handle_data(data, "suser")
    elif clase == "comun":
        return handle_data(data, "comun")
    elif clase == "foros":
        return handle_data(data, "foros")
    else:
        print("Clase no encontrada")
        print ('received {!r}'.format(data))


def cliente_login(sock):
    rut = input("Ingrese el rut del usuario: ")
    contrasena = input("Ingrese la contraseña del usuario: ")
    # Transformar datos a DATA del JSON
    json = {
        "name_function": "login",
            "data": {
                "rut": rut,
                "contrasena": contrasena
            }
    }

    print ("------------------")
    data_dict = transaction(sock, "suser", json)
    return data_dict
    #return estado, usuario
    

def gestion_usuarios(sock, data_usuario):
    clase = "suser"
    tipo_usuario = data_usuario['tipo_usuario']

    # Definir las opciones del menú para cada tipo de usuario
    menus = {
        'RESIDENTE': [
            "Ver Usuario"
        ],
        'CONSERJE': [
            "Listar usuarios",
            "Ver Usuario"
        ],
        'ADMINISTRADOR': [
            "Listar usuarios",
            "Actualizar usuario",
            "Ver Usuario"
        ],
        'ADMINISTRADOR_SISTEMA': [
            "Listar usuarios",
            "Actualizar usuario",
            "Eliminar usuario",
            "Crear usuario",
            "Loguear usuario",
            "Ver Usuario"
        ]
    }

    # Mapear las opciones del menú a las acciones correspondientes
    menu_actions = {
        "Listar usuarios": "1",
        "Actualizar usuario": "2",
        "Eliminar usuario": "3",
        "Crear usuario": "4",
        "Loguear usuario": "5",
        "Ver Usuario": "6",
        "Volver al menú principal": "7"
    }

    while True:
        # Mostrar las opciones del menú según el tipo de usuario
        print("\nSeleccione una operación de Gestión de Usuarios:")
        opciones_disponibles = menus[tipo_usuario]
        for i, opcion in enumerate(opciones_disponibles, start=1):
            print(f"{i}. {opcion}")

        print(f"{len(opciones_disponibles) + 1}. Volver al menú principal")

        opcion = input("Ingrese el número de la operación: ")

        if opcion == str(len(opciones_disponibles) + 1):
            break
        elif opcion.isdigit() and 1 <= int(opcion) <= len(opciones_disponibles):
            accion = opciones_disponibles[int(opcion) - 1]

            if accion == "Listar usuarios":
                json = {
                    "name_function": "all",
                    "data": {
                         "name": "usuarios",
                    }
                }
                transaction(sock, clase, json)

            elif accion == "Actualizar usuario":
                id_usuario = input("Ingrese el ID del usuario a actualizar: ")
                json = {
                    "name_function": "get",
                    "data": {
                        "id_usuario": id_usuario
                    }
                }
                response = transaction(sock, clase, json)
                if 'error' not in response:
                    print('Usuario Encontrado')
                    rut_usuario = input("Ingrese el nuevo rut del usuario o '0' para mantener el actual:") or response['rut']
                    user_type = input("Ingrese el nuevo tipo del usuario o '0' para mantener el actual:") or response['tipo_usuario']
                    correo = input("Ingrese el nuevo email del usuario o '0' para mantener el actual:") or response['correo']
                    fono = input("Ingrese el nuevo fono del usuario o '0' para mantener el actual:") or response['fono']
                    nombre = input("Ingrese el nuevo nombre del usuario o '0' para mantener el actual:") or response['nombre']
                    apellido_paterno = input("Ingrese el nuevo apellido paterno del usuario o '0' para mantener el actual:") or response['apellido_paterno']
                    apellido_materno = input("Ingrese el nuevo apellido materno del usuario o '0' para mantener el actual:") or response['apellido_materno']
                    estado_cuenta = input("Ingrese el nuevo estado de cuenta del usuario o '0' para mantener el actual:") or response['estado_cuenta']

                    json = {
                        "name_function": "update",
                        "data": {
                            "id_usuario": id_usuario,
                            "rut": rut_usuario,
                            "tipo_usuario": user_type,
                            "correo": correo,
                            "fono": fono,
                            "nombre": nombre,
                            "apellido_paterno": apellido_paterno,
                            "apellido_materno": apellido_materno,
                            "estado_cuenta": estado_cuenta
                        }
                    }
                    transaction(sock, clase, json)
                else:
                    print('Usuario No existe')

            elif accion == "Eliminar usuario":
                user_id = input("Ingrese el ID del usuario a eliminar: ")
                json = {
                    "name_function": "delete",
                    "data": {
                        "id_usuario": user_id,
                    }
                }
                transaction(sock, clase, json)

            elif accion == "Crear usuario":
                id_usuario = input("Ingrese el id del nuevo usuario: ")
                rut = input("Ingrese el rut del nuevo usuario: ")
                tipo_usuario = input("Ingrese el tipo del nuevo usuario: ")
                correo = input("Ingrese el email del nuevo usuario: ")
                fono = input("Ingrese el fono del nuevo usuario: ")
                nombre = input("Ingrese el nombre del nuevo usuario: ")
                apellido_paterno = input("Ingrese el ap_p del nuevo usuario: ")
                apellido_materno = input("Ingrese elap_m del nuevo usuario: ")
                estado_cuenta = input("Ingrese el estado del nuevo usuario: ")
                contrasena = input("Ingrese la contraseña del nuevo usuario: ")
                json = {
                    "name_function": "create",
                    "data": {
                        "id_usuario": id_usuario,
                        "rut": rut,
                        "tipo_usuario": tipo_usuario,
                        "correo": correo,
                        "fono": fono,
                        "nombre": nombre,
                        "apellido_paterno": apellido_paterno,
                        "apellido_materno": apellido_materno,
                        "estado_cuenta": estado_cuenta,
                        "contrasena": contrasena
                    }
                }
                transaction(sock, clase, json)

            elif accion == "Loguear usuario":
                cliente_login(sock)

            elif accion == "Ver Usuario":
                user_id = input("Ingrese el ID del usuario a ver: ")
                json = {
                    "name_function": "get",
                    "data": {
                        "id_usuario": user_id,
                    }
                }
                transaction(sock, clase, json)
        else:
            print("Opción no válida o no tiene acceso a esta opción. Inténtelo de nuevo.")

def gestion_comunidad(sock, data_usuario):
    clase = "comun"
    tipo_usuario = data_usuario['tipo_usuario']

    # Definir las opciones del menú para cada tipo de usuario
    menus = {
        'RESIDENTE': [
            "Ver Comunidad",
            "Mostrar Comunidades"
        ],
        'CONSERJE': [
            "Ver Comunidad",
            "Mostrar Comunidades"
        ],
        'ADMINISTRADOR': [
            "Crear Comunidad",
            "Ver Comunidad",
            "Mostrar Comunidades",
            "Actualizar Comunidad",
            "Eliminar Comunidad"
        ],
        'ADMINISTRADOR_SISTEMA': [
            "Crear Comunidad",
            "Ver Comunidad",
            "Mostrar Comunidades",
            "Actualizar Comunidad",
            "Eliminar Comunidad"
        ]
    }

    while True:
        # Mostrar las opciones del menú según el tipo de usuario
        print("\nSeleccione una operación de Gestión de Comunidad:")
        opciones_disponibles = menus[tipo_usuario]
        for i, opcion in enumerate(opciones_disponibles, start=1):
            print(f"{i}. {opcion}")

        print(f"{len(opciones_disponibles) + 1}. Volver al menú principal")

        opcion = input("Ingrese el número de la operación: ")

        if opcion == str(len(opciones_disponibles) + 1):
            break
        elif opcion.isdigit() and 1 <= int(opcion) <= len(opciones_disponibles):
            accion = opciones_disponibles[int(opcion) - 1]

            if accion == "Crear Comunidad":
                comunidad = input("Ingrese el nombre de la nueva comunidad: ")
                json = {
                    "name_function": "create",
                    "data": {
                        "nombre_comunidad": comunidad,
                    }
                }
                transaction(sock, clase, json)

            elif accion == "Ver Comunidad":
                comunidad_id = input("Ingrese el ID de la comunidad a ver: ")
                json = {
                    "name_function": "get",
                    "data": {
                        "id_comunidad": comunidad_id,
                    }
                }
                transaction(sock, clase, json)

            elif accion == "Mostrar Comunidades":
                json = {
                    "name_function": "all",
                    "data": {
                        "name": "comunidad",
                    }
                }
                transaction(sock, clase, json)

            elif accion == "Actualizar Comunidad":
                id_comunidad = input("Ingrese el ID de la comunidad a actualizar: ")
                json = {
                    "name_function": "get",
                    "data": {
                        "id_comunidad": id_comunidad,
                    }
                }
                response = transaction(sock, clase, json)
                if 'error' not in response:
                    print('Comunidad Encontrada')
                    nombre_comunidad = input("Ingrese el nuevo nombre de la comunidad o '0' para mantener el actual:") or response['nombre_comunidad']
            
                    json = {
                        "name_function": "update",
                        "data": {
                            "id_comunidad": id_comunidad,
                            "nombre_comunidad": nombre_comunidad,
                        }
                    }
                    transaction(sock, clase, json)
                else:
                    print('Comunidad No existe')

            elif accion == "Eliminar Comunidad":
                comunidad_id = input("Ingrese el ID de la comunidad a eliminar: ")
                json = {
                    "name_function": "delete",
                    "data": {
                        "id_comunidad": comunidad_id,
                    }
                }
                transaction(sock, clase, json)
        else:
            print("Opción no válida o no tiene acceso a esta opción. Inténtelo de nuevo.")

def gestion_foros(sock, data_usuario):
    clase = "foros"
    tipo_usuario = data_usuario['tipo_usuario']

    # Definir las opciones del menú para cada tipo de usuario
    menus = {
        'RESIDENTE': [
            "Ver Foro",
            "Mostrar Foros"
        ],
        'CONSERJE': [
            "Ver Foro",
            "Mostrar Foros"
        ],
        'ADMINISTRADOR': [
            "Crear Foro",
            "Ver Foro",
            "Mostrar Foros",
            "Actualizar Foro",
            "Eliminar Foro"
        ],
        'ADMINISTRADOR_SISTEMA': [
            "Crear Foro",
            "Ver Foro",
            "Mostrar Foros",
            "Actualizar Foro",
            "Eliminar Foro"
        ]
    }

    while True:
        # Mostrar las opciones del menú según el tipo de usuario
        print("\nSeleccione una operación de Gestión de Foros:")
        opciones_disponibles = menus[tipo_usuario]
        for i, opcion in enumerate(opciones_disponibles, start=1):
            print(f"{i}. {opcion}")

        print(f"{len(opciones_disponibles) + 1}. Volver al menú principal")

        opcion = input("Ingrese el número de la operación: ")

        if opcion == str(len(opciones_disponibles) + 1):
            break
        elif opcion.isdigit() and 1 <= int(opcion) <= len(opciones_disponibles):
            accion = opciones_disponibles[int(opcion) - 1]

            if accion == "Crear Foro":
                id_comunidad = input("Ingrese el id de la comunidad del nuevo foro: ")
                id_usuario = input("Ingrese el id del usuario del nuevo foro: ")
                tipo_foro = input("Ingrese el tipo del nuevo foro: ")
                estado_foro = input("Ingrese el estado del nuevo foro: ")
                tema_foro = input("Ingrese el tema del nuevo foro: ")
                json = {
                    "name_function": "create",
                    "data": {
                        "id_comunidad": id_comunidad,
                        "id_usuario": id_usuario,
                        "tipo_foro": tipo_foro,
                        "estado_foro": estado_foro,
                        "tema_foro": tema_foro
                    }
                }
                transaction(sock, clase, json)

            elif accion == "Ver Foro":
                foro_id = input("Ingrese el ID del foro a ver: ")
                json = {
                    "name_function": "get",
                    "data": {
                        "id_foro": foro_id,
                    }
                }
                transaction(sock, clase, json)

            elif accion == "Mostrar Foros":
                json = {
                    "name_function": "all",
                    "data": {
                        "id_foro": "foros",
                    }
                }
                transaction(sock, clase, json)

            elif accion == "Actualizar Foro":
                id_foro = input("Ingrese el ID del foro a actualizar: ")
                json = {
                    "name_function": "get",
                    "data": {
                        "id_foro": id_foro,
                    }
                }
                response = transaction(sock, clase, json)
                if 'error' not in response:
                    print('Foro Encontrado')
                    tipo_foro = input("Ingrese el nuevo tipo del foro o '0' para mantener el actual:") or response['tipo_foro']
                    estado_foro = input("Ingrese el nuevo estado del foro o '0' para mantener el actual:") or response['estado_foro']
                    tema_foro = input("Ingrese el nuevo tema del foro o '0' para mantener el actual:") or response['tema_foro']

                    json = {
                        "name_function": "update",
                        "data": {
                            "id_foro": id_foro,
                            "tipo_foro": tipo_foro,
                            "estado_foro": estado_foro,
                            "tema_foro": tema_foro,
                        }
                    }
                    transaction(sock, clase, json)
                else:
                    print('Foro No existe')

            elif accion == "Eliminar Foro":
                foro_id = input("Ingrese el ID del foro a eliminar: ")
                json = {
                    "name_function": "delete",
                    "data": {
                        "id_foro": foro_id,
                    }
                }
                transaction(sock, clase, json)
        else:
            print("Opción no válida o no tiene acceso a esta opción. Inténtelo de nuevo.")

def gestion_productos(sock, data_usuario):
    return 0

def gestion_servicios(sock, data_usuario):
    return 0

def gestion_msn(sock):
    id_usuario = input("Ingrese su ID de usuario:")
    id_foro = input("Ingrese el ID del foro:")
    contenido = input("Ingrese el contenido del mensaje:")
    json_data = {
        "name_function": "create_message",
        "data": {
            "id_usuario": id_usuario,
            "id_foro": id_foro,
            "contenido": contenido
        }
    }
    message = dt.create_transaction("msngr", json_data)
    print('sending {!r}'.format(message))
    sock.sendall(message)

    print("Waiting for transaction")
    amount_received = 0
    amount_expected = int(sock.recv(5))

    while amount_received < amount_expected:
        data = sock.recv(amount_expected - amount_received)
        amount_received += len(data)
    print("Checking servi answer ...")
    print('received {!r}'.format(data))
