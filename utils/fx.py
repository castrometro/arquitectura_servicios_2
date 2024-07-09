import socket
import json as js
import sys
from time import sleep
import utils.data_transaction as dt
total_message = b''

def handle_data(data, clase):
    print('handle data-------')
    decoded_data = data.decode('utf-8', errors='ignore')
    print ("Decoded data: ", decoded_data)
    prefix = clase + 'OK'
    
    if len(decoded_data) > len(prefix):
        json_str = decoded_data
        print ("JSON: ", json_str)
        try:
            print(json_str)
            data_dict = js.loads(json_str)
        except js.JSONDecodeError:
            print("OK, no hay json")
            return {}
        
        if isinstance(data_dict, list):
            print("Los datos son una lista:")
            for item in data_dict:
                print(item)
            return data_dict
        elif isinstance(data_dict, dict):
            print("Los datos son un diccionario:")
            for key, value in data_dict.items():
                print(key, ":", value)
            return data_dict
        else:
            print("Los datos no son ni una lista ni un diccionario.")
            return {}
    else:
        print("No hay datos después de 'OK'")
        return {}
total_lenght = 0
total_message = b''
def transaction(sock, clase, json_data):
    global total_lenght 
    global total_message
    print ("------------------")
    print("Enviando transaccion ...")
    print("Clase: ", clase)
    print ("------------------")
    print ("JSON: ", json_data)
    print ("------------------")
    print ("Creando Mensaje ...")   
    message = dt.create_transaction(clase, json_data)
    print ("Mensaje: ", message)
    print ("------------------")
    print ("Enviando Mensaje ...")
    print('sending {!r}'.format(message))
    sock.sendall(message)
    print ("------------------")
    while len(total_message) != total_lenght or total_message == b'':
        # Esperar la respuesta
        print("...Esperando transaccion respuesta")
        amount_received = 0
        a = sock.recv(17).decode()
        print ("------------------")
        print("Recibido: ", a)
        print ("------------------")
        amount_expected = int(a[0:5])
        total_lenght = int(a[12:]) # Decodificar la cantidad esperada
        print("Cantidad Total: ", total_lenght)
        print("Cantidad esperada: ", amount_expected)
        # data = b''
        # total_message = b''
        # while amount_received < amount_expected:
        #         data = sock.recv(amount_expected - amount_received)
        #         amount_received += len(data)
        # print("Verificando respuesta del servidor...")
        # print('Recibido {!r}'.format(data))
        # print(data, 'RAW DATA')
        # print("Esperando Respuesta ...")
        # if clase in ["suser", "comun", "foros", "chats"]:
        #     return handle_data(data, clase)
        # else:
        #     print("Clase no encontrada")
        #     print('received {!r}'.format(data))
        #     return {}
        message = b''
        
        while amount_received < amount_expected:
            print ('Soy el while:')
            print('ammount:', amount_received)
            print ('cantidad recivida:', amount_received)
            print ('---------------')
            data = sock.recv(amount_expected - amount_received)
            name_function = data[0:5]
            if total_message == b'':
                print (data, 'DATAAA')
                #largo_total = data[10:15]
                #print('Largo total: ', largo_total)
                messaje = data
                total_message = messaje
                
                amount_received += len(data) + 12
                
                print('total message:', total_message)
                print ('-----1------')

                
            else:
                print('total message:', total_message)
                total_message += data
                amount_received += len(data) + 12
                
            print('ammount pene:', amount_received)
            print('cantidad recivida:', amount_received)
            print ('-----2------')

        print('total message_final:', total_message)
        print('----3------')
        print('len total message:', len(total_message))
        print('ammount:', amount_expected)
        print ('total lenght', total_lenght)
        if len(total_message) + 10 == total_lenght and total_message != b'':
            print('ENTRE a la wa')
            messaje = b''
            #total_message = total_message[10:]
            print('mensaje total:', total_message)
            data = total_message
            total_message = b''
            total_lenght = 0
            # print("Enviando respuesta")
            # message = b'00013serviReceived'
            # print('Enviando {!r}'.format(message))
            # sock.sendall(message)
            if clase in ["suser", "comun", "foros", "chats"]:
                return handle_data(data, clase)
            else:
                print("Clase no encontrada")
                print('received {!r}'.format(data))
                return {}
        else:
            print ('no entré al if')


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
    
