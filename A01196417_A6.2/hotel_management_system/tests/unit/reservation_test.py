"""
This module contains tests for reservation.py module
"""

import unittest
import os
import io
from unittest.mock import patch, mock_open
from hotel_system.reservation import Reservation


class TestReservation(unittest.TestCase):
    """Pruebas unitarias para la clase Reservation."""

    def setUp(self):
        """Configura un archivo de prueba antes de cada test."""
        self.test_file = "test_reservations.txt"
        Reservation.DATA_FILE = self.test_file
        self.reservation = Reservation("John Doe", "Grand Hotel")

        # Crear archivo vacío
        with open(self.test_file, "w", encoding="utf-8"):
            pass

    def tearDown(self):
        """Elimina el archivo de prueba después de cada test."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_create_reservation(self):
        """TC-01: Crear una reservación nueva."""
        result = Reservation.create_reservation("Juan Perez", "Hotel Central")
        self.assertEqual(result, "[INFO] Reservación creada exitosamente.")

    def test_create_duplicate_reservation(self):
        """TC-02: Crear una reservación duplicada."""
        Reservation.create_reservation("Juan Perez", "Hotel Central")
        result = Reservation.create_reservation("Juan Perez", "Hotel Central")
        self.assertEqual(result, "[ERROR] La reservación ya existe.")

    def test_cancel_reservation(self):
        """TC-03: Cancelar una reservación existente."""
        Reservation.create_reservation("Juan Perez", "Hotel Central")
        result = Reservation.cancel_reservation("Juan Perez", "Hotel Central")
        self.assertEqual(result, "[INFO] Reservación cancelada exitosamente.")

    def test_cancel_nonexistent_reservation(self):
        """TC-04: Cancelar una reservación inexistente."""
        result = Reservation.cancel_reservation("Ana Gomez", "Hotel Sunset")
        self.assertEqual(result, "[ERROR] Reservación no encontrada.")

    def test_display_reservations(self):
        """TC-05: Mostrar reservaciones."""
        Reservation.create_reservation("Carlos Lopez", "Hotel Plaza")
        Reservation.create_reservation("Maria Ruiz", "Hotel Beach")
        reservations = Reservation.display_reservations()
        self.assertIn("Carlos Lopez | Hotel Plaza", reservations)
        self.assertIn("Maria Ruiz | Hotel Beach", reservations)

    def test_load_invalid_file(self):
        """TC-06: Intentar cargar un archivo corrupto o inexistente."""
        Reservation.DATA_FILE = "non_existing_file.txt"
        reservations = Reservation.load_data()
        self.assertEqual(reservations, [])

    def test_create_multiple_reservations(self):
        """TC-07: Crear múltiples reservaciones."""
        data = [("Carlos Lopez", "Hotel Plaza"), ("Maria Ruiz", "Hotel Beach")]
        for customer, hotel in data:
            Reservation.create_reservation(customer, hotel)
        reservations = Reservation.display_reservations()
        self.assertEqual(len(reservations), 2)

    def test_reservation_attributes(self):
        """Prueba que los atributos se asignan correctamente."""
        self.assertEqual(self.reservation.customer_name, "John Doe")
        self.assertEqual(self.reservation.hotel_name, "Grand Hotel")

    def test_to_line_format(self):
        """Prueba que el método to_line genera el formato correcto."""
        expected_line = "John Doe | Grand Hotel\n"
        self.assertEqual(self.reservation.to_line(), expected_line)

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_save_data_ioerror(self, mock_stdout, mock_file):
        """Prueba el manejo de IOError al guardar el archivo."""
        mock_file.side_effect = IOError  # Simulamos error al abrir el archivo
        Reservation.save_data(["Some data"])

        self.assertIn(
            "[ERROR] No se pudo guardar el archivo de reservaciones.",
            mock_stdout.getvalue()
        )

    @patch("builtins.open", side_effect=IOError)
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_load_data_ioerror(self, mock_stdout, _):
        """Prueba el manejo de IOError al leer el archivo."""
        result = Reservation.load_data()
        self.assertEqual(result, [])

        self.assertIn(
            "[ERROR] No se pudo leer el archivo de reservaciones.",
            mock_stdout.getvalue()
        )


if __name__ == "__main__":
    unittest.main()
