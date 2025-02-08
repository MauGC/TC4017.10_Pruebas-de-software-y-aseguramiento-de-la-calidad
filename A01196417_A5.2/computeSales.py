"""
Compute total sales from a given product catalog and sales records.
Handles returns by subtracting negative quantities.
"""

import sys
import time
import json
from decimal import Decimal, ROUND_HALF_UP


def read_json(file_path):
    """Reads a JSON file and returns the data."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"[ERROR] File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON format in '{file_path}'")
        sys.exit(1)


def compute_total_sales(price_catalogue, sales_records):
    """
    Computes total sales revenue, considering returns (negative quantities).
    Returns total sales, detailed sales summary, and invalid entries.
    """
    product_prices = {
        item["title"]: Decimal(str(item["price"]))
        for item in price_catalogue
        if isinstance(item, dict) and "title" in item and "price" in item
    }

    total_sales = Decimal("0.00")
    sales_summary = []
    invalid_entries = []

    for sale in sales_records:
        if ("Product" not in sale or "Quantity" not in sale or
                not isinstance(sale["Quantity"], (int, float))):
            invalid_entries.append(f"[ERROR] Invalid sale entry: {sale}")
            continue  # 🚀 Skip invalid entries

        product_name = sale["Product"]
        quantity = Decimal(str(sale["Quantity"]))

        if product_name in product_prices:
            item_price = product_prices[product_name]
            item_total = item_price * quantity

            if quantity > 0:
                sales_summary.append(
                    f"{product_name}: {quantity} x {item_price} = "
                    f"{item_total}"
                )
                total_sales += item_total  # ✅ Add to total
            elif quantity < 0:
                sales_summary.append(
                    f"{product_name} (RETURN): {quantity} x {item_price} = "
                    f"{item_total}"
                )
                total_sales += item_total  # ✅ Subtract from total
        else:
            invalid_entries.append(
                f"[ERROR] Unknown product '{product_name}' in sales record."
            )

    # Round only at the end to prevent floating point issues
    total_sales = total_sales.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return total_sales, sales_summary, invalid_entries


def write_results(output_file, total_sales, sales_summary,
                  invalid_entries, elapsed_time):
    """Writes the sales report to a file."""
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("SALES SUMMARY\n")
        file.write("=" * 40 + "\n")

        if sales_summary:
            file.write("\n".join(sales_summary) + "\n")
        else:
            file.write("[INFO] No valid sales records found.\n")

        file.write(f"\nTOTAL SALES: ${total_sales}\n")

        file.write("\nInvalid Entries:\n")
        file.write("=" * 40 + "\n")
        if invalid_entries:
            file.write("\n".join(invalid_entries) + "\n")
        else:
            file.write("[INFO] No invalid entries detected.\n")

        file.write(f"\nExecution Time: {elapsed_time:.2f} seconds\n")


def main():
    """Handles input arguments, processes sales data, and outputs results."""
    if len(sys.argv) != 3:
        print("Usage: python compute_sales.py <ProductList.json> <Sales.json>")
        sys.exit(1)

    product_file = sys.argv[1]
    sales_file = sys.argv[2]

    start_time = time.time()

    price_catalogue = read_json(product_file)
    sales_records = read_json(sales_file)

    total_sales, sales_summary, invalid_entries = compute_total_sales(
        price_catalogue, sales_records
    )

    elapsed_time = time.time() - start_time
    output_file = "SalesResults.txt"

    print("\nSALES SUMMARY")
    print("=" * 40)
    for summary in sales_summary:
        print(summary)

    print(f"\nTOTAL SALES: ${total_sales}")

    print("\nInvalid Entries:")
    print("=" * 40)
    for error in invalid_entries:
        print(error)

    print(f"\nExecution Time: {elapsed_time:.2f} seconds")

    write_results(output_file, total_sales, sales_summary,
                  invalid_entries, elapsed_time)


if __name__ == "__main__":
    main()
