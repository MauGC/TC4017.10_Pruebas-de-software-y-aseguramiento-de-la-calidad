"""
This module contains tests for hotel.py module
"""

import unittest
import os
from hotel_system.hotel import Hotel


class TestHotel(unittest.TestCase):
    """Pruebas unitarias para la clase Hotel."""

    def setUp(self):
        """Configura el archivo de prueba antes de cada test."""
        self.test_file = "test_hotels.txt"
        Hotel.DATA_FILE = self.test_file

        # Crear archivo vacío
        with open(self.test_file, "w", encoding="utf-8"):
            pass

    def tearDown(self):
        """Elimina el archivo de prueba después de cada test."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_create_hotel(self):
        """Prueba la creación de un hotel."""
        result = Hotel.create_hotel("Hotel Test", "Ciudad A", "50", "100.5")
        self.assertEqual(result, "[INFO] Hotel creado exitosamente.")

    def test_create_duplicate_hotel(self):
        """Prueba la creación de un hotel duplicado."""
        Hotel.create_hotel("Hotel Doble", "Lugar X", "30", "75.0")
        result = Hotel.create_hotel("Hotel Doble", "Lugar X", "30", "75.0")
        self.assertEqual(result, "[ERROR] El hotel ya existe.")

    def test_modify_hotel(self):
        """Prueba la modificación de un hotel existente."""
        Hotel.create_hotel("Hotel Mod", "Lugar Z", "20", "50.0")
        result = Hotel.modify_hotel("Hotel Mod", "Nuevo Lugar", "40", "120.0")
        self.assertEqual(result, "[INFO] Hotel modificado exitosamente.")

    def test_modify_nonexistent_hotel(self):
        """Prueba la modificación de un hotel inexistente."""
        result = Hotel.modify_hotel("No Existe", "Ciudad X", "10", "90.0")
        self.assertEqual(result, "[ERROR] Hotel no encontrado.")

    def test_delete_hotel(self):
        """Prueba la eliminación de un hotel existente."""
        Hotel.create_hotel("Hotel Delete", "Ciudad B", "15", "60.0")
        result = Hotel.delete_hotel("Hotel Delete")
        self.assertEqual(result, "[INFO] Hotel eliminado exitosamente.")

    def test_delete_nonexistent_hotel(self):
        """Prueba la eliminación de un hotel inexistente."""
        result = Hotel.delete_hotel("No Existe")
        self.assertEqual(result, "[ERROR] Hotel no encontrado.")

    def test_display_hotels_empty(self):
        """Prueba que al no haber hoteles registrados, lo maneja correcto."""
        hotels = Hotel.display_hotels()
        self.assertEqual(hotels, [])

    def test_invalid_data_handling(self):
        """Prueba el manejo de datos inválidos en el archivo."""
        with open(self.test_file, "w", encoding="utf-8") as file:
            file.write("INVALID DATA LINE\n")

        hotels = Hotel.display_hotels()
        self.assertEqual(hotels, [])


if __name__ == "__main__":
    unittest.main()
