from datetime import date
from .gasto import Gasto


class Viaje:
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
        return self.__destino

    @property
    def fecha_inicio(self) -> date:
        return self.__fecha_inicio

    @property
    def fecha_fin(self) -> date:
        return self.__fecha_fin

    @property
    def presupuesto_diario(self) -> float:
        return self.__presupuesto_diario

    @property
    def gastos(self) -> list[Gasto]:
        return self.__gastos

    def agregar_gasto(self, gasto: Gasto):
        self.__gastos.append(gasto)

    def get_balance_dia(self, fecha):
        balance = self.presupuesto_diario
        for gasto in self.get_gastos_dia(fecha):
            balance -= gasto.valor
        return balance

    def get_gastos_dia(self, fecha):
        gastos_dia: list[Gasto] = []
        for gasto in self.gastos:
            print(gasto.fecha == fecha)
            if gasto.fecha == fecha:
                gastos_dia.append(gasto)
        return gastos_dia

    def to_dict(self):
        return {
            "destino": self.destino,
            "fecha_inicio": self.fecha_inicio.strftime("%Y-%m-%d"),
            "fecha_fin": self.fecha_fin.strftime("%Y-%m-%d"),
            "presupuesto_diario": self.presupuesto_diario,
            "gastos": [gasto.to_dict() for gasto in self.gastos],
        }

    @staticmethod
    def from_dict(data):
        fecha_inicio = date.fromisoformat(data["fecha_inicio"])
        fecha_fin = date.fromisoformat(data["fecha_fin"])
        viaje = Viaje(
            data["destino"], fecha_inicio, fecha_fin, data["presupuesto_diario"]
        )
        for gasto_data in data["gastos"]:
            viaje.agregar_gasto(Gasto.from_dict(gasto_data))
        return viaje
