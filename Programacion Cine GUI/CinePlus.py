import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from cinebackendproy import Pelicula, Sala, Funcion, Usuario, Empleado, Promocion, FuncionesDatos, PromocionDatos, ReservasDatos
from PIL import ImageTk, Image, ImageFilter
import os



funciones_globales = FuncionesDatos.cargar_datos()
reservas_globales = ReservasDatos.cargar_reservas(funciones_globales)

def menu_reserva():
    ventana_admin = tk.Toplevel()
    ventana_admin.title("Menú de Reserva")
    ventana_admin.geometry("400x600")

    image_path5 = os.path.join(os.path.dirname(__file__), 'ff4.jpg')
    
    imagen_fondo = Image.open(image_path5)
    imagen_fondo = imagen_fondo.resize((600, 600))
    imagen_desenfocada = imagen_fondo.filter(ImageFilter.GaussianBlur(radius=0))  
    imagen_fondo = ImageTk.PhotoImage(imagen_desenfocada)

    ventana_admin.imagen_fondo = imagen_fondo

    fondo_label = tk.Label(ventana_admin, image=imagen_fondo)
    
    fondo_label.place(x=0, y=30, relwidth=1, relheight=1)


    tk.Label(ventana_admin, text="Seleccione una opción", font=("Arial", 20, "bold"), fg="#73C6CB", bg="#020302", padx=250, pady=20).pack(pady=0)
    
    btn_funciones = tk.Button(ventana_admin, text="Reservar Película", command=reservar_boletos, font=("Arial", 14, "bold"), width=20, height=2, bg="#73C6CB", fg="#020302")
    btn_funciones.pack(pady=50)
    
    btn_promociones = tk.Button(ventana_admin, text="Mis Reservas", command=mis_reservas,font=("Arial", 14, "bold"), width=20, height=2, bg="#73C6CB", fg="#020302")
    btn_promociones.pack(pady=15)

from PIL import Image, ImageTk

