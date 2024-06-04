from datetime import datetime
from .gasto import Gasto

class Viaje:
    def __init__(self, destino: str, fecha_inicio: datetime, fecha_fin: datetime, presupuesto:float) -> None:
        self.__destino = destino
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__presupuesto = presupuesto
        self.__gastos: list[Gasto] = []

    @property
    def destino(self) -> str:
        return self.__destino

    @property
    def fecha_inicio(self) -> datetime:
        return self.__fecha_inicio
    
    @property
    def fecha_fin(self) -> datetime:
        return self.__fecha_fin
    
    @property
    def presupuesto(self) -> float:
        return self.__presupuesto
    
    @property
    def gastos(self) -> list[Gasto]:
        return self.__gastos

    def agregar_gasto(self, gasto: Gasto):
        self.__gastos.append(gasto)

    def get_balance_dia(self):
        raise NotImplementedError()

    def get_gastos_dia(self):
        raise NotImplementedError()
    