"""Convert numbers to binary and hexadecimal formats 
from a file containing numerical data."""

import sys
import time
import re


def read_file(filename):
    """Reads a file, extracts numbers, and handles errors gracefully."""
    numbers = []  # Store extracted numbers
    invalid_lines = []  # Store invalid lines

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    invalid_lines.append(
                        f"Warning: Line {line_num} is empty."
                    )
                    continue

                extracted_numbers = [
                    int(number) for number in re.findall(r'-?\d+', line)
                ]
                if extracted_numbers:
                    numbers.extend(extracted_numbers)
                else:
                    invalid_lines.append(
                        f"Warning: No valid numbers on line {line_num}: "
                        f"{line}"
                    )

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return [], ["File not found."]
    except (IOError, OSError) as error:
        print(f"File error: {error}")
        return [], [f"File error: {error}"]

    return numbers, invalid_lines


def to_binary(number):
    """Manually converts a number to its binary representation."""
    if number == 0:
        return "0"
    binary = ""
    number = abs(number)  # Remove negative sign

    while number > 0:
        binary = str(number % 2) + binary
        number //= 2

    return binary  # Always return positive binary representation


def to_hexadecimal(number):
    """Manually converts a number to its hexadecimal representation."""
    if number == 0:
        return "0"
    hex_digits = "0123456789ABCDEF"
    hexadecimal = ""
    number = abs(number)  # Remove negative sign

    while number > 0:
        remainder = number % 16
        hexadecimal = hex_digits[remainder] + hexadecimal
        number //= 16

    return hexadecimal  # Always return positive hexadecimal


def write_results_to_file(conversions, invalid_lines, execution_time):
    """Writes conversion results and errors to a results file."""
    with open('ConvertionResults.txt', 'w', encoding='utf-8') as file:
        file.write("\nWarnings and Errors:\n")
        for line in invalid_lines:
            file.write(f"{line}\n")

        file.write("\nNumber Conversions:\n")
        for number, binary, hexa in conversions:
            file.write(
                f"Number: {number}, Binary: {binary}, Hex: {hexa}\n"
            )

        file.write(f"\nExecution Time: {execution_time:.2f} sec\n")


def main():
    """Main function to process file and convert numbers."""
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py <fileWithData.txt>")
        return

    filename = sys.argv[1]
    start_time = time.time()

    numbers, invalid_lines = read_file(filename)
    conversions = [
        (num, to_binary(num), to_hexadecimal(num)) for num in numbers
    ]
    execution_time = time.time() - start_time

    print("\nWarnings and Errors:")
    for line in invalid_lines:
        print(line)

    print("\nNumber Conversions:")
    for num, binary, hexa in conversions:
        print(f"Number: {num}, Binary: {binary}, Hex: {hexa}")

    print(f"\nExecution Time: {execution_time:.2f} sec")

    write_results_to_file(conversions, invalid_lines, execution_time)


if __name__ == "__main__":
    main()
