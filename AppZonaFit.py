from cliente import Cliente
from cliente_dao import ClienteDao

print('*** Clientes Zona Fit (GYM)***')
opcion = None
while opcion != 5:
    print('''\nMenu:
    1. Listar clientes
    2. Agregar clientes
    3. Modificar cliente
    4. Eliminar cliente
    5. Salir''')
    opcion = int(input('Selecciona una opcion: '))
    if opcion == 1: # listar clientes
        print('\n *** Listado Clientes ***')
        clientes = ClienteDao.seleccionar()
        for cliente in clientes:
            print(cliente)
    elif opcion == 2: # Insertar clientes
        nombre = input('\nIngrese el nombre del cliente: ')
        apellido = input('Ingrese el apellido del cliente: ')
        membresia = input('Ingrese la membresia: ')
        cliente = Cliente(nombre=nombre, apellido=apellido, membresia=membresia)
        cliente_insertar = ClienteDao.insertar(cliente)
        print(f'Clientes insertados = {cliente_insertar}\n')
    elif opcion == 3: #Actualizar cliente
        id = int(input('\nIngrese el id de la persona a actualizar: '))
        nombre_update = input('Ingrese el nombre: ')
        apellido_update = input('Ingrese el apellido de la persona a actualizar: ')
        membresia_update = input('Ingrese la membresia de la persona: ')
        cliente = Cliente(id, nombre_update, apellido_update, membresia_update)
        cliente_update = ClienteDao.actualizar(cliente)
        print(f'Clientes Actualizados = {cliente_update}\n')
    elif opcion == 4:
        id_del = int(input('\nIngrese el id de la persona a eliminar: '))
        cliente = Cliente(id = id_del)
        cliente_delete = ClienteDao.eliminar(cliente)
        print(f'Clientes Eliminados = {cliente_delete}\n')
    else:
        print('Digite una opcion valida entre 1-5')