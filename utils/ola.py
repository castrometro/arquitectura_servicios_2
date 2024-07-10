def gestion_departamento(sock, data_usuario):
    clase = "depto"
    tipo_usuario = data_usuario['tipo_usuario']

    # Definir las opciones del menú para cada tipo de usuario
    menus = {
        'RESIDENTE': [
            "Ver departamento",
            "Mostrar departamentos"
        ],
        'CONSERJE': [
            "Ver Departamento",
            "Mostrar Departamentos"
        ],
        'ADMINISTRADOR': [
            "Crear Departamento",
            "Ver Departamento",
            "Mostrar Departamentos"
        ],
        'ADMINISTRADOR_SISTEMA': [
            "Crear Departamento",
            "Ver Departamento",
            "Mostrar Departamentos",
            "Eliminar Departamento"
        ]
    }

    while True:
        # Mostrar las opciones del menú según el tipo de usuario
        print("\nSeleccione una operación de Gestión de Departamento:")
        opciones_disponibles = menus[tipo_usuario]
        for i, opcion in enumerate(opciones_disponibles, start=1):
            print(f"{i}. {opcion}")

        print(f"{len(opciones_disponibles) + 1}. Volver al menú principal")

        opcion = input("Ingrese el número de la operación: ")

        if opcion == str(len(opciones_disponibles) + 1):
            break
        elif opcion.isdigit() and 1 <= int(opcion) <= len(opciones_disponibles):
            accion = opciones_disponibles[int(opcion) - 1]

            if accion == "Crear Departamento":
                comunidad_id = input("Ingrese el ID de la comunidad donde crear el Departamento:")
                json = {
                    "name_function": "get",
                    "data": {
                        "id_comunidad": comunidad_id,
                    }
                }
                response = transaction(sock, comun, json)
                if 'error' not in response:
                    print('Comunidad Encontrada')
                    numero_departamento = input("Ingrese el número del Departamento:")
                    json = {
                        "name_function": "create",
                        "data": {
                            "id_comunidad": comunidad_id,
                            "numero": numero_departamento,
                        }
                    }
                    transaction(sock, clase, json)
                else:
                    print('Comunidad No existe')

            elif accion == "Ver Departamento":
                id_comunidad = input("Ingrese el ID de la comunidad a ver: ")
                numero_departamento= input("Ingrese el numero del Departamento a ver: ")
                json = {
                    "name_function": "get",
                    "data": {
                        "numero": numero_departamento,
                        "id_comunidad": id_comunidad
                    }
                }
                transaction(sock, clase, json)

            elif accion == "Mostrar Departamentos por Comunidad":
                comunidad_id = input("Ingrese el ID de la comunidad a ver: ")
                json = {
                    "name_function": "all",
                    "data": {
                        "id_comunidad": comunidad_id,
                    }
                } 
                transaction(sock, clase, json)

            # elif accion == "Actualizar Departamento":
            #     id_Departamento = input("Ingrese el ID de la Departamento a actualizar: ")
            #     json = {
            #         "name_function": "get",
            #         "data": {
            #             "id_Departamento": id_Departamento,
            #         }
            #     }
                # response = transaction(sock, clase, json)
                # if 'error' not in response:
                #     print('Departamento Encontrada')
                #     nombre_Departamento = input("Ingrese el nuevo nombre de la Departamento o enter para mantener el actual:") or response['nombre_Departamento']
            
                #     json = {
                #         "name_function": "update",
                #         "data": {
                #             "id_Departamento": id_Departamento,
                #             "nombre_Departamento": nombre_Departamento,
                #         }
                #     }
                #     transaction(sock, clase, json)
                # else:
                #     print('Departamento No existe')

            elif accion == "Eliminar Departamento":
                id_comunidad = input("Ingrese el ID de la comunidad a la que pertenece el Departamento a eliminar:")
                numero = input("Ingrese el numero de la Departamento a eliminar: ")
                json = {
                    "name_function": "delete",
                    "data": {
                        "numero": numero,
                        "id_comunidad": id_comunidad
                    }
                }
                transaction(sock, clase, json)
        else:
            print("Opción no válida o no tiene acceso a esta opción. Inténtelo de nuevo.")