"ViajesController Unit Tests"

import os
from datetime import date
from unittest import TestCase

from controllers.viajes_controller import ViajesController
from exceptions.gasto_exception import GastoException
from exceptions.viaje_exception import ViajeException
from models.gasto import Gasto


class TestViajesController(TestCase):
    """ViajesController tests suite"""

    def cleanup(self):
        """Verifica si existe el archivo viajes.json y en caso de que exista lo elimina"""
        path = "archivos/viajes.json"
        if os.path.exists(path):
            os.remove(path)

    def test_registrar_viaje_success(self):
        """Test para el metodo registar_viaje"""
        self.cleanup()
        controller = ViajesController()
        result = controller.registrar_viaje(
            "colombia", "2024-06-07", "2024-06-08", 200_000
        )
        self.assertEqual(result, "Viaje registrado con exito (ver archivo viajes.json)")

    def test_registrar_viaje_destino_invalid(self):
        """Test para el metodo registar_destino"""
        self.cleanup()
        controller = ViajesController()
        result = controller.registrar_viaje(
            "destino", "2024-06-07", "2024-06-08", 200_000
        )
        assert result == ""

    def test_registrar_viaje_fechas_invalida(self):
        """Test para el metodo registrar_viaje"""
        self.cleanup()
        controller = ViajesController()
        result = controller.registrar_viaje(
            "colombia", "2024-06-07", "2024-06-06", 200_000
        )
        assert result == ""

    def test_validar_destino_success(self):
        """Test para el metodo registar_viaje"""
        controller = ViajesController()
        for destino in ["colombia", "usa", "europa"]:
            controller.validar_destino(destino)

    def test_validar_destino_invalido(self):
        """Test para el metodo registar_viaje"""
        controller = ViajesController()
        with self.assertRaises(ViajeException):
            controller.validar_destino("destino")

    def test_validar_fechas_success(self):
        """Test para el metodo registar_viaje"""
        self.cleanup()
        controller = ViajesController()
        fecha_inicio = "2024-06-07"
        fecha_fin = "2024-06-08"
        f1 = date.fromisoformat(fecha_inicio)
        f2 = date.fromisoformat(fecha_fin)
        result = controller.validar_fechas(fecha_inicio, fecha_fin)
        self.assertEqual(result, (f1, f2))

    def test_validar_fechas_iguales(self):
        """Test para el metodo registar_viaje"""
        self.cleanup()
        controller = ViajesController()
        fecha_inicio = "2024-06-07"
        fecha_fin = "2024-06-07"
        with self.assertRaises(ViajeException):
            controller.validar_fechas(fecha_inicio, fecha_fin)

    def test_validar_fechas_fecha_existente(self):
        """Test para el metodo registar_viaje"""
        controller = ViajesController()
        fecha_inicio = "2024-06-07"
        fecha_fin = "2024-06-08"
        with self.assertRaises(ViajeException):
            controller.validar_fechas(fecha_inicio, fecha_fin)

    def test_validar_metodo_pago_success(self):
        """Test para el metodo registar_viaje"""
        controller = ViajesController()
        for mp in ["efectivo", "tarjeta"]:
            controller.validar_metodo_pago(mp)

    def test_validar_metodo_pago_fail(self):
        """Test para el metodo registar_viaje"""
        controller = ViajesController()
        with self.assertRaises(GastoException):
            controller.validar_metodo_pago("nequi")

    def test_validator_tipo_gasto_success(self):
        """Test para el metodo registar_viaje"""
        controller = ViajesController()
        for tp in Gasto.tipos_gasto:
            controller.validar_tipo_gasto(tp)

    def test_validator_tipo_gasto_fail(self):
        """Test para el metodo registar_viaje"""
        controller = ViajesController()
        with self.assertRaises(GastoException):
            controller.validar_tipo_gasto("testing")

    def test_get_viaje(self):
        """Test para el metodo registar_viaje"""
        controller = ViajesController()
        controller.registrar_viaje("colombia", "2024-06-07", "2024-06-08", 200000)
        viajes, viaje = controller.get_viaje(date.fromisoformat("2024-06-07"))
        self.assertGreater(len(viajes), 0)
        self.assertEqual(
            viaje.to_dict(),
            {
                "destino": "colombia",
                "fecha_inicio": "2024-06-07",
                "fecha_fin": "2024-06-08",
                "presupuesto_diario": 200000.0,
                "gastos": [],
            },
        )
