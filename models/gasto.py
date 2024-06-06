from datetime import date


class Gasto:
    def __init__(
        self, fecha: date, valor: float, metodo_pago: str, tipo_gasto: str
    ) -> None:
        self.__fecha = fecha
        self.__valor = valor
        self.__metodo_pago = metodo_pago
        self.__tipo_gasto = tipo_gasto

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def valor(self) -> float:
        return self.__valor

    @property
    def metodo_pago(self) -> str:
        return self.__metodo_pago

    @property
    def tipo_gasto(self) -> str:
        return self.__tipo_gasto

    def to_dict(self):
        return {
            "fecha": self.fecha.strftime("%Y-%m-%d"),
            "valor": self.valor,
            "metodo_pago": self.metodo_pago,
            "tipo_gasto": self.tipo_gasto,
        }

    @staticmethod
    def from_dict(data):
        fecha = date.fromisoformat(data["fecha"])
        return Gasto(fecha, data["valor"], data["metodo_pago"], data["tipo_gasto"])
