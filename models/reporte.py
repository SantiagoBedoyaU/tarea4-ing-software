""" 
Este modulo trabaja como servicio de generacion de reportes para viajes

Incluye funcionalidades para:
- generar reportes por dias y por tipos de gastos para un viaje

Importaciones:
- datetime.timedelta: util para iterar entre dos fechas para la generacion de reportes por dias
- Viaje: La clase que representa un viaje.
- Gasto: La clase que representa un gasto.
"""

from datetime import timedelta
from models.gasto import Gasto
from models.viaje import Viaje


class Reporte:
    """clase que brinda los servicios de generacion de reportes"""

    @staticmethod
    def generar_reportes(viaje: Viaje):
        """genera un reporte general para el viaje dado y sobreescribe el archivo reporte.txt

        Args:
            viaje (Viaje): el viaje sobre el cual generar el reporte

        Returns:
            str: mensaje indicando la correcta generacion de los reportes
        """
        contenido = "--- Reporte de gastos para el viaje entre las fechas "
        contenido += (
            f"{viaje.fecha_inicio} y {viaje.fecha_fin} en {viaje.destino} ---\n"
        )
        gasto_total = sum(gasto.valor for gasto in viaje.gastos)
        if len(viaje.gastos) > 0:
            contenido += Reporte.reporte_dias(viaje)
            contenido += Reporte.reporte_tipos(viaje)
        else:
            contenido += "No hay gastos registrados para este viaje\n"
        contenido += f"Gastos totales del viaje : {gasto_total}\n"
        with open("archivos/reporte.txt", "w", encoding="utf-8") as reporte:
            reporte.write(contenido)
        return "Reporte generado con exito (ver archivo reporte.txt)"

    @staticmethod
    def reporte_dias(viaje: Viaje):
        """genera el reporte de gastos por dias del viaje

        Args:
            viaje (Viaje): el viaje sobre el cual se genera el reporte

        Returns:
            str: contenido del reporte por dias
        """
        delta = timedelta(days=1)
        fecha = viaje.fecha_inicio
        contenido = "\nReporte de gastos por dias:\n"
        while fecha <= viaje.fecha_fin:
            total_dia = 0
            total_dia_efectivo = 0
            total_dia_tarjeta = 0
            for gasto in viaje.gastos:
                if gasto.fecha == fecha:
                    if gasto.metodo_pago == "efectivo":
                        total_dia_efectivo += gasto.valor
                        total_dia += gasto.valor
                    else:
                        total_dia_tarjeta += gasto.valor
                        total_dia += gasto.valor
            contenido += f"  Gastos {fecha}:\n"
            contenido += f"    Efectivo: {total_dia_efectivo}\n"
            contenido += f"    Tarjeta : {total_dia_tarjeta}\n"
            contenido += f"    Total   : {total_dia}\n\n"
            fecha += delta
        return contenido

    @staticmethod
    def reporte_tipos(viaje: Viaje):
        """genera el reporte de gastos por tipos de gasto del viaje

        Args:
            viaje (Viaje): el viaje sobre el cual se genera el reporte

        Returns:
            str: contenido del reporte por tipos
        """
        contenido = "\nReporte de gastos por tipo:\n"
        for tipo_gasto in Gasto.tipos_gasto:
            total_tipo = 0
            total_tipo_efectivo = 0
            total_tipo_tarjeta = 0
            for gasto in viaje.gastos:
                if gasto.tipo_gasto == tipo_gasto:
                    if gasto.metodo_pago == "efectivo":
                        total_tipo_efectivo += gasto.valor
                        total_tipo += gasto.valor
                    else:
                        total_tipo_tarjeta += gasto.valor
                        total_tipo += gasto.valor
            contenido += f"  Gastos en {tipo_gasto}:\n"
            contenido += f"    Efectivo: {total_tipo_efectivo}\n"
            contenido += f"    Tarjeta : {total_tipo_tarjeta}\n"
            contenido += f"    Total   : {total_tipo}\n\n"
        return contenido
