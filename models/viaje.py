"""
Este módulo proporciona una abstraccion Viaje al controlador.

Importaciones:
- datetime.date: para el manejo de fechas.
- Gasto: Clase que representa un gasto en el sistema de viajes.
"""

from datetime import date
from .gasto import Gasto


class Viaje:
    """
    clase que representa un viaje
    """

    def __init__(
        self,
        destino: str,
        fecha_inicio: date,
        fecha_fin: date,
        presupuesto_diario: float,
    ) -> None:
        self.__destino = destino
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__presupuesto_diario = presupuesto_diario
        self.__gastos: list[Gasto] = []

    @property
    def destino(self) -> str:
        """retorna el atributo __destino

        Returns:
            str: destino del viaje
        """
        return self.__destino

    @property
    def fecha_inicio(self) -> date:
        """retorna el atributo __fecha_inico

        Returns:
            str: fecha de inicio del viaje
        """
        return self.__fecha_inicio

    @property
    def fecha_fin(self) -> date:
        """retorna el atributo __fecha_fin

        Returns:
            str: fecha de culminacion del viaje
        """
        return self.__fecha_fin

    @property
    def presupuesto_diario(self) -> float:
        """retorna el atributo __presupuesto_diario

        Returns:
            str: presupuesto diario del viaje
        """
        return self.__presupuesto_diario

    @property
    def gastos(self) -> list[Gasto]:
        """retorna el atributo __gastos

        Returns:
            list[Gasto]: listado de gastos del viaje
        """
        return self.__gastos

    def agregar_gasto(self, gasto: Gasto):
        """añade a la lista de gastos del viaje el gasto dado

        Args:
            gasto (Gasto): el gasto a añador al viaje
        """
        self.__gastos.append(gasto)

    def get_balance_dia(self, fecha):
        """calcula la diferencia entre el presupuesto diario y los gastos de la fecha dada

        Args:
            fecha (_type_): la fecha sobre la que se calcula el balance

        Returns:
            float: balance de la fecha dada
        """
        balance = self.presupuesto_diario
        for gasto in self.get_gastos_dia(fecha):
            balance -= gasto.valor
        return balance

    def get_gastos_dia(self, fecha: date) -> list[Gasto]:
        """obtiene los gastos de una fecha dada

        Args:
            fecha (date): la fecha de los gastos a buscar

        Returns:
            list[Gasto]: listado de gastos de la fecha dada
        """
        gastos_dia: list[Gasto] = []
        for gasto in self.gastos:
            print(gasto.fecha == fecha)
            if gasto.fecha == fecha:
                gastos_dia.append(gasto)
        return gastos_dia

    def to_dict(self):
        """reescribe el objeto viaje y sus atributos en formato dict

        Returns:
            dict: el objeto reescrito en formato dict
        """
        return {
            "destino": self.destino,
            "fecha_inicio": self.fecha_inicio.strftime("%Y-%m-%d"),
            "fecha_fin": self.fecha_fin.strftime("%Y-%m-%d"),
            "presupuesto_diario": self.presupuesto_diario,
            "gastos": [gasto.to_dict() for gasto in self.gastos],
        }

    @staticmethod
    def from_dict(data: dict) -> "Viaje":
        """estructura un objeto de tipo Viaje a partir de un dict con los atributos

        Args:
            data (dict): el dict con los atributos del viaje

        Returns:
            Viaje: el objeto estructurado a partir del dict
        """
        fecha_inicio = date.fromisoformat(data["fecha_inicio"])
        fecha_fin = date.fromisoformat(data["fecha_fin"])
        viaje = Viaje(
            data["destino"], fecha_inicio, fecha_fin, data["presupuesto_diario"]
        )
        for gasto_data in data["gastos"]:
            viaje.agregar_gasto(Gasto.from_dict(gasto_data))
        return viaje