def chat(sock, data_usuario):
    clase="chats"
    tipo_usuario = data_usuario['tipo_usuario']
    menus = {
        'RESIDENTE': [
            "Ver Chat",
            "Enviar Mensaje",
            "Crear Chat",
            "Obtener Mensajes"
        ],
        'CONSERJE': [
            "Ver Chat",
            "Enviar Mensaje",
            "Crear Chat",
            "Obtener Mensajes"
        ],
        'ADMINISTRADOR': [
            "Ver Chat",
            "Enviar Mensaje",
            "Crear Chat",
            "Mostrar Chats",
            "Eliminar Chat",
            "Obtener Mensajes"
        ],
        'ADMINISTRADOR_SISTEMA': [
            "Ver Chat",
            "Enviar Mensaje",
            "Crear Chat",
            "Mostrar Chats",
            "Eliminar Chat",
            "Obtener Mensajes"
        ]
    }

    menu_actions = {
        "Ver Chat": "1",
        "Mostrar Chats": "2",
        "Enviar Mensaje": "3",
        "Crear Chat": "4",
        "Obtener Mensajes": "5",
        "Volver al menú principal": "6"
    }

    while True:
        print("\nSeleccione una operación de Chat:")
        opciones_disponibles = menus[tipo_usuario]
        for i, opcion in enumerate(opciones_disponibles, start=1):
            print(f"{i}. {opcion}")

        print(f"{len(opciones_disponibles) + 1}. Volver al menú principal")

        opcion = input("Ingrese el número de la operación: ")

        if opcion == str(len(opciones_disponibles) + 1):
            break
        elif opcion.isdigit() and 1 <= int(opcion) <= len(opciones_disponibles):
            accion = opciones_disponibles[int(opcion) - 1]

            if accion == "Ver Chat":
                chat_id = input("Ingrese el ID del chat a ver: ")
                json = {
                    "name_function": "get",
                    "data": {
                        "id_chat": chat_id,
                    }
                }
                transaction(sock, clase, json)

            elif accion == "Mostrar Chats":
                json = {
                    "name_function": "all",
                    "data": {
                        "name": "chats",
                    }
                }
                transaction(sock, clase, json)

            elif accion == "Enviar Mensaje":
                id_usuario = data_usuario['id_usuario']
                id_chat = input("Ingrese el ID del chat:")
                contenido = input("Ingrese el contenido del mensaje:")
                json_data = {
                    "name_function": "create_mensaje",
                    "data": {
                        "id_usuario": id_usuario,
                        "id_chat": id_chat,
                        "contenido": contenido
                    }
                }
                transaction(sock, clase, json_data)

            elif accion == "Eliminar Chat":
                chat_id = input("Ingrese el ID del chat a eliminar: ")
                json = {
                    "name_function": "delete",
                    "data": {
                        "id_chat": chat_id,
                    }
                }
                transaction(sock, clase, json)

            elif accion == "Crear Chat":
                id_usuario = data_usuario['id_usuario']
                id_usuario2 = input("Ingrese el ID del otro usuario:")
                json_data = {
                    "name_function": "create",
                    "data": {
                        "id_usuario_remitente": id_usuario,
                        "id_usuario_receptor": id_usuario2
                    }
                }
                transaction(sock, clase, json_data)

            elif accion == "Obtener Mensajes":
                id_chat = input("Ingrese el ID del chat:")
                json_data = {
                    "name_function": "get_mensajes",
                    "data": {
                        "id_chat": id_chat
                    }
                }
                transaction(sock, clase, json_data)
        else:
            print("Opción no válida o no tiene acceso a esta opción. Inténtelo de nuevo.")

def gestion_usuarios(sock, data_usuario):
    clase = "suser"
    tipo_usuario = data_usuario['tipo_usuario']

    # Definir las opciones del menú para cada tipo de usuario
    menus = {
        'RESIDENTE': [
            "Ver Usuario",
            "Modificar privacidad"
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
        "Modificar privacidad": "7",
        "Volver al menú principal": "8"
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
                id_comunidad = input("Ingrese el id de la comunidad del nuevo usuario: ")
                rut = input("Ingrese el rut del nuevo usuario: ")
                tipo_usuario = input("Ingrese el tipo del nuevo usuario: ")
                correo = input("Ingrese el email del nuevo usuario: ")
                fono = input("Ingrese el fono del nuevo usuario: ")
                nombre = input("Ingrese el nombre del nuevo usuario: ")
                apellido_paterno = input("Ingrese el ap_p del nuevo usuario: ")
                apellido_materno = input("Ingrese el ap_m del nuevo usuario: ")
                estado_cuenta = input("Ingrese el estado del nuevo usuario: ")
                contrasena = input("Ingrese la contraseña del nuevo usuario: ")
                json = {
                    "name_function": "create",
                    "data": {
                        "id_comunidad": id_comunidad,
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
            
            elif accion == "Modificar Privacidad":
                user_id = data_usuario['id_usuario']
                nueva_privacidad = input("Ingrese la nueva privacidad (publica/privada): ")
                json = {
                    "name_function": "update_privacidad",
                    "data": {
                        "id_usuario": user_id,
                        "privacidad": nueva_privacidad
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
            "Mostrar Foros",
            "Gestion Mensajeria",
            "Ver Mensajes"
        ],
        'CONSERJE': [
            "Ver Foro",
            "Mostrar Foros",
            "Gestion Mensajeria"
        ],
        'ADMINISTRADOR': [
            "Crear Foro",
            "Ver Foro",
            "Mostrar Foros",
            "Actualizar Foro",
            "Eliminar Foro",
            "Enviar Mensaje",
            "Ver Mensajes"
        ],
        'ADMINISTRADOR_SISTEMA': [
            "Crear Foro",
            "Ver Foro",
            "Mostrar Foros",
            "Actualizar Foro",
            "Eliminar Foro",
            "Enviar Mensaje",
            "Ver Mensajes"
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

            
            elif accion == "Enviar Mensaje":
                id_usuario = input("Ingrese su ID de usuario:")
                id_foro = input("Ingrese el ID del foro:")
                contenido = input("Ingrese el contenido del mensaje:")
                json_data = {
                    "name_function": "create_mensaje",
                    "data": {
                        "id_usuario": id_usuario,
                        "id_foro": id_foro,
                        "contenido": contenido
                    }
                }
                transaction(sock, clase, json_data)
            
            elif accion == "Ver Mensajes":
                foro_id = input("Ingrese el ID del foro:")
                json_data = {
                    "name_function": "get_mensajes",
                    "data": {
                        "id_foro": foro_id
                    }
                }
                transaction(sock, clase, json_data)

        else:
            print("Opción no válida o no tiene acceso a esta opción. Inténtelo de nuevo.")

def gestion_productos(sock, data_usuario):
    return 0

def gestion_servicios(sock, data_usuario):
    return 0


