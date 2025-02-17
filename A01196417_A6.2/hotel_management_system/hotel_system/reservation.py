"""
Reservation Management Module

This module provides functionality to manage reservations using a TXT file
for data persistence. It allows creating, deleting, and getting reservations.
"""

import os


class Reservation:
    """Clase que maneja las Reservaciones con persistencia en TXT."""
    DATA_FILE = "reservations.txt"

    def __init__(self, customer_name: str, hotel_name: str):
        self.customer_name = customer_name
        self.hotel_name = hotel_name

    def to_line(self):
        """Convierte la reserva en una línea de texto."""
        return f"{self.customer_name} | {self.hotel_name}\n"

    @classmethod
    def save_data(cls, reservations):
        """Guarda las reservaciones en un archivo de texto."""
        try:
            with open(cls.DATA_FILE, "w", encoding="utf-8") as file:
                file.writelines(reservations)
        except IOError:
            print("[ERROR] No se pudo guardar el archivo de reservaciones.")

    @classmethod
    def load_data(cls):
        """Carga las reservaciones desde el archivo de texto."""
        if not os.path.exists(cls.DATA_FILE):
            return []

        try:
            with open(cls.DATA_FILE, "r", encoding="utf-8") as file:
                return [line.strip() for line in file.readlines()]
        except IOError:
            print("[ERROR] No se pudo leer el archivo de reservaciones.")
            return []

    @classmethod
    def create_reservation(cls, customer_name, hotel_name):
        """Crea una nueva reservación si no existe una igual."""
        reservations = cls.load_data()
        new_reservation = f"{customer_name} | {hotel_name}"

        if new_reservation in reservations:
            return "[ERROR] La reservación ya existe."

        reservations.append(new_reservation)
        cls.save_data([res + "\n" for res in reservations])
        return "[INFO] Reservación creada exitosamente."

    @classmethod
    def cancel_reservation(cls, customer_name, hotel_name):
        """Cancela una reservación existente."""
        reservations = cls.load_data()
        updated_reservations = [
            r for r in reservations if r != f"{customer_name} | {hotel_name}"
        ]

        if len(updated_reservations) == len(reservations):
            return "[ERROR] Reservación no encontrada."

        cls.save_data([res + "\n" for res in updated_reservations])
        return "[INFO] Reservación cancelada exitosamente."

    @classmethod
    def display_reservations(cls):
        """Devuelve la lista de reservaciones."""
        return cls.load_data()
