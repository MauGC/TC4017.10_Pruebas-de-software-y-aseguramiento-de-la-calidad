"""
Hotel Management Module

This module provides functionality to manage hotels using a TXT file
for data persistence. It allows creating, deleting, modifying, and
retrieving hotel information.
"""

import os


class Hotel:
    """Clase que maneja la información de los hoteles."""
    DATA_FILE = "hotels.txt"

    def __init__(self, name, location, rooms, price):
        self.name = name
        self.location = location
        self.rooms = rooms
        self.price = price

    def to_string(self):
        """Convierte atributos en un string formateado para guardar en TXT."""
        return f"{self.name}|{self.location}|{self.rooms}|{self.price}\n"

    @classmethod
    def save_data(cls, hotels):
        """Guarda la lista de hoteles en un archivo TXT."""
        with open(cls.DATA_FILE, "w", encoding="utf-8") as file:
            file.writelines(hotels)

    @classmethod
    def load_data(cls):
        """Carga los hoteles desde el archivo TXT y maneja datos inválidos."""
        if not os.path.exists(cls.DATA_FILE):
            return []

        hotels = []
        try:
            with open(cls.DATA_FILE, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("|")
                    if len(parts) == 4:
                        hotels.append(parts)
                    else:
                        print(f"[ERROR] Invalid data format: {line.strip()}")
        except (OSError, ValueError) as error:
            print(f"[ERROR] Failed to load hotel data: {error}")
            return []
        return hotels

    @classmethod
    def create_hotel(cls, name, location, rooms, price):
        """Crea un nuevo hotel y lo guarda en el archivo."""
        hotels = cls.load_data()

        # Verificar si el hotel ya existe
        if any(hotel[0] == name for hotel in hotels):
            return "[ERROR] El hotel ya existe."

        new_hotel = f"{name}|{location}|{rooms}|{price}\n"
        hotels.append(new_hotel)
        cls.save_data(hotels)
        return "[INFO] Hotel creado exitosamente."

    @classmethod
    def modify_hotel(cls, name, location=None, rooms=None, price=None):
        """Modifica la información de un hotel existente."""
        hotels = cls.load_data()
        found = False

        for i, hotel in enumerate(hotels):
            if hotel[0] == name:
                if location:
                    hotel[1] = location
                if rooms:
                    hotel[2] = rooms
                if price:
                    hotel[3] = price
                hotels[i] = "|".join(hotel) + "\n"
                found = True

        if found:
            cls.save_data(hotels)
            return "[INFO] Hotel modificado exitosamente."
        return "[ERROR] Hotel no encontrado."

    @classmethod
    def delete_hotel(cls, name):
        """Elimina un hotel por nombre."""
        hotels = cls.load_data()
        new_hotels = [hotel for hotel in hotels if hotel[0] != name]

        if len(new_hotels) == len(hotels):
            return "[ERROR] Hotel no encontrado."

        cls.save_data(["|".join(hotel) + "\n" for hotel in new_hotels])
        return "[INFO] Hotel eliminado exitosamente."

    @classmethod
    def display_hotels(cls):
        """Muestra la lista de hoteles disponibles."""
        hotels = cls.load_data()
        return hotels if hotels else []
