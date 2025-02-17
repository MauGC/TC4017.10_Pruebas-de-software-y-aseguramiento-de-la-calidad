"""
Unit tests for the Customer class in hotel_system.customer.

This module tests customer management operations including:
- Creating, deleting, modifying, and displaying customers.
- Handling file persistence issues.
"""

import unittest
import os
from unittest.mock import patch
from io import StringIO
from hotel_system.customer import Customer


class TestCustomer(unittest.TestCase):
    """Unit tests for the Customer class."""

    def setUp(self):
        """Creates a temporary test file before each test."""
        self.test_file = "test_customers.txt"
        Customer.DATA_FILE = self.test_file
        self.cleanup_file()

    def tearDown(self):
        """Deletes the test file after each test."""
        self.cleanup_file()

    def cleanup_file(self):
        """Deletes the test file if it exists."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_create_customer(self):
        """TC-01: Test creating a new customer."""
        Customer.create_customer("Juan Perez", "juan@example.com", "555-1234")
        customers = Customer.display_customers()
        self.assertIn("Juan Perez | juan@example.com | 555-1234", customers)

    def test_create_duplicate_customer(self):
        """TC-02: Test creating a duplicate customer (should fail)."""
        Customer.create_customer("Ana Gomez", "ana@example.com", "555-5678")
        result = Customer.create_customer("Ana Gomez",
                                          "other@example.com",
                                          "999-0000")
        self.assertEqual(result, "[ERROR] Customer already exists.")

    def test_delete_customer(self):
        """TC-03: Test deleting an existing customer."""
        Customer.create_customer("Carlos Ruiz", "car@exmple.com", "555-9876")
        result = Customer.delete_customer("Carlos Ruiz")
        self.assertEqual(result, "[INFO] Customer successfully deleted.")
        customers = Customer.display_customers()
        self.assertNotIn("Carlos Ruiz | car@exmple.com | 555-9876", customers)

    def test_delete_nonexistent_customer(self):
        """TC-04: Test deleting a non-existent customer (should fail)."""
        result = Customer.delete_customer("Does Not Exist")
        self.assertEqual(result, "[ERROR] Customer not found.")

    def test_display_empty_customers(self):
        """TC-05: Test if no customers are registered, the list is empty."""
        customers = Customer.display_customers()
        self.assertEqual(customers, [])

    def test_modify_customer_email(self):
        """TC-06: Test modifying the email of an existing customer."""
        Customer.create_customer("Maria Lopez", "maria@ample.com", "555-7777")
        Customer.modify_customer("Maria Lopez", email="new@ample.com")
        customers = Customer.display_customers()
        self.assertIn("Maria Lopez | new@ample.com | 555-7777", customers)

    def test_modify_customer_phone(self):
        """TC-07: Test modifying the phone number of an existing customer."""
        Customer.create_customer("Luis Torres", "lui@example.com", "555-8888")
        Customer.modify_customer("Luis Torres", phone="555-9999")
        customers = Customer.display_customers()
        self.assertIn("Luis Torres | lui@example.com | 555-9999", customers)

    def test_modify_nonexistent_customer(self):
        """TC-08: Test modifying a non-existent customer (should fail)."""
        result = Customer.modify_customer("Does Not Exist", email="x@exa.com")
        self.assertEqual(result, "[ERROR] Customer not found.")

    def test_modify_customer_both_fields(self):
        """TC-09: Test modifying both email and phone of a customer."""
        Customer.create_customer("Laura Vega", "laura@example.com", "555-6666")
        Customer.modify_customer("Laura Vega",
                                 email="new@example.com",
                                 phone="555-7777")
        customers = Customer.display_customers()
        self.assertIn("Laura Vega | new@example.com | 555-7777", customers)

    @patch("builtins.open", side_effect=IOError("Mocked IOError"))
    @patch("sys.stderr", new_callable=StringIO)  # ✅ Capture stderr instead
    def test_load_data_ioerror(self, _, __):
        """TC-11: Test handling IOError when reading the file."""
        result = Customer.load_data()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
