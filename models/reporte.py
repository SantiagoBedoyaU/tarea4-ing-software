class Reporte:
    def __init__(self, tipo_reporte: str, detalles: str) -> None:
        self.__tipo_reporte = tipo_reporte
        self.__detalles = detalles

    @property
    def tipo_reporte(self) -> str:
        return self.__tipo_reporte
    
    @property
    def detalles(self) -> str:
        return self.__detalles