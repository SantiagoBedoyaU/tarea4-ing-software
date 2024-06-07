"""
Este módulo maneja la lógica principal para gestionar viajes y gastos.

Incluye funcionalidades para:
- Trabajar con fechas usando el módulo datetime.
- Registrar y manejar errores mediante el módulo logging.
- Convertir datos a y desde JSON.
- Hacer solicitudes HTTP con requests.
- Definir y manipular objetos Viaje y Gasto.
- Generar reportes con los datos de viajes y gastos.
- Manejar excepciones personalizadas para viajes y gastos.

Importaciones:
- datetime.date: Para manejar fechas relacionadas con los viajes.
- logging: Para registrar eventos, errores y mensajes de depuración.
- json: Para la serialización y deserialización de datos en formato JSON.
- requests: Para hacer solicitudes HTTP a servicios externos.
- Viaje: La clase que representa un viaje.
- Gasto: La clase que representa un gasto.
- Reporte: La clase que genera reportes sobre los viajes y gastos.
- ViajeException: Excepción personalizada para errores relacionados con viajes.
- GastoException: Excepción personalizada para errores relacionados con gastos.
"""

from datetime import date
import logging
import json
import requests
from models.viaje import Viaje
from models.gasto import Gasto
from models.reporte import Reporte
from exceptions.viaje_exception import ViajeException
from exceptions.gasto_exception import GastoException


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ViajesController:
    """clase controladora de la logica de negocio de viajes y gastos"""

    def registrar_viaje(
        self,
        destino: str,
        fecha_inicio: str,
        fecha_fin: str,
        presupuesto_diario: str,
    ):
        """crea un nuevo registro de viaje

        Args:
            destino (str): el lugar al que se viaja
            fecha_inicio (str): fecha de inicio del viaje
            fecha_fin (str): fecha de culminacion del vije
            presupuesto_diario (str): presupuesto diario del viaje (en moneda del destino)

        Returns:
            str: mensaje exitoso de creacion de viaje o log del error ocurrido en caso de fallar
        """
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

    def validar_destino(self, destino: str):
        """verifica que el destino sea permitido en la aplicacion

        Args:
            destino (str): lugar de destino del viaje

        Raises:
            ViajeException: excepcion lanzada en caso de no ser permitido el destino
        """
        if destino not in ["colombia", "usa", "europa"]:
            raise ViajeException("destino no aceptado")

    def validar_fechas(self, fecha_inicio: str, fecha_fin: str) -> tuple[date, date]:
        """valida que:
        1. Las fechas esten en el orden correcto de tiempo
        2. Las fechas no se crucen con ningun otro viaje

        Args:
            fecha_inicio (str): fecha de inicio del viaje
            fecha_fin (str): fecha de culminacion del viaje

        Raises:
            ViajeException: excepcion lanzada en caso de nu cumplir alguna de las verificaciones

        Returns:
            tuple[date,date]: un tupla con las fechas transformadas a tipo date
        """
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
        """valida que el metodo de pago de un gasto sea permitido en la aplicacion

        Args:
            metodo_pago (str): el metodo de pago de un gasto

        Raises:
            GastoException: excepcion lanzada en caso de no ser un metodo de pago permitido
        """
        if metodo_pago not in ["efectivo", "tarjeta"]:
            raise GastoException("metodo de pago no valido")

    def validar_tipo_gasto(self, tipo_gasto: str):
        """valida que el tipo de pago sea permitido en la aplicacion

        Args:
            tipo_gasto (str): el tipo de gasto realizado

        Raises:
            GastoException: Excepcion lanzada en caso de no permitirse el tipo de gasto
        """
        if tipo_gasto not in Gasto.tipos_gasto:
            raise GastoException("tipo de gasto no valido")

    def get_viaje(self, fecha: date):
        """obtiene el viaje que contenga la fecha especificada

        Args:
            fecha (date): la fecha que se usara para buscar el viaje

        Raises:
            ViajeException: excepcion lanzada en caso de no encontrar un viaje en la fecha indicada

        Returns:
            tuple[list[Viaje], Viaje]: lista de todos los viajes y el viaje encontrado para la fecha
        """
        viajes = self.get_viajes()
        for viaje in viajes:
            if viaje.fecha_inicio <= fecha <= viaje.fecha_fin:
                return viajes, viaje
        raise ViajeException("No hay ningun viaje en la fecha dada para el pago")

    def get_viajes(self) -> list[Viaje]:
        """obtiene el listado de viajes almacenados en el archivo viajes.json

        Returns:
            list[Viaje]: lista de viajes estructurados como objetos de tipo Viaje
        """
        try:
            with open("archivos/viajes.json", "r", encoding="utf-8") as f:
                viajes_data = json.load(f)
                return [Viaje.from_dict(viaje_data) for viaje_data in viajes_data]
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    def convertir_moneda(self, lugar: str, cantidad: float):
        """
        -verifica que la cantidad a convertir sea positiva\n
        -hace la conversion de moneda segun corresponda\n
        -consume una API para simular la conversion de moneda de Dolar/Euro a peso colombiano

        Args:
            lugar (str): el lugar en el que se hace el viaje o gasto
            cantidad (float): la cantidad a convertir de moneda del lugar a peso colombiano

        Raises:
            ValueError: excepcion lanzada en caso de tener una cantidad negativa

        Returns:
            float: la cantidad convertida a peso colombiano
        """
        if cantidad < 0:
            raise ValueError("no se admiten valores negativos")
        if lugar == "colombia":
            return cantidad
        try:
            valor_moneda = requests.get(
                "https://csrng.net/csrng/csrng.php?min=3500&max=4500", timeout=10
            ).json()[0]["random"]
            if lugar == "usa":
                return cantidad * valor_moneda
            valor_moneda += 200
            return cantidad * valor_moneda
        except requests.exceptions.Timeout as e:
            raise ValueError(
                "La solicitud para obtener la tasa de cambio ha expirado"
            ) from e

    def agregar_viaje(self, viaje: Viaje) -> list[Viaje]:
        """obtiene la lista de viajes y agrega a la misma el viaje dado

        Args:
            viaje (Viaje): el viaje a agregar

        Returns:
            list[Viaje]: la lista de viajes con el viaje agregado
        """
        viajes = self.get_viajes()
        viajes.append(viaje)
        return viajes

    def guardar_archivo(self, viajes: list[Viaje]):
        """reescribe el archivo viajes.json con la lista de viajes dada

        Args:
            viajes (list[Viaje]): la lista de viajes a guardar en el archivo viajes.json
        """
        with open("archivos/viajes.json", "w", encoding="utf-8") as f:
            json.dump([viaje.to_dict() for viaje in viajes], f, indent=4)

    def registrar_gasto(
        self, fecha: str, valor: float, metodo_pago: str, tipo_gasto: str
    ):
        """registra un nuevo gato en el viaje que contenga la fecha dada

        Args:
            fecha (str): la fecha del gasto realizado
            valor (float): a valor del gasto realizado (en moneda del lugar del viaje)
            metodo_pago (str): metodo de pago con el que se realizo el pago
            tipo_gasto (str): el tipo de gasto que se realizo

        Returns:
            str: mensaje exitoso de creacion del pago o log del error ocurrido en caso de fallar
        """
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
            mensaje = "Gasto registrado con exito"
            mensaje += f"\nBalance del dia {fecha.strftime('%Y-%m-%d')}:"
            mensaje += f"\n  Presupuesto diario: {viaje.presupuesto_diario}"
            mensaje += f"\n  Gastos: {viaje.presupuesto_diario-balance_dia}"
            mensaje += f"\n  Balance dia: {balance_dia}"
            return mensaje
        except (ViajeException, GastoException, ValueError) as e:
            logging.error(e)
            return ""

    def generar_reportes(self, viaje: Viaje):
        """llama al servicio de generar reporte de la clase Reporte para el viaje especificado

        Args:
            viaje (Viaje): el viaje sobre el cual se generan los reportes

        Returns:
            str: mensaje indicando la correcta generacion de los reportes
        """
        return Reporte.generar_reportes(viaje)
