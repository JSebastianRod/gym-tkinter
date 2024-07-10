import tkinter as tk
from tkinter import Scrollbar, ttk
from tkinter.messagebox import showerror, showinfo

from cliente import Cliente
from cliente_dao import ClienteDao

class App(tk.Tk):
    COLOR_VENTANA = '#1d2d44'
    def __init__(self):
        super().__init__()
        self.id_cliente = None
        self.configurar_ventana()
        self.configurar_grid()
        self.mostrar_titulo()
        self.mostrar_formulario()
        self.mostrar_tabla()
        self.mostrar_botones()
            
    def configurar_ventana(self):
        self.geometry('900x600')
        self.title('Zona Fit App')
        self.configure(background=App.COLOR_VENTANA)
        #Aplicamos el estilo
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        self.estilo.configure(self,background = App.COLOR_VENTANA, foreground = 'white')
        
    def configurar_grid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
    def mostrar_titulo(self):
        etiqueta = ttk.Label(self, text='ZONA FIT GYM', font=('Arial', 30), background=App.COLOR_VENTANA, foreground='white')
        etiqueta.grid(row=0, column=0, columnspan=2, pady=30)
        
    def mostrar_formulario(self):
        self.frame_f = ttk.Frame()
        #Nombre
        nombre_l = ttk.Label(self.frame_f, text='Nombre: ')
        nombre_l.grid(row=0, column=0, sticky=tk.W, pady=30)
        self.nombre_e = ttk.Entry(self.frame_f)
        self.nombre_e.configure(foreground = 'black')
        self.nombre_e.grid(row=0, column=1)
        #Apellido
        apellido_l = ttk.Label(self.frame_f, text='Apellido: ')
        apellido_l.grid(row=1, column=0, sticky=tk.W, pady=30)
        self.apellido_e = ttk.Entry(self.frame_f)
        self.apellido_e.configure(foreground='black')
        self.apellido_e.grid(row=1, column=1)
        #Membresia
        membresia_l = ttk.Label(self.frame_f, text='Membresia: ')
        membresia_l.grid(row=2, column=0, sticky=tk.W, pady=30)
        self.membresia_e = ttk.Entry(self.frame_f)
        self.membresia_e.configure(foreground= 'black')
        self.membresia_e.grid(row=2, column=1)
        
        
        #Publicamos el frame
        self.frame_f.grid(row=1, column=0)
    
    def mostrar_tabla(self): 
        #Creamos un frame para mostrar la tabla
        self.frame_tabla = ttk.Frame(self)
        #Definimos estilos
        self.estilo.configure('Treeview', background = 'black', foreground = 'white', fieldbackground = 'black', rowheight =30)
        columnas = ('Id', 'Nombre', 'Apellido', 'Membresia')
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show='headings')
        #Cabeceros tabla
        self.tabla.heading('Id', text='Id', anchor=tk.CENTER)
        self.tabla.heading('Nombre', text='Nombre', anchor=tk.W)
        self.tabla.heading('Apellido', text='Apellido', anchor=tk.W)
        self.tabla.heading('Membresia', text='Membresia', anchor=tk.W)
        #Formato columas
        self.tabla.column('Id', anchor=tk.CENTER, width=80)
        self.tabla.column('Nombre', anchor=tk.W, width=120)
        self.tabla.column('Apellido', anchor=tk.W, width=120)
        self.tabla.column('Membresia', anchor=tk.W, width=120)
        
        #Cargar datos BD
        clientes = ClienteDao.seleccionar()
        for cliente in clientes:
            self.tabla.insert(parent='', index=tk.END, values=(cliente.get_id(), cliente.get_nombre(), cliente.get_apellido(), cliente.get_membresia()))
        scrollbar = tk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscroll = scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.tabla.grid(row=0, column=0)
        
        #Asociamos el evento select
        self.tabla.bind('<<TreeviewSelect>>', self.cargar_cliente)
        
        self.frame_tabla.grid(row=1, column=1, padx=30)
        
    def cargar_cliente(self, event):
        elemento_seleccionado = self.tabla.selection()[0]
        elemento = self.tabla.item(elemento_seleccionado)
        cliente_t = elemento['values']
        #Recuperamos el valor del cliente
        self.id_cliente = cliente_t[0]
        nombre = cliente_t[1]
        apellido = cliente_t[2]
        membresia = cliente_t[3]
        #Limpiamos el formulario por si son muchos clicks
        self.limpiar_formulario()
        #Cargar los valores en el formulario
        self.nombre_e.insert(0, nombre)
        self.apellido_e.insert(0, apellido)
        self.membresia_e.insert(0, membresia)       
        
    def mostrar_botones(self):
        self.frame_b = ttk.Frame()
        agregar_b = ttk.Button(self.frame_b, text='Guardar', command=self.validar_cliente)
        agregar_b.grid(row=0, column=0, padx=30)
        eliminar_b = ttk.Button(self.frame_b, text='Eliminar', command=self.eliminar_cliente)
        eliminar_b.grid(row=0, column=1, padx=30)
        limpiar_b = ttk.Button(self.frame_b, text='Limpiar', command=self.limpiar_datos)
        limpiar_b.grid(row=0, column=2, padx=30)
        
        #Aplicamos estilo a botones
        self.estilo.configure('TButton', background='#005f73')
        self.estilo.map('TButton', background=[('active', '#0a9396')])
        
        self.frame_b.grid(row=2, column=0, columnspan=2, pady=40)
            
    def validar_cliente(self):
        #Validamos los campos
        if self.nombre_e.get() and self.apellido_e.get() and self.membresia_e.get():
            if self.validar_membresia():
                self.guardar_cliente()
            else:
                showerror(title='Atencion!!', message='El valor de membresia NO es numérico')
                self.membresia_e.delete(0, tk.END)# se borra la cadena desde el inicio hasta el final
                self.membresia_e.focus_set()#Colocar cursor sobre este campo
        else:
            showerror(title='Atencion', message='El formulario esta incompleto')
            self.nombre_e.focus_set()
                        
    def validar_membresia(self):
        try:
            int(self.membresia_e.get())
            return True
        except:
            return False
    
    def eliminar_cliente(self):
        if self.id_cliente is None:
            showerror(title='Atencion', message='Debe seleccionar un cliente a eliminar')
        else:
            cliente = Cliente(id = self.id_cliente)
            ClienteDao.eliminar(cliente)
            showinfo(title='Eliminado', message='Cliente eliminado')
            self.recargar_datos()
    
    def limpiar_datos(self):
        self.limpiar_formulario()
        self.id_cliente = None
    
    def limpiar_formulario(self):
        self.nombre_e.delete(0, tk.END)
        self.apellido_e.delete(0,tk.END)
        self.membresia_e.delete(0,tk.END)
    
    def guardar_cliente(self):
        #recuperar valores de las cajas de texto
        nombre = self.nombre_e.get()
        apellido = self.apellido_e.get()
        membresia = self.membresia_e.get()
        # Validamos el valor de id del cliente
        if self.id_cliente is None:    #Insertar
            cliente = Cliente(nombre=nombre, apellido=apellido, membresia=membresia)
            ClienteDao.insertar(cliente)
            showinfo(title='Agregar' ,message='Cliente Agregado')
        else: #Actualizar
            cliente = Cliente(self.id_cliente, nombre, apellido, membresia)
            ClienteDao.actualizar(cliente)
            showinfo(title='Actualizacion', message='Cliente Actualizado')
        #Recargar tabla luego de agregar el cliente
        self.recargar_datos()
        
    def recargar_datos(self):
        self.mostrar_tabla()
        #Limpiar datos
        self.limpiar_datos()
    
if __name__ == '__main__':
    app = App()
    app.mainloop()