def reservar_boletos():
    ventana_reservar = tk.Toplevel()
    ventana_reservar.title("Reservar Boletos")
    ventana_reservar.geometry("700x700")  
    ventana_reservar.configure(bg="#020302")

    frame_principal = tk.Frame(ventana_reservar, bg="#020302")
    frame_principal.pack(fill="both", expand=True)

    frame_izquierdo = tk.Frame(frame_principal, bg="#020302")
    frame_izquierdo.pack(side="left", fill="both", expand=False, padx=10, pady=10)

    image_path4 = os.path.join(os.path.dirname(__file__), 'recurso.png')

    imagen = Image.open(image_path4)  
    imagen = imagen.resize((300, 657))  
    imagen_tk = ImageTk.PhotoImage(imagen)
    ventana_reservar.imagen_tk = imagen_tk  
    tk.Label(frame_izquierdo, image=imagen_tk, bg="#020302").pack()

    frame_derecho = tk.Frame(frame_principal, bg="#020302")
    frame_derecho.pack(side="right", fill="both", expand=True, padx=20, pady=100)

    peliculas_disponibles = list({funcion.pelicula.titulo for funcion in funciones_globales})

    tk.Label(frame_derecho, text="Selecciona una película:", font=("Arial", 15), fg="#73C6CB", bg="#020302").pack(pady=10)
    pelicula_var = tk.StringVar(value=peliculas_disponibles[0] if peliculas_disponibles else "")
    option_menu = tk.OptionMenu(frame_derecho, pelicula_var, *peliculas_disponibles)
    option_menu.config(bg="#020302", fg="#73C6CB", font=("Arial", 12, "bold"), activebackground="#73C6CB", activeforeground="#020302")
    option_menu.pack()

    def actualizar_funciones(*args):
        funcion_menu['menu'].delete(0, 'end')
        for funcion in funciones_globales:
            if funcion.pelicula.titulo == pelicula_var.get():
                texto_funcion = f"{funcion.hora} - Sala {funcion.sala.identificador} Tipo: {funcion.sala.tipo} ({funcion.asientos_disponibles} asientos)"
                funcion_menu['menu'].add_command(label=texto_funcion, command=tk._setit(funcion_var, texto_funcion))

    pelicula_var.trace('w', actualizar_funciones)

    tk.Label(frame_derecho, text="Selecciona una función:", font=("Arial", 15), fg="#73C6CB", bg="#020302").pack(pady=10)
    funcion_var = tk.StringVar()
    funcion_menu = tk.OptionMenu(frame_derecho, funcion_var, "")
    funcion_menu.config(bg="#020302", fg="#73C6CB", font=("Arial", 12, "bold"), activebackground="#73C6CB", activeforeground="#020302")
    funcion_menu.pack()

    tk.Label(frame_derecho, text="Número de asientos:", font=("Arial", 15), fg="#73C6CB", bg="#020302").pack(pady=10)
    asientos_entry = tk.Entry(frame_derecho, bg="#020302", fg="#73C6CB", insertbackground="#73C6CB")
    asientos_entry.pack()

    tk.Label(frame_derecho, text="Ingresa tu nombre:", font=("Arial", 15), fg="#73C6CB", bg="#020302").pack(pady=10)
    nombre_entry = tk.Entry(frame_derecho, bg="#020302", fg="#73C6CB", insertbackground="#73C6CB")
    nombre_entry.pack()

    tk.Label(frame_derecho, text="Ingresa tu correo electrónico:", font=("Arial", 15), fg="#73C6CB", bg="#020302").pack(pady=10)
    correo_entry = tk.Entry(frame_derecho, bg="#020302", fg="#73C6CB", insertbackground="#73C6CB")
    correo_entry.pack()

    def hacer_reserva():
        try:
            nombre = nombre_entry.get()
            correo = correo_entry.get()
            num_asientos = int(asientos_entry.get())
            funcion_seleccionada = None

            for funcion in funciones_globales:
                texto_funcion = f"{funcion.hora} - Sala {funcion.sala.identificador} Tipo: {funcion.sala.tipo} ({funcion.asientos_disponibles} asientos)"
                if texto_funcion == funcion_var.get():
                    funcion_seleccionada = funcion
                    break

            if funcion_seleccionada:
                if num_asientos > funcion_seleccionada.asientos_disponibles:
                    messagebox.showerror("Error", f"No hay suficientes asientos disponibles. Solo quedan {funcion_seleccionada.asientos_disponibles}.")
                    return

                usuario = Usuario(nombre, correo)
                usuario.reservar(funcion_seleccionada, num_asientos)

                reservas_globales.append({
                    "usuario": usuario,
                    "funcion": funcion_seleccionada,
                    "asientos": num_asientos
                })

                ReservasDatos.guardar_reservas(reservas_globales)
                FuncionesDatos.guardar_datos(funciones_globales)

                messagebox.showinfo("Éxito", f"Reserva confirmada para {funcion_seleccionada.pelicula.titulo}!")
                ventana_reservar.destroy()
            else:
                messagebox.showerror("Error", "Selecciona una función válida")
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido de asientos")

    tk.Button(frame_derecho, text="Reservar", width=20, height=2, font=("Arial", 10, "bold"), fg="#020302", bg="#73C6CB", command=lambda: [hacer_reserva(), confirmar_reserva()]).pack(pady=20)


def confirmar_reserva():
    ventana_confirmar = tk.Toplevel()
    ventana_confirmar.title("Mis reservas")
    ventana_confirmar.geometry("600x400")
    ventana_confirmar.configure(bg="#020302")

    tk.Label(ventana_confirmar, text="Tu reserva se ha realizado exitosamente",
             font=("Arial", 20, "bold"), fg="#73C6CB", bg="#020302").pack(pady=10)

    tk.Label(ventana_confirmar, text="Datos de tu reserva:",
             font=("Arial", 15, "bold"), fg="#73C6CB", bg="#020302").pack(pady=10)

    if not reservas_globales:
        tk.Label(ventana_confirmar, text="No hay reservas registradas.",
                 fg="white", bg="#020302").pack()
    else:
        frame_reservas = tk.Frame(ventana_confirmar, bg="#020302", bd=2, relief="groove", padx=10, pady=10)
        frame_reservas.pack(pady=10, fill="both", expand=True)

        for reserva in reservas_globales:
            info = (
                f"Cliente: {reserva['usuario'].nombre}\n"
                f"Película: {reserva['funcion'].pelicula.titulo}\n"
                f"Hora: {reserva['funcion'].hora}\n"
                f"Sala: {reserva['funcion'].sala.identificador}\n"
                f"Asientos: {reserva['asientos']}\n"
                "--------------------------"
            )

            tk.Label(frame_reservas, text=info, font=("Arial", 12),
                     fg="#73C6CB", bg="#0D0D0D", justify="left").pack(anchor="w", pady=5)

