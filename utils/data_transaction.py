def create_transaction(service, data):
    # print ('create_transaction...')
    # print ('service:', service)
    # print ('data:', data)
    # print ('len(data):', len(data))
    # print ('len(service):', len(service))
    # print ('Entrando a ifs...')
    if len(service) != 5:
        raise ValueError("El nombre del servicio debe tener exactamente 5 caracteres.")
    data_length = len(data)
    if data_length > 99999:
        raise ValueError("Los datos no pueden tener más de 99999 caracteres.")
    # print ('Saliendo de ifs...')
    # print ('Creando transaction...')
    cantidad = len(data) + len(service)
    transaction = f"{cantidad:05}{service}{data}"
    # print ('transaction:', transaction)
    return transaction.encode()

def create_transaction_data(service, data):
    if len(service) != 5:
        raise ValueError("El nombre del servicio debe tener exactamente 5 caracteres.")
    data_length = len(data)
    if data_length > 99999:
        raise ValueError("Los datos no pueden tener más de 99999 caracteres.")
    
    transaction = f"{data_length:05}{service}{data}"
    return transaction.encode()

def create_service_data(service):
    if len(service) != 5:
        raise ValueError("El nombre del servicio debe tener exactamente 5 caracteres.")
    transaction = f"00010sinit{service}"
    return transaction.encode()