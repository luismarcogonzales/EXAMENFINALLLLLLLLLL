import json


class Persona:
    def __init__(self, nombre, DNI):
        self.nombre = nombre
        self.DNI = DNI


class Comprador(Persona):
    def __init__(self, nombre, DNI):
        super().__init__(nombre, DNI)


class Organizador(Persona):
    def __init__(self, nombre, DNI):
        super().__init__(nombre, DNI)


from abc import ABC, abstractmethod

class Evento(ABC):
    @abstractmethod
    def mostrar_detalle(self):
        pass


class EventoParrillada(Evento):
    def __init__(self, nombre, fecha, lugar, costo, descripcion):
        self.nombre = nombre
        self.fecha = fecha
        self.lugar = lugar
        self.costo = costo
        self.descripcion = descripcion

    def mostrar_detalle(self):
        return f"Evento de Parrillada: {self.nombre}, Fecha: {self.fecha}, Lugar: {self.lugar}, Costo: ${self.costo}, Descripción: {self.descripcion}"

class EventoVIP(Evento):
    def __init__(self, nombre, fecha, lugar, costo, descripcion, beneficios):
        self.nombre = nombre
        self.fecha = fecha
        self.lugar = lugar
        self.costo = costo
        self.descripcion = descripcion
        self.beneficios = beneficios

    def mostrar_detalle(self):
        return f"Evento VIP: {self.nombre}, Fecha: {self.fecha}, Lugar: {self.lugar}, Costo: ${self.costo}, Descripción: {self.descripcion}, Beneficios: {self.beneficios}"


class Venta:
    def __init__(self, comprador, evento):
        self.comprador = comprador
        self.evento = evento

    def calcular_total(self):
        return self.evento.costo


class GestorVentas:
    def __init__(self):
        self.ventas = []

    def agregar_venta(self, venta):
        self.ventas.append(venta)

    def reporte_ventas_totales(self):
        total = sum(venta.calcular_total() for venta in self.ventas)
        return f"Total de ventas: ${total}"

    def guardar_ventas(self, archivo):
        with open(archivo, 'w') as f:
            json.dump([venta.__dict__ for venta in self.ventas], f)

    def cargar_ventas(self, archivo):
        try:
            with open(archivo, 'r') as f:
                data = json.load(f)
                self.ventas = [Venta(Comprador(**venta['comprador']), Evento(**venta['evento'])) for venta in data]
        except FileNotFoundError:
            raise ArchivoNoEncontradoError("El archivo especificado no se encontró.")
        except json.JSONDecodeError:
            raise ArchivoInvalidoError("El archivo especificado no es un archivo JSON válido.")

    def crear_evento_parrillada(self, nombre, fecha, lugar, costo, descripcion):
        evento = EventoParrillada(nombre, fecha, lugar, costo, descripcion)
        return evento

    def crear_evento_vip(self, nombre, fecha, lugar, costo, descripcion, beneficios):
        evento = EventoVIP(nombre, fecha, lugar, costo, descripcion, beneficios)
        return evento

    def eliminar_evento(self, evento):
        self.eventos.remove(evento)


