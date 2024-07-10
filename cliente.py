#Clase de dominio o de entidad de la aplicación

class Cliente:
    def __init__(self, id = None, nombre = None, apellido = None, membresia = None):
        self._id = id
        self._nombre = nombre
        self._apellido = apellido
        self._membresia = membresia
        
    def get_id(self):
        return self._id
    
    def get_nombre(self):
        return self._nombre
    
    def set_nombre(self, nombre):
        self._nombre = nombre
        
    def get_apellido(self):
        return self._apellido
    
    def set_apellido(self, apellido):
        self._apellido = apellido
    
    def get_membresia(self):
        return self._membresia
    
    def set_membresia(self, membresia):
        self._membresia = membresia
    
    def __str__(self):
        return (f'Id: {self.get_id()}, Nombre: {self.get_nombre()}, '
                f'Apellido: {self.get_apellido()}, Membresia: {self.get_membresia()}')