"""
Module for counting distinct words in a text file and their frequency.
"""

import sys
import time


def read_file(filename):
    """Reads a file and extracts words, handling errors gracefully."""
    words = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    print(f"Warning: Line {line_num} is empty.")
                    continue
                words.extend(line.split())
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except (OSError, IOError) as file_error:
        print(f"File error: {file_error}")
        sys.exit(1)

    return words


def count_words(words):
    """Counts occurrences of each distinct word in a list."""
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    return word_freq


def write_results(word_freq, execution_time):
    """Writes word count results to a file."""
    with open("WordCountResults.txt", 'w', encoding='utf-8') as file:
        file.write("Word\tFrequency\n")
        file.write("---------------------\n")
        for word, count in sorted(word_freq.items()):
            file.write(f"{word}\t{count}\n")
        file.write(f"\nExecution Time: {execution_time:.2f} seconds\n")


def main():
    """Main function to process the file and count words."""
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py <fileWithData.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    start_time = time.time()

    words = read_file(filename)
    word_freq = count_words(words)
    execution_time = time.time() - start_time

    print("\nWord Count Results:")
    print("Word\tFrequency")
    print("---------------------")
    for word, count in sorted(word_freq.items()):
        print(f"{word}\t{count}")

    print(f"\nExecution Time: {execution_time:.2f} seconds")

    write_results(word_freq, execution_time)


if __name__ == "__main__":
    main()