class EventoAgotadoError(Exception):
    def __init__(self, mensaje="Lo siento, el evento seleccionado está agotado."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class DatosInvalidosError(Exception):
    def __init__(self, mensaje="Los datos ingresados no son válidos."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ArchivoNoEncontradoError(Exception):
    def __init__(self, mensaje="El archivo especificado no se encontró."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ArchivoInvalidoError(Exception):
    def __init__(self, mensaje="El archivo especificado no es un archivo JSON válido."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


# Interfaz de usuario
def menu_principal():
    print("Bienvenido al sistema de gestión de ventas de eventos de comida")
    print("1. Comprar entrada")
    print("2. Reporte de ventas totales")
    print("3. Guardar ventas en archivo")
    print("4. Cargar ventas desde archivo")
    print("5. Crear evento de Parrillada")
    print("6. Crear evento VIP")
    print("7. Eliminar evento")
    print("8. Salir")

def menu_comprar_entrada(eventos):
    print("Seleccione un evento para comprar una entrada:")
    for i, evento in enumerate(eventos, 1):
        print(f"{i}. {evento.mostrar_detalle()}")

def main():
    eventos = [EventoParrillada("Parrillada de Verano", "15/07/2024", "Parque Central", 50, "Disfruta de una parrillada al aire libre"),
               EventoVIP("Noche VIP", "20/07/2024", "Hotel de Lujo", 100, "Una noche exclusiva con música en vivo", "Barra libre y acceso exclusivo")]

    gestor_ventas = GestorVentas()

    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_comprar_entrada(eventos)
            seleccion = input("Seleccione un evento: ")
            try:
                seleccion = int(seleccion)
                if 1 <= seleccion <= len(eventos):
                    comprador_nombre = input("Ingrese su nombre: ")
                    comprador_DNI = input("Ingrese su DNI: ")
                    comprador = Comprador(comprador_nombre, comprador_DNI)
                    venta = Venta(comprador, eventos[seleccion - 1])
                    gestor_ventas.agregar_venta(venta)
                    print("¡Entrada comprada exitosamente!")
                else:
                    print("Selección no válida.")
            except ValueError:
                print("Entrada no válida.")
            except EventoAgotadoError:
                print("Lo siento, el evento seleccionado está agotado.")
            except DatosInvalidosError:
                print("Los datos ingresados no son válidos.")

        elif opcion == "2":
            print(gestor_ventas.reporte_ventas_totales())

        elif opcion == "3":
            archivo = input("Ingrese el nombre del archivo para guardar las ventas: ")
            try:
                gestor_ventas.guardar_ventas(archivo)
                print("¡Ventas guardadas exitosamente!")
            except ArchivoInvalidoError as e:
                print(f"Error al guardar las ventas: {e}")

        elif opcion == "4":
            archivo = input("Ingrese el nombre del archivo para cargar las ventas: ")
            try:
                gestor_ventas.cargar_ventas(archivo)
                print("¡Ventas cargadas exitosamente!")
            except ArchivoNoEncontradoError as e:
                print(f"Error al cargar las ventas: {e}")
            except ArchivoInvalidoError as e:
                print(f"Error al cargar las ventas: {e}")

        elif opcion == "5":
            nombre = input("Ingrese el nombre del evento de Parrillada: ")
            fecha = input("Ingrese la fecha del evento (DD/MM/AAAA): ")
            lugar = input("Ingrese el lugar del evento: ")
            costo = float(input("Ingrese el costo del evento: "))
            descripcion = input("Ingrese la descripción del evento: ")
            evento_parrillada = gestor_ventas.crear_evento_parrillada(nombre, fecha, lugar, costo, descripcion)
            eventos.append(evento_parrillada)
            print("Evento de Parrillada creado exitosamente.")

        elif opcion == "6":
            nombre = input("Ingrese el nombre del evento VIP: ")
            fecha = input("Ingrese la fecha del evento (DD/MM/AAAA): ")
            lugar = input("Ingrese el lugar del evento: ")
            costo = float(input("Ingrese el costo del evento: "))
            descripcion = input("Ingrese la descripción del evento: ")
            beneficios = input("Ingrese los beneficios del evento VIP: ")
            evento_vip = gestor_ventas.crear_evento_vip(nombre, fecha, lugar, costo, descripcion, beneficios)
            eventos.append(evento_vip)
            print("Evento VIP creado exitosamente.")

        elif opcion == "7":
            menu_comprar_entrada(eventos)
            seleccion = input("Seleccione el evento que desea eliminar: ")
            try:
                seleccion = int(seleccion)
                if 1 <= seleccion <= len(eventos):
                    evento_eliminado = eventos.pop(seleccion - 1)
                    gestor_ventas.eliminar_evento(evento_eliminado)
                    print("Evento eliminado exitosamente.")
                else:
                    print("Selección no válida.")
            except ValueError:
                print("Entrada no válida.")

        elif opcion == "8":
            print("¡Gracias por utilizar nuestro sistema!")
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()