"""
Customer Management Module

This module provides functionality to manage customers using a TXT file
for data persistence. It allows creating, deleting, modifying, and
retrieving customer information.
"""

import os
import sys


class Customer:
    """Class representing a Customer stored in a TXT file."""
    DATA_FILE = "customers.txt"

    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone

    def to_string(self):
        """Converts customer information to a text string."""
        return f"{self.name} | {self.email} | {self.phone}\n"

    @classmethod
    def save_data(cls, customers):
        """Saves the list of customers to a TXT file."""
        try:
            with open(cls.DATA_FILE, "w", encoding="utf-8") as file:
                file.writelines(customers)
        except IOError:
            print("[ERROR] Unable to save customer file.",
                  file=sys.stderr,
                  flush=True)

    @classmethod
    def load_data(cls):
        """Loads the list of customers from a TXT file."""
        if not os.path.exists(cls.DATA_FILE):
            return []
        with open(cls.DATA_FILE, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]

    @classmethod
    def create_customer(cls, name, email, phone):
        """Creates a new customer and stores it in the file."""
        customers = cls.load_data()
        if any(c.startswith(name + " |") for c in customers):
            return "[ERROR] Customer already exists."
        new_customer = cls(name, email, phone)
        customers.append(new_customer.to_string())
        cls.save_data(customers)
        return "[INFO] Customer successfully created."

    @classmethod
    def delete_customer(cls, name):
        """Deletes a customer from the file."""
        customers = cls.load_data()
        filtered_customers = [
            c for c in customers if not c.startswith(name + " |")]
        if len(customers) == len(filtered_customers):
            return "[ERROR] Customer not found."
        cls.save_data(filtered_customers)
        return "[INFO] Customer successfully deleted."

    @classmethod
    def display_customers(cls):
        """Returns the list of customers in text format."""
        return cls.load_data()

    @classmethod
    def modify_customer(cls, name, email=None, phone=None):
        """Modifies an existing customer's details."""
        customers = cls.load_data()
        modified = False
        for i, customer in enumerate(customers):
            parts = customer.split(" | ")
            if parts[0] == name:
                if email:
                    parts[1] = email
                if phone:
                    parts[2] = phone
                customers[i] = " | ".join(parts)
                modified = True
        if not modified:
            return "[ERROR] Customer not found."
        cls.save_data(customers)
        return "[INFO] Customer successfully modified."
