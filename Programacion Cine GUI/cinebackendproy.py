import json
import os

class Persona:

    lista=[]
    
    def __init__(self,nombre,correo):
        self.nombre=nombre
        self.correo=correo

    def registrar(self):
        Persona.lista.append(self)
        print(f"La persona {self.nombre} ha sido registrada con el correo {self.correo}")

    def actualizar_datos(self,nombre,correo):
        self.nombre=nombre
        self.correo=correo
        print(f"Los datos han sido actualizados")

    @classmethod
    def personas_registradas(cls):
        print("Personas registradas")
        for Persona in cls.lista:
            print(f"-{Persona.nombre} - {Persona.correo}")


class Usuario(Persona):
    def __init__(self, nombre, correo):
        super().__init__(nombre, correo)
        self.historial_reservas = []

    def reservar(self, funcion, asientos):
        if asientos <= funcion.asientos_disponibles:
            funcion.asientos_disponibles -= asientos
            self.historial_reservas.append({"funcion": funcion, "asientos": asientos})
            print(f"Reserva realizada para '{funcion.pelicula.titulo}' en la sala {funcion.sala.identificador}.")
        else:
            print("No hay suficientes asientos disponibles.")
    

    def cancelar_reserva(self, funcion):
        reserva = next((r for r in self.historial_reservas if r["funcion"] == funcion), None)
        if reserva:
            funcion.asientos_disponibles += reserva["asientos"]
            self.historial_reservas.remove(reserva)
            print(f"Reserva cancelada para '{funcion.pelicula.titulo}'.")
        else:
            print("No tienes una reserva para esta función.")

class Empleado(Persona):
    def __init__(self, nombre, correo, rol):
        super().__init__(nombre, correo)
        self.rol = rol

    def agregar_funcion(self, funcion):
        print(f"Función agregada: {funcion.pelicula.titulo} a las {funcion.hora} en la sala {funcion.sala.identificador}.")

    def modificar_promocion(self, promocion, nuevo_descuento, nuevas_condiciones):
        promocion.descuento = nuevo_descuento
        promocion.condiciones = nuevas_condiciones
        print(f"Promoción modificada: {nuevo_descuento}% de descuento. {nuevas_condiciones}.")


class Espacio:
    def __init__(self,capacidad,identificador):
        self.capacidad=capacidad
        self.identificador=identificador
    
    def descripcion(self):
        print(f"El edificio tiene tamaño {self.capacidad} y tiene id {self.identificador}")

class Sala(Espacio):
    def __init__(self,capacidad,identificador,tipo):
        super().__init__(capacidad,identificador)
        self.tipo=tipo
        self.disponibilidad=True

    def Consultardisponibilidad(self):
        if self.disponibilidad:
            print("La sala esta disponible")
        else:
            print("La sala esta ocupada")


class Pelicula:
    def __init__(self, titulo, genero, duracion):
        self.titulo = titulo
        self.genero = genero
        self.duracion = duracion

class Funcion:
    def __init__(self, pelicula, sala, hora, asientos_disponibles=None):
        self.pelicula = pelicula
        self.sala = sala
        self.hora = hora
        self.asientos_disponibles = asientos_disponibles or sala.capacidad

class Promocion:
    def __init__(self, descuento, condiciones):
        self.descuento = descuento
        self.condiciones = condiciones

    def mostrar(self):
        print(f"Promoción: {self.descuento}% de descuento. Condiciones: {self.condiciones}")


class FuncionesDatos:
    FUNCIONES_JSON = "funciones.json"
    
    @classmethod
    def guardar_datos(cls, funciones):
        datos = {
            'funciones': [
                {
                    'pelicula': {
                        'titulo': funcion.pelicula.titulo,
                        'genero': funcion.pelicula.genero,
                        'duracion': funcion.pelicula.duracion
                    },
                    'sala': {
                        'capacidad': funcion.sala.capacidad,
                        'identificador': funcion.sala.identificador,
                        'tipo': funcion.sala.tipo
                    },
                    'hora': funcion.hora,
                    'asientos_disponibles': funcion.asientos_disponibles
                }
                for funcion in funciones
            ]
        }
        
        with open(cls.FUNCIONES_JSON, 'w') as f:
            json.dump(datos, f, indent=4)
    
    @classmethod
    def cargar_datos(cls):
        if not os.path.exists(cls.FUNCIONES_JSON):
            return []
            
        with open(cls.FUNCIONES_JSON, 'r') as f:
            datos = json.load(f)
        
        funciones = []
        for func_data in datos['funciones']:
            pelicula = Pelicula(
                func_data['pelicula']['titulo'],
                func_data['pelicula']['genero'],
                func_data['pelicula']['duracion']
            )
            
            sala = Sala(
                func_data['sala']['capacidad'],
                func_data['sala']['identificador'],
                func_data['sala']['tipo']
            )
            
            funcion = Funcion(
                pelicula,
                sala,
                func_data['hora'],
                func_data['asientos_disponibles']
            )
            
            funciones.append(funcion)
        
        return funciones

class PromocionDatos:
    PROMOCIONES_JSON = "promociones.json"
    
    @classmethod
    def guardar_promociones(cls, promociones):
        datos = {
            'promociones': [
                {
                    'descuento': promocion.descuento,
                    'condiciones': promocion.condiciones
                }
                for promocion in promociones
            ]
        }
        
        with open(cls.PROMOCIONES_JSON, 'w') as f:
            json.dump(datos, f, indent=4)
    
    @classmethod
    def cargar_promociones(cls):
        if not os.path.exists(cls.PROMOCIONES_JSON):
            return []
            
        with open(cls.PROMOCIONES_JSON, 'r') as f:
            datos = json.load(f)
        
        return [Promocion(p['descuento'], p['condiciones']) for p in datos['promociones']]
    
class ReservasDatos:
    RESERVAS_JSON = "reservas.json"

    @classmethod
    def guardar_reservas(cls, reservas):
        datos = []
        for reserva in reservas:
            datos.append({
                "usuario": {
                    "nombre": reserva["usuario"].nombre,
                    "correo": reserva["usuario"].correo
                },
                "funcion": {
                    "pelicula": reserva["funcion"].pelicula.titulo,
                    "hora": reserva["funcion"].hora,
                    "sala": reserva["funcion"].sala.identificador
                },
                "asientos": reserva["asientos"]
            })
        with open(cls.RESERVAS_JSON, "w") as f:
            json.dump(datos, f, indent=4)

    @classmethod
    def cargar_reservas(cls, funciones):
        if not os.path.exists(cls.RESERVAS_JSON):
            return []

        with open(cls.RESERVAS_JSON, "r") as f:
            datos = json.load(f)

        reservas = []
        for r in datos:
            funcion = next(
                (f for f in funciones if f.pelicula.titulo == r["funcion"]["pelicula"]
                 and f.hora == r["funcion"]["hora"]
                 and f.sala.identificador == r["funcion"]["sala"]),
                None
            )
            if funcion:
                usuario = Usuario(r["usuario"]["nombre"], r["usuario"]["correo"])
                reservas.append({
                    "usuario": usuario,
                    "funcion": funcion,
                    "asientos": r["asientos"]
                })
        return reservas




