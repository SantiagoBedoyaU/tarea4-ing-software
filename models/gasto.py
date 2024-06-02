from datetime import datetime

class Gasto:
    def __init__(self, fecha: datetime, valor: float, metodo_pago: str, tipo_pago: str) -> None:
        self.__fecha = fecha
        self.__valor = valor
        self.__metodo_pago = metodo_pago
        self.__tipo_pago = tipo_pago
    
    @property
    def fecha(self) -> datetime:
        return self.__fecha

    @property
    def valor(self) -> float:
        return self.__valor
    
    @property
    def metodo_pago(self) -> str:
        return self.__metodo_pago

    @property
    def tipo_pago(self) -> str:
        return self.__tipo_pago