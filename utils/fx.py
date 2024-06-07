import socket
import utils.data_transaction as dt

def gestion_usuarios(sock):
    while True:
        # Menú de opciones para Gestión de Usuarios
        print("\nSeleccione una operación de Gestión de Usuarios:")
        print("1. Listar usuarios")
        print("2. Actualizar usuario")
        print("3. Eliminar usuario")
        print("4. Crear usuario")
        print("5. Loguear usuario")
        print("6. Registrar usuario")
        print("7. Ver Usuario")
        print("8. Volver al menú principal")
        
        opcion = input("Ingrese el número de la operación: ")
        
        if opcion == '1':
            json = {
                "name_function": "all",
                # "data": {
                #     "name": "comunidad",
                # }
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
           
        elif opcion == '3':
            # Solicitar ID del usuario a eliminar
            user_id = input("Ingrese el ID del usuario a eliminar: ")
            json = {
                "name_function": "delete",
                "data": {
                    "id_usuario": user_id,
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

        elif opcion == '5':
            # Solicitar datos de logueo
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

        elif opcion == '6':
            # Solicitar datos de registro
            rut = input("Ingrese el rut del usuario: ")
            tipo_usuario = input("Ingrese el tipo del usuario: ")
            correo = input("Ingrese el email del usuario: ")
            fono = input("Ingrese el fono del usuario: ")
            nombre = input("Ingrese el nombre del usuario: ")
            apellido_paterno = input("Ingrese el apellido paterno del usuario: ")
            apellido_materno = input("Ingrese el apellido materno del usuario: ")
            estado_cuenta = input("Ingrese el estado de cuenta del usuario: ")
            contrasena = input("Ingrese la contraseña del usuario: ")
            # Transformar datos a DATA del JSON
            json = {
                "name_function": "register",
                 "data": {
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
       
        elif opcion == '7':
            # Solicitar ID del usuario a ver
            user_id = input("Ingrese el ID del usuario a ver: ")
            json = {
                "name_function": "get",
                "data": {
                    "id_usuario": user_id,
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
       
        elif opcion == '8':
            # Volver al menú principal
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")