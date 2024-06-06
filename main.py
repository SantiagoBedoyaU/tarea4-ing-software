from models.viaje import Viaje
from models.gasto import Gasto
from datetime import date
from controllers.viajes_controller import ViajesController

controller = ViajesController()


def main():
    while True:
        print("\n---------  Menú Principal ---------")
        print("1. Registrar viaje")
        print("2. Registrar gasto")
        print("3. Ver reportes")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "4":
            print("Finalizando la aplicacion")
            break
        opciones(opcion)


def opciones(opcion):
    if opcion == "1":
        registrar_viaje()
    elif opcion == "2":
        registrar_gasto()
    elif opcion == "3":
        ver_reportes()
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")


def registrar_viaje():
    destino = input("Ingrese el destino del viaje (colombia,usa o europa): ")
    fecha_inicio = input("Ingrese la fecha de inicio del viaje (YYYY-MM-DD): ")
    fecha_fin = input("Ingrese la fecha de fin del viaje (YYYY-MM-DD): ")
    presupuesto_diario = input(
        "Ingrese el presupuesto diario (en moneda del destino): "
    )

    print(
        controller.registrar_viaje(destino, fecha_inicio, fecha_fin, presupuesto_diario)
    )


def registrar_gasto():
    fecha = input("Ingrese la fecha del gasto (YYYY-MM-DD): ")
    valor = input("Ingrese el valor del gasto (en moneda del lugar del viaje): ")
    metodo_pago = input("Ingrese el método de pago (efectivo/tarjeta): ")
    tipo_gasto = input(
        "Ingrese el tipo de gasto (transporte,alojamiento,alimentación,entretenimiento,compras): "
    )
    print(controller.registrar_gasto(fecha, valor, metodo_pago, tipo_gasto))


def ver_reportes():
    viajes: list[Viaje] = controller.get_viajes()
    print("------ Para que viaje deseas ver sus reportes? ------")
    for i, viaje in enumerate(viajes, start=0):
        print(
            f"  {i}. Viaje entre las fechas {viaje.fecha_inicio} y {viaje.fecha_fin} en {viaje.destino}\n"
        )
    try:
        opcion = int(input("Seleccione una opcion: "))
        if 0 <= opcion < len(viajes):
            print(controller.generar_reportes(viajes[opcion]))
        else:
            print("Opcion incorrecta")
    except Exception:
        print("Error al seleccionar la opcion")


if __name__ == "__main__":
    main()
