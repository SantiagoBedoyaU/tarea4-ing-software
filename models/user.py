from .viaje import Viaje

class User:
    def __init__(self, nombre: str, email: str) -> None:
        self.__nombre = nombre
        self.__email = email
        self.viajes: list[Viaje] = []
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @property
    def email(self) -> str:
        return self.__email