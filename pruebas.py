import tkinter as tk
from tkinter import messagebox
from estilos import *


class VentanaPrincipal(tk.Toplevel):
    def __init__(self, login):
        super().__init__()
        self.login = login

        self.title("Panel principal")
        centrar_ventana(self, 400, 500) #Para que se abra en el centro (temporal porque pienso ponerlo en pantalla completa)

        tk.Label(self, text="Bienvenido al sistema").pack(pady=50)

        # Evento al cerrar esta ventana
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def cerrar(self):
        self.destroy()              # Cierra ventana principal
        self.login.deiconify()     # Muestra login otra vez
        self.login.limpiar_campos()  # Limpia datos


class Login(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        centrar_ventana(self, 400, 500) #Para que se abra en el centro

        tk.Label(self, text="Usuario", font=FUENTE_TITULO).pack(pady=(0,0))
        self.entry_user = tk.Entry(self)
        self.entry_user.pack()

        tk.Label(self, text="Contraseña", font=FUENTE_TITULO).pack(pady=(30, 0))
        self.entry_pass = tk.Entry(self, show="*")
        self.entry_pass.pack()

        tk.Button(self, text="Iniciar sesión", font=FUENTE_BOTON, bg=COLOR_BOTON,command=self.verificar).pack(pady=30)

        self.bind("<Return>", self.verificar_evento) #para presionar enter

        self.protocol("WM_DELETE_WINDOW", self.salir)

    def verificar(self):
        usuario = self.entry_user.get()
        contrasenia = self.entry_pass.get()

        if usuario == "admin" and contrasenia == "1234":
            self.abrir_principal()
        else:
            messagebox.showerror("Error", "Datos incorrectos")

    def verificar_evento(self, event):
        self.verificar()

    def abrir_principal(self):
        self.withdraw()  # Oculta login
        VentanaPrincipal(self)

    def limpiar_campos(self):
        self.entry_user.delete(0, tk.END)
        self.entry_pass.delete(0, tk.END)

    def salir(self):
        self.destroy()  #cerrar completamente el programa


if __name__ == "__main__":
    app = Login()
    app.mainloop()