def mis_reservas():
    ventana_reservar = tk.Toplevel()
    ventana_reservar.title("Mis reservas")
    ventana_reservar.geometry("400x400")
    ventana_reservar.configure(bg="#020302")

    tk.Label(ventana_reservar, text="Reservas Realizadas", font=("Arial", 20, "bold"), fg="#73C6CB", bg="#020302", padx=250, pady=20).pack(pady=0)

    if not reservas_globales:
        tk.Label(ventana_reservar, text="No hay reservas registradas.",
                 fg="white", bg="#020302").pack()
    else:
        frame_reservas = tk.Frame(ventana_reservar, bg="#020302", bd=2, relief="groove", padx=10, pady=10)
        frame_reservas.pack(pady=10, fill="both", expand=True)

        for reserva in reservas_globales:
            info = (
                f"Cliente: {reserva['usuario'].nombre}\n"
                f"Película: {reserva['funcion'].pelicula.titulo}\n"
                f"Hora: {reserva['funcion'].hora}\n"
                f"Sala: {reserva['funcion'].sala.identificador}\n"
                f"Asientos: {reserva['asientos']}\n"
                "--------------------------"
            )

            tk.Label(frame_reservas, text=info, font=("Arial", 12),
                     fg="#73C6CB", bg="#0D0D0D", justify="left").pack(anchor="w", pady=5)



def menu_administracion():
    ventana_admin = tk.Toplevel()
    ventana_admin.title("Menú de Administración")
    ventana_admin.geometry("400x600")

    image_path3 = os.path.join(os.path.dirname(__file__), 'ff4.jpg')

    #ventana_admin.configure(bg="#020302")
    imagen_fondo = Image.open(image_path3)
    imagen_fondo = imagen_fondo.resize((600, 600))
    imagen_desenfocada = imagen_fondo.filter(ImageFilter.GaussianBlur(radius=0))  
    imagen_fondo = ImageTk.PhotoImage(imagen_desenfocada)

    ventana_admin.imagen_fondo = imagen_fondo

    fondo_label = tk.Label(ventana_admin, image=imagen_fondo)
    #fondo_label.pack(side="top", fill="x")
    fondo_label.place(x=0, y=30, relwidth=1, relheight=1)

    tk.Label(ventana_admin, text="Seleccione una opción", font=("Arial", 20, "bold"), fg="#73C6CB", bg="#020302", padx=250, pady=20).pack(pady=0)
    
    btn_funciones = tk.Button(ventana_admin, text="Administrar Funciones", command=administrar_funciones, font=("Arial", 14, "bold"), width=20, height=2, bg="#73C6CB", fg="#020302")
    btn_funciones.pack(pady=50)
    
    btn_promociones = tk.Button(ventana_admin, text="Administrar Promociones", command=administrar_promociones,font=("Arial", 14, "bold"), width=20, height=2, bg="#73C6CB", fg="#020302")
    btn_promociones.pack(pady=15)

    

