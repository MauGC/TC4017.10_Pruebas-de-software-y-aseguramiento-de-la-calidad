from hotel_system import Hotel, Customer, Reservation

if __name__ == "__main__":
    # Ejemplo de uso
    Hotel.create_hotel("Hotel Plaza", "NYC", 100, "150.00")
    Customer.create_customer("John Doe", "johndoe@example.com", "1234567890")
    Reservation.create_reservation("John Doe", "Hotel Plaza")

    print("Hoteles:", Hotel.display_hotels())
    print("Clientes:", Customer.display_customers())
    print("Reservaciones:", Reservation.display_reservations())
