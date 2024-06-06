from models.viaje import Viaje
from models.gasto import Gasto
from models.reporte import Reporte
from datetime import date
from exceptions.viaje_exception import ViajeException
from exceptions.gasto_exception import GastoException
import requests, json
import logging


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ViajesController:

    def registrar_viaje(
        self,
        destino: str,
        fecha_inicio: str,
        fecha_fin: str,
        presupuesto_diario: str,
    ):
        try:
            self.validar_destino(destino)
            fecha_inicio, fecha_fin = self.validar_fechas(fecha_inicio, fecha_fin)
            presupuesto_diario = self.convertir_moneda(
                destino, float(presupuesto_diario)
            )
            viaje = Viaje(destino, fecha_inicio, fecha_fin, presupuesto_diario)
            viajes = self.agregar_viaje(viaje)
            self.guardar_archivo(viajes)
            return "Viaje registrado con exito (ver archivo viajes.json)"
        except (ViajeException, ValueError) as e:
            logging.error(e)
            return ""

    def validar_destino(self, destino):
        if destino not in ["colombia", "usa", "europa"]:
            raise ViajeException("destino no aceptado")

    def validar_fechas(self, fecha_inicio: date, fecha_fin: date):
        fecha_inicio = date.fromisoformat(fecha_inicio)
        fecha_fin = date.fromisoformat(fecha_fin)
        if fecha_fin <= fecha_inicio:
            raise ViajeException("fechas incorrectas")
        viajes: list[Viaje] = self.get_viajes()
        for viaje in viajes:
            if (viaje.fecha_inicio <= fecha_inicio <= viaje.fecha_fin) or (
                viaje.fecha_inicio <= fecha_fin <= viaje.fecha_fin
            ):
                raise ViajeException("fechas cruzadas con otro viaje")
        return fecha_inicio, fecha_fin

    def validar_metodo_pago(self, metodo_pago: str):
        if metodo_pago not in ["efectivo", "tarjeta"]:
            raise GastoException("metodo de pago no valido")

    def validar_tipo_gasto(self, tipo_gasto: str):
        if tipo_gasto not in [
            "transporte",
            "alojamiento",
            "alimentacion",
            "entretenimiento",
            "compras",
        ]:
            raise GastoException("tipo de gasto no valido")

    def get_viaje(self, fecha: date):
        viajes = self.get_viajes()
        for viaje in viajes:
            if viaje.fecha_inicio <= fecha <= viaje.fecha_fin:
                return viajes, viaje
        raise ViajeException("No hay ningun viaje en la fecha dada para el pago")

    def get_viajes(self) -> list[Viaje]:
        try:
            with open("archivos/viajes.json", "r") as f:
                viajes_data = json.load(f)
                return [Viaje.from_dict(viaje_data) for viaje_data in viajes_data]
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    def convertir_moneda(self, lugar: str, cantidad: float):
        if cantidad < 0:
            raise ValueError("no se admiten valores negativos")
        if lugar == "colombia":
            return cantidad
        else:
            valor_moneda = requests.get(
                "https://csrng.net/csrng/csrng.php?min=3500&max=4500"
            ).json()[0]["random"]
            if lugar == "eeuu":
                return cantidad * valor_moneda
            else:
                valor_moneda += 200
                return cantidad * valor_moneda

    def agregar_viaje(self, viaje: Viaje) -> list[Viaje]:
        viajes = self.get_viajes()
        viajes.append(viaje)
        return viajes

    def guardar_archivo(self, viajes: list[Viaje]):
        with open("archivos/viajes.json", "w") as f:
            json.dump([viaje.to_dict() for viaje in viajes], f, indent=4)

    def registrar_gasto(
        self, fecha: str, valor: float, metodo_pago: str, tipo_gasto: str
    ):
        try:
            fecha: date = date.fromisoformat(fecha)
            viajes, viaje = self.get_viaje(fecha)
            self.validar_metodo_pago(metodo_pago)
            self.validar_tipo_gasto(tipo_gasto)
            valor = self.convertir_moneda(viaje.destino, float(valor))
            gasto = Gasto(fecha, valor, metodo_pago, tipo_gasto)
            viaje.agregar_gasto(gasto)
            for gasto in viaje.gastos:
                print(gasto.to_dict())
            balance_dia = viaje.get_balance_dia(fecha)
            self.guardar_archivo(viajes)
            mensaje = f"Gasto registrado con exito\nBalance del dia {fecha.strftime('%Y-%m-%d')}:\nPresupuesto diario: {viaje.presupuesto_diario}\nGastos: {viaje.presupuesto_diario-balance_dia}\nBalance dia: {balance_dia}"
            return mensaje
        except (ViajeException, GastoException) as e:
            logging.error(e)
            return ""

    def generar_reportes(self, viaje: Viaje):
        return Reporte.generar_reportes(viaje)
