import socket
import json as js
import sys
from time import sleep
import utils.data_transaction as dt


def handle_data(data, clase):
    decoded_data = data.decode('utf-8')
    json_str = decoded_data[len(clase + 'OK'):]
    data_dict = js.loads(json_str)
    for key, value in data_dict.items():
        print(key, ":", value)
    return data_dict


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
    while True:
        # Menú de opciones para Gestión de Usuarios
        print("\nSeleccione una operación de Gestión de Usuarios:")
        print("1. Listar usuarios (problema)")
        print("2. Actualizar usuario")
        print("3. Eliminar usuario")
        print("4. Crear usuario")
        print("5. Loguear usuario")
        print("6. Ver Usuario")
        print("7. Volver al menú principal")
        
        opcion = input("Ingrese el número de la operación: ")
        
        if opcion == '1':
            json = {
                "name_function": "all",
                "data": {
                     "name": "usuarios",
                }
            }
            message = dt.create_transaction("suser", json)
            print('sending {!r}'.format(message))
            sock.sendall(message)

            # Esperar la respuesta
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)
            print("Checking servi answer ...")
            print('received {!r}'.format(data))

        elif opcion == '2':
            # Solicitar datos del usuario a actualizar
            id_usuario = input("Ingrese el ID del usuario a actualizar: ")
            # Solicitar datos a modificar
            rut_usuario = input("Ingrese el nuevo rut del usuario o '0' para mantener el actual:")
            if rut_usuario == '0':
                rut_usuario = None

            tipo_usuario = input("Ingrese el nuevo tipo del usuario o '0' para mantener el actual:")
            if tipo_usuario == '0':
                tipo_usuario = None

            correo = input("Ingrese el nuevo email del usuario o '0' para mantener el actual:")
            if correo == '0':
                correo = None

            fono = input("Ingrese el nuevo fono del usuario o '0' para mantener el actual:")
            if fono == '0':
                fono = None

            nombre = input("Ingrese el nuevo nombre del usuario o '0' para mantener el actual:")
            if nombre == '0':
                nombre = None

            apellido_paterno = input("Ingrese el nuevo apellido paterno del usuario o '0' para mantener el actual:")
            if apellido_paterno == '0':
                apellido_paterno = None

            apellido_materno = input("Ingrese el nuevo apellido materno del usuario o '0' para mantener el actual:")
            if apellido_materno == '0':
                apellido_materno = None

            estado_cuenta = input("Ingrese el nuevo estado de cuenta del usuario o '0' para mantener el actual:")
            if estado_cuenta == '0':
                estado_cuenta = None


            # Transformar datos a DATA del JSON
            json = {
                "name_function": "update",
                 "data": {
                        "id_usuario": id_usuario,
                        "rut": rut_usuario,
                        "tipo_usuario": tipo_usuario,
                        "correo": correo,
                        "fono": fono,
                        "nombre": nombre,
                        "apellido_paterno": apellido_paterno,
                        "apellido_materno": apellido_materno,
                        "estado_cuenta": estado_cuenta
                 }
            }
            transaction(sock, "suser", json)
           
        elif opcion == '3':
            # Solicitar ID del usuario a eliminar
            user_id = input("Ingrese el ID del usuario a eliminar: ")
            json = {
                "name_function": "delete",
                "data": {
                    "id_usuario": user_id,
                }
            }
            transaction(sock, "suser", json)
            
        elif opcion == '4':
            # Solicitar datos del nuevo usuario
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
            # Transformar datos a DATA del JSON
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

            transaction(sock, "suser", json)

        elif opcion == '5':
            cliente_login(sock)
       
        elif opcion == '6':
            # Solicitar ID del usuario a ver
            user_id = input("Ingrese el ID del usuario a ver: ")
            json = {
                "name_function": "get",
                "data": {
                    "id_usuario": user_id,
                }
            }
            transaction(sock, "suser", json)
       
        elif opcion == '7':
            # Volver al menú principal
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

