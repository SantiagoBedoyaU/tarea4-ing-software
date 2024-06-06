from models.viaje import Viaje
from datetime import timedelta


class Reporte:
    @staticmethod
    def generar_reportes(viaje: Viaje):
        contenido = f"--- Reporte de gastos para el viaje entre las fechas {viaje.fecha_inicio} y {viaje.fecha_fin} en {viaje.destino} ---\n"
        gasto_total = sum(gasto.valor for gasto in viaje.gastos)
        if len(viaje.gastos) > 0:
            contenido += Reporte.reporte_dias(viaje)
            contenido += Reporte.reporte_tipos(viaje)
        else:
            contenido += "No hay gastos registrados para este viaje\n"
        contenido += f"Gastos totales del viaje : {gasto_total}\n"
        with open("archivos/reporte.txt", "w") as reporte:
            reporte.write(contenido)
        return "Reporte generado con exito (ver archivo reporte.txt)"

    @staticmethod
    def reporte_dias(viaje: Viaje):
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
        contenido = "\nReporte de gastos por tipo:\n"
        for tipo_gasto in [
            "transporte",
            "alojamiento",
            "alimentacion",
            "entretenimiento",
            "compras",
        ]:
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
