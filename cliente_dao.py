from cliente import Cliente
from conexion import Conexion

class ClienteDao:
    SELECCIONAR = 'SELECT * FROM clientes'
    INSERTAR = 'INSERT INTO clientes(nombre, apellido, membresia) VALUES(%s, %s, %s)'
    ACTUALIZAR = 'UPDATE clientes SET nombre=%s, apellido=%s, membresia=%s WHERE id=%s'
    ELIMINAR = 'DELETE FROM clientes WHERE id=%s'
    
    @classmethod
    def seleccionar(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR)
            registros = cursor.fetchall()
            #Mapeo de clase tabla\
            clientes = []
            for registro in registros:
                cliente = Cliente(registro[0], registro[1], registro[2],registro[3])
                clientes.append(cliente)
            return clientes
        except Exception as e:
            print(f'Ocurrio un error al seleccionar cliente: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
     
    @classmethod           
    def insertar(cls, cliente):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cliente.get_nombre(), cliente.get_apellido(), cliente.get_membresia())
            cursor.execute(cls.INSERTAR, valores)
            conexion.commit()
            return cursor.rowcount #Conteo de registros
        except Exception as e:
            print(f'Ocurrio un error al insertar cliente {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
                
    @classmethod
    def actualizar(cls,cliente):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cliente.get_nombre(), cliente.get_apellido(), cliente.get_membresia(), cliente.get_id())
            cursor.execute(cls.ACTUALIZAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'No se pudo actualizar el cliente {e}')
        finally:
            if conexion != None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
                
    @classmethod
    def eliminar(cls, cliente):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cliente.get_id(),) #coma al final para que se cree una tupla de lo contrario marcaria error
            cursor.execute(cls.ELIMINAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'No se pudo eliminar el registro {e}')
        finally:
            if conexion != None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
            

if __name__ == '__main__':
    cliente1 = Cliente(nombre = 'Juan', apellido= 'Rodriguez', membresia = '300')
    clientes_insertados = ClienteDao.insertar(cliente1)
    print(f'Clientes insertados = {clientes_insertados}')
    
    #cliente_actualizar = Cliente(1,'Sebastian','Rodriguez',10)
    ##clientes_actualizados = ClienteDao.actualizar(cliente_actualizar)
    #print(f'Clientes actualizados: {clientes_actualizados}')
    
    #cliente_borrar  = Cliente(id=1)
    #clientes_eliminados = ClienteDao.eliminar(cliente_borrar)
    #print(clientes_eliminados)
    
    clientes = ClienteDao.seleccionar()
    for cliente in clientes:
        print(cliente)
                
            