def gestion_comunidad(sock, data_usuario):
    clase = "comun"
    while True:
        # Menú de opciones para Gestión de Usuarios
        print("\nSeleccione una operación de Gestión de Comunidad:")
        print("1. Crear Comunidad")
        print("2. Ver Comunidad")
        print("3. Mostrar Comunidades")
        print("4. Actualizar Comunidad")
        print("5. Eliminar Comunidad")
        print("6. Volver al menú principal")
        
        opcion = input("Ingrese el número de la operación: ")
        
        if opcion == '1':
            # Solicitar datos de la nueva comunidad
            comunidad = input("Ingrese el nombre de la nueva comunidad: ")
            json = {
                "name_function": "create",
                 "data": {
                     "nombre_comunidad": comunidad,
                 }
            }
            message = dt.create_transaction("comun", json)
            print('sending {!r}'.format(message))
            sock.sendall(message)

            # Esperar la respuesta
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)
            print("Checking servi answer ...")
            print('received {!r}'.format(data))

        elif opcion == '2':
            # Solicitar ID de la comunidad a ver
            comunidad_id = input("Ingrese el ID de la comunidad a ver: ")
            json = {
                "name_function": "get",
                "data": {
                    "id_comunidad": comunidad_id,
                }
            }
            message = dt.create_transaction("comun", json)
            print('sending {!r}'.format(message))
            sock.sendall(message)

            # Esperar la respuesta
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)
            print("Checking servi answer ...")
            print('received {!r}'.format(data))

        elif opcion == '3':
            json = {
                "name_function": "all",
                 "data": {
                     "name": "comunidad",
                 }
            }
            message = dt.create_transaction("comun", json)
            print('sending {!r}'.format(message))
            sock.sendall(message)

            # Esperar la respuesta
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)
            print("Checking servi answer ...")
            print('received {!r}'.format(data))
        
        elif opcion == '4':
            # Solicitar datos de la comunidad a actualizar
            id_comunidad = input("Ingrese el ID de la comunidad a actualizar: ")
            nombre_comunidad = input("Ingrese el nuevo nombre de la comunidad o '0' para mantener el actual:")
            if nombre_comunidad == '0':
                nombre_comunidad = None

            # Transformar datos a DATA del JSON
            json = {
                "name_function": "update",
                 "data": {
                        "id_comunidad": id_comunidad,
                        "nombre_comunidad": nombre_comunidad,
                 }
            }

            message = dt.create_transaction("comun", json)
            print('sending {!r}'.format(message))
            sock.sendall(message)

            # Esperar la respuesta
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)
            print("Checking servi answer ...")
            print('received {!r}'.format(data))
        
        elif opcion == '5':
            # Solicitar ID de la comunidad a eliminar
            comunidad_id = input("Ingrese el ID de la comunidad a eliminar: ")
            json = {
                "name_function": "delete",
                "data": {
                    "id_comunidad": comunidad_id,
                }
            }
            message = dt.create_transaction("comun", json)
            print('sending {!r}'.format(message))
            sock.sendall(message)

            # Esperar la respuesta
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)
            print("Checking servi answer ...")
            print('received {!r}'.format(data))
            
        elif opcion == '6':
            # Volver al menú principal
            break

def gestion_productos(sock, data_usuario):
    return 0

def gestion_servicios(sock, data_usuario):
    return 0

def gestion_foros(sock, data_usuario):
    clase = "foros"
    while True:
        # Menú de opciones para Gestión de Usuarios
        print("\nSeleccione una operación de Gestión de Foros:")
        print("1. Crear Foro")
        print("2. Ver Foro")
        print("3. Mostrar Foros")
        print("4. Actualizar Foro")
        print("5. Eliminar Foro")
        print("6. Volver al menú principal")
        
        opcion = input("Ingrese el número de la operación: ")
        
        if opcion == '1':
            # Solicitar datos del nuevo foro
            id_comunidad = input("Ingrese el id de la comunidad del nuevo foro: ")
            id_usuario = input("Ingrese el id del usuario del nuevo foro: ")
            tipo_foro = input("Ingrese el tipo del nuevo foro: ")
            estado_foro = input("Ingrese el estado del nuevo foro: ")
            tema_foro = input("Ingrese el tema del nuevo foro: ")
            # Transformar datos a DATA del JSON
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

            message = dt.create_transaction("foros", json)
            print('sending {!r}'.format(message))
            sock.sendall(message)

            # Esperar la respuesta
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)
            print("Checking servi answer ...")
            print('received {!r}'.format(data))

        elif opcion == '2':
            # Solicitar ID del foro a ver
            foro_id = input("Ingrese el ID del foro a ver: ")
            json = {
                "name_function": "get",
                "data": {
                    "id_foro": foro_id,
                }
            }
            message = dt.create_transaction("foros", json)
            print('sending {!r}'.format(message))
            sock.sendall(message)

            # Esperar la respuesta
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)
            print("Checking servi answer ...")
            print('received {!r}'.format(data))

        elif opcion == '3':
            # Solicitar ID del foro a ver
            json = {
                "name_function": "all",
                "data": {
                    "id_foro": "foros",
                }
            }
            message = dt.create_transaction("foros", json)
            print('sending {!r}'.format(message))
            sock.sendall(message)

            # Esperar la respuesta
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)
            print("Checking servi answer ...")
            print('received {!r}'.format(data))

        elif opcion == '4':
            # Solicitar datos del foro a actualizar
            id_foro = input("Ingrese el ID del foro a actualizar: ")
            tipo_foro = input("Ingrese el nuevo tipo del foro o '0' para mantener el actual:")
            if tipo_foro == '0':
                tipo_foro = None

            estado_foro = input("Ingrese el nuevo estado del foro o '0' para mantener el actual:")
            if estado_foro == '0':
                estado_foro = None

            tema_foro = input("Ingrese el nuevo tema del foro o '0' para mantener el actual:")
            if tema_foro == '0':
                tema_foro = None

            # Transformar datos a DATA del JSON
            json = {
                "name_function": "update",
                 "data": {
                        "id_foro": id_foro,
                        "tipo_foro": tipo_foro,
                        "estado_foro": estado_foro,
                        "tema_foro": tema_foro,

                 }
            }

            message = dt.create_transaction("foros", json)
            print('sending {!r}'.format(message))
            sock.sendall(message)

            # Esperar la respuesta
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)
            print("Checking servi answer ...")
            print('received {!r}'.format(data))

        elif opcion == '5':
            # Solicitar ID del foro a eliminar
            foro_id = input("Ingrese el ID del foro a eliminar: ")
            json = {
                "name_function": "delete",
                "data": {
                    "id_foro": foro_id,
                }
            }
            message = dt.create_transaction("foros", json)
            print('sending {!r}'.format(message))
            sock.sendall(message)

            # Esperar la respuesta
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)
            print("Checking servi answer ...")
            print('received {!r}'.format(data))

        elif opcion == '6':
            # Volver al menú principal
            break
