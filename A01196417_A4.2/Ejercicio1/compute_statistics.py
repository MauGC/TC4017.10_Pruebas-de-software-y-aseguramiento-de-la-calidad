"""Compute statistics (mean, median, mode, variance, and std dev) 
from numerical data in a file."""

import re
import sys
import time


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
                    float(num) for num in re.findall(r'-?\d+\.?\d*', line)
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


def compute_statistics(numbers):
    """Compute mean, median, mode, variance, and std dev manually."""
    if not numbers:
        return {}

    count = len(numbers)
    mean = sum(numbers) / count

    # Median calculation
    sorted_numbers = sorted(numbers)
    if count % 2 == 0:
        median = (
            sorted_numbers[count // 2 - 1] + sorted_numbers[count // 2]
        ) / 2
    else:
        median = sorted_numbers[count // 2]

    # Mode calculation
    freq = {}
    for num in numbers:
        freq[num] = freq.get(num, 0) + 1
    max_freq = max(freq.values())
    mode = [key for key, val in freq.items() if val == max_freq]

    # Variance & Standard Deviation
    variance = sum((x - mean) ** 2 for x in numbers) / count
    std_dev = variance ** 0.5

    return {
        "mean": mean,
        "median": median,
        "mode": mode,
        "variance": variance,
        "std_dev": std_dev,
    }


def write_results_to_file(stats, invalid_lines, execution_time):
    """Writes statistics and errors to a results file."""
    with open('StatisticsResults.txt', 'w', encoding='utf-8') as file:
        file.write("\nWarnings and Errors:\n")
        for line in invalid_lines:
            file.write(f"{line}\n")

        file.write("\nDescriptive Statistics:\n")
        for key, value in stats.items():
            file.write(f"{key.capitalize()}: {value}\n")

        file.write(f"\nExecution Time: {execution_time:.2f} sec\n")


def main():
    """Main function to process file and compute statistics."""
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py <fileWithData.txt>")
        return

    filename = sys.argv[1]
    start_time = time.time()

    numbers, invalid_lines = read_file(filename)
    stats = compute_statistics(numbers)
    execution_time = time.time() - start_time

    print("\nWarnings and Errors:")
    for line in invalid_lines:
        print(line)

    print("\nDescriptive Statistics:")
    for key, value in stats.items():
        print(f"{key.capitalize()}: {value}")

    print(f"\nExecution Time: {execution_time:.2f} sec")

    write_results_to_file(stats, invalid_lines, execution_time)


if __name__ == "__main__":
    main()