def administrar_funciones():
    ventana_admin = tk.Toplevel()
    ventana_admin.title("Administrar Funciones")
    ventana_admin.geometry("400x700")
    ventana_admin.configure(bg="#020302")

    style = ttk.Style()
    style.theme_use('default')  

    style.configure("CustomCombobox.TCombobox",
    fieldbackground="#0D0D0D",  
    background="#020302",       
    foreground="#73C6CB",       
    arrowcolor="#73C6CB"        
)
    
    
    tk.Label(ventana_admin, text="Agregar nueva función", font=("Arial", 20, "bold"), bg="#020302", fg="#73C6CB").pack(pady=20)
    
    tk.Label(ventana_admin, text="Título de la película:", font=("Arial", 15), bg="#020302", fg="white").pack(pady=10)
    titulo_entry = tk.Entry(ventana_admin, bg="#020302", fg="#73C6CB", insertbackground="#73C6CB")
    titulo_entry.pack()
    
    tk.Label(ventana_admin, text="Género:", font=("Arial", 15), bg="#020302", fg="white").pack(pady=10)
    genero_entry = tk.Entry(ventana_admin, bg="#020302", fg="#73C6CB", insertbackground="#73C6CB")
    genero_entry.pack()
    
    tk.Label(ventana_admin, text="Duración (min):", font=("Arial", 15), bg="#020302", fg="white").pack(pady=10)
    duracion_entry = tk.Entry(ventana_admin, bg="#020302", fg="#73C6CB", insertbackground="#73C6CB")
    duracion_entry.pack()
    
    tk.Label(ventana_admin, text="Sala:", font=("Arial", 15), bg="#020302", fg="white").pack(pady=10)
    sala_entry = tk.Entry(ventana_admin, bg="#020302", fg="#73C6CB", insertbackground="#73C6CB")
    sala_entry.pack()

    tk.Label(ventana_admin, text="Capacidad de la sala:", font=("Arial", 15), bg="#020302", fg="white").pack(pady=10)
    capacidad_entry = tk.Entry(ventana_admin, bg="#020302", fg="#73C6CB", insertbackground="#73C6CB")
    capacidad_entry.pack()
    
    tk.Label(ventana_admin, text="Tipo de sala (2D/3D/IMAX):", font=("Arial", 15), bg="#020302", fg="white").pack(pady=10)
    tipo_combobox = ttk.Combobox(ventana_admin, values=["2D", "3D", "IMAX"], style="CustomCombobox.TCombobox")
    tipo_combobox.pack()
    
    tk.Label(ventana_admin, text="Hora (HH:MM):", font=("Arial", 15), bg="#020302", fg="white").pack(pady=10)
    hora_entry = tk.Entry(ventana_admin, bg="#020302", fg="#73C6CB", insertbackground="#73C6CB")
    hora_entry.pack()
    
    def agregar_funcion():
        try:
            pelicula = Pelicula(
                titulo_entry.get(),
                genero_entry.get(),
                int(duracion_entry.get())
            )
            
            sala = Sala(
                int(capacidad_entry.get()),
                sala_entry.get(),
                tipo_combobox.get()  
            )
            
            funcion = Funcion(
                pelicula,
                sala,
                hora_entry.get()
            )
            
            funciones_globales.append(funcion)
            FuncionesDatos.guardar_datos(funciones_globales)
            messagebox.showinfo("Éxito", "Función agregada correctamente")
            ventana_admin.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingresa datos válidos")
    
    tk.Button(ventana_admin, text="Agregar Función", command=agregar_funcion, width=20, height=2, font=("Arial", 10, "bold"), fg="#020302", bg="#73C6CB").pack(pady=30)

promociones_globales=PromocionDatos.cargar_promociones()

def administrar_promociones():
    
    ventana_admin_promos = tk.Toplevel()
    ventana_admin_promos.title("Administrar Promociones")
    ventana_admin_promos.geometry("400x600")
    ventana_admin_promos.configure(bg="#020302")
    
    tk.Label(ventana_admin_promos, text="Agregar Nueva Promoción", font=("Arial", 20, "bold"), bg="#020302", fg="#73C6CB").pack(pady=20)
    
    tk.Label(ventana_admin_promos, text="Descuento (%):", font=("Arial", 15), bg="#020302", fg="white").pack(pady=10)
    descuento_entry = tk.Entry(ventana_admin_promos, bg="#020302", fg="#73C6CB", insertbackground="#73C6CB")
    descuento_entry.pack()
    
    tk.Label(ventana_admin_promos, text="Detalles y condiciones:", font=("Arial", 15), bg="#020302", fg="white").pack(pady=10)
    condiciones_entry = tk.Entry(ventana_admin_promos, bg="#020302", fg="#73C6CB", insertbackground="#73C6CB")
    condiciones_entry.pack()
    
    def agregar_promocion():
        try:
            descuento = int(descuento_entry.get())  
            condiciones = condiciones_entry.get()
            
            nueva_promocion = Promocion(descuento, condiciones)
            promociones_globales.append(nueva_promocion)

            PromocionDatos.guardar_promociones(promociones_globales)
            
            messagebox.showinfo("Éxito", "Promoción agregada correctamente")
            ventana_admin_promos.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingresa un descuento válido")
    
    tk.Button(ventana_admin_promos, text="Agregar Promoción", command=agregar_promocion, width=20, height=2, font=("Arial", 10, "bold"), fg="#020302", bg="#73C6CB" ).pack(pady=30)


