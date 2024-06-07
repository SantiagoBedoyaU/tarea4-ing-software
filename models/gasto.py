"""
Este módulo proporciona una abstraccion Gasto al controlador.

Importaciones:
- datetime.date: para el manejo de fechas.
"""

from datetime import date


class Gasto:
    """clse que representa un gasto"""

    tipos_gasto = [
        "transporte",
        "alojamiento",
        "alimentacion",
        "entretenimiento",
        "compras",
    ]

    def __init__(
        self, fecha: date, valor: float, metodo_pago: str, tipo_gasto: str
    ) -> None:
        self.__fecha = fecha
        self.__valor = valor
        self.__metodo_pago = metodo_pago
        self.__tipo_gasto = tipo_gasto

    @property
    def fecha(self) -> date:
        """retorna el atributo __fecha

        Returns:
            str: fecha del gasto
        """
        return self.__fecha

    @property
    def valor(self) -> float:
        """retorna el atributo __valor

        Returns:
            str: valor del gasto
        """
        return self.__valor

    @property
    def metodo_pago(self) -> str:
        """retorna el atributo __metodo_pago

        Returns:
            str: metodo de pago del gasto
        """
        return self.__metodo_pago

    @property
    def tipo_gasto(self) -> str:
        """retorna el atributo __tipo_gasto

        Returns:
            str: tipo de gasto
        """
        return self.__tipo_gasto

    def to_dict(self):
        """reescribe el objeto gasto y sus atributos en formato dict

        Returns:
            dict: el objeto reescrito en formato dict
        """
        return {
            "fecha": self.fecha.strftime("%Y-%m-%d"),
            "valor": self.valor,
            "metodo_pago": self.metodo_pago,
            "tipo_gasto": self.tipo_gasto,
        }

    @staticmethod
    def from_dict(data: dict) -> "Gasto":
        """estructura un objeto de tipo Gasto a partir de un dict con los atributos

        Args:
            data (dict): el dict con los atributos del viaje

        Returns:
            Gasto: el objeto estructurado a partir del dict
        """
        fecha = date.fromisoformat(data["fecha"])
        return Gasto(fecha, data["valor"], data["metodo_pago"], data["tipo_gasto"])