def ver_promociones():
    ventana_promos = tk.Toplevel()
    ventana_promos.title("Promociones")
    ventana_promos.geometry("550x700")
    #ventana_promos.configure(bg="#020302")

    image_path2 = os.path.join(os.path.dirname(__file__), 'stitch.jpg')

    imagen_fondo = Image.open(image_path2)
    imagen_fondo = imagen_fondo.resize((600, 750))
    imagen_desenfocada = imagen_fondo.filter(ImageFilter.GaussianBlur(radius=0))  
    imagen_fondo = ImageTk.PhotoImage(imagen_desenfocada)

    ventana_promos.imagen_fondo = imagen_fondo

    fondo_label = tk.Label(ventana_promos, image=imagen_fondo)
    
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    
    tk.Label(ventana_promos, text="Promociones Disponibles", font=("Arial", 20, "bold"), bg="#020302", fg="#73C6CB", padx=120, pady=30).pack(pady=0)
    
    if not promociones_globales:
        tk.Label(ventana_promos, text="No hay promociones disponibles").pack()
    else:
        for promocion in promociones_globales:
            promo_frame = tk.Frame(ventana_promos, bg="#73C6CB", bd=2, relief="groove", padx=10, pady=20)
            promo_frame.pack(pady=10, padx=20, fill="x")

            
            tk.Label(promo_frame, text=f"{promocion.descuento}% de descuento",
                     bg="#73C6CB", fg="#020302", font=("Arial", 14, "bold")).pack(anchor="w")
            tk.Label(promo_frame, text=f"{promocion.condiciones}",
                     bg="#73C6CB", fg="white", font=("Arial", 10)).pack(anchor="w")
    
    





ventana_principal = tk.Tk()
ventana_principal.title("Ventana Principal")
ventana_principal.geometry("480x720")

image_path = os.path.join(os.path.dirname(__file__), 'portada.jpg')

#ventana_admin.configure(bg="#020302")
imagen_fondo = Image.open(image_path)
imagen_fondo = imagen_fondo.resize((480, 700))
imagen_desenfocada = imagen_fondo.filter(ImageFilter.GaussianBlur(radius=0))  
imagen_fondo = ImageTk.PhotoImage(imagen_desenfocada)

ventana_principal.imagen_fondo = imagen_fondo

fondo_label = tk.Label(ventana_principal, image=imagen_fondo)
#fondo_label.pack(side="top", fill="x")
fondo_label.place(x=0, y=10, relwidth=1, relheight=1)


titulo = tk.Label(ventana_principal, text="¡Bienvenido a CinePlus!", font=("Arial", 24, "bold"), fg="#64D8D5", bg="#020302", padx=250, pady=20)
titulo.place(relx=0.5, rely=0.05, anchor="center")


boton_administracion = tk.Button(ventana_principal, text="Administración", command=menu_administracion, width=20, height=3, font=("Arial", 14, "bold"), bg="#020302", fg="#64D8D5")
boton_administracion.place(relx=0.5, rely=0.5, anchor="center", y=-90)  

boton_reservar = tk.Button(ventana_principal, text="Reservar", command=menu_reserva, width=20, height=3, font=("Arial", 14, "bold"), bg="#020302", fg="#64D8D5")
boton_reservar.place(relx=0.5, rely=0.5, anchor="center", y=20)  

boton_promociones = tk.Button(ventana_principal, text="Promociones", command=ver_promociones, width=20, height=3, font=("Arial", 14, "bold"), bg="#020302", fg="#64D8D5")
boton_promociones.place(relx=0.5, rely=0.5, anchor="center", y=140)  


ventana_principal.mainloop()