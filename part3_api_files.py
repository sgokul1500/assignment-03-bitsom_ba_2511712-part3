import requests
from datetime import datetime

def log_error(function_name, error_type, message):
    with open("error_log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] ERROR in {function_name}: {error_type} — {message}\n")


#TASK 1 
def file_operations():
    filename = "python_notes.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Topic 1: Variables store data. Python is dynamically typed.\n")
            f.write("Topic 2: Lists are ordered and mutable.\n")
            f.write("Topic 3: Dictionaries store key-value pairs.\n")
            f.write("Topic 4: Loops automate repetitive tasks.\n")
            f.write("Topic 5: Exception handling prevents crashes.\n")
        print("File written successfully.")
    except Exception as e:
        log_error("file_write", "Exception", str(e))

    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write("Topic 6: Functions improve code reuse.\n")
            f.write("Topic 7: Modules help organize code.\n")
        print("Lines appended.")
    except Exception as e:
        log_error("file_append", "Exception", str(e))

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        print("\n--- File Content ---")
        for i, line in enumerate(lines, 1):
            print(f"{i}. {line.strip()}")

        print(f"\nTotal lines: {len(lines)}")

        keyword = input("\nEnter keyword to search: ").lower()
        found = False

        for line in lines:
            if keyword in line.lower():
                print(line.strip())
                found = True

        if not found:
            print("No matching lines found.")

    except Exception as e:
        log_error("file_read", "Exception", str(e))


#TASK 2
def fetch_products():
    url = "https://dummyjson.com/products?limit=20"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()["products"]

        print("\nID | Title | Category | Price | Rating")
        print("-" * 60)

        for p in data:
            print(f"{p['id']} | {p['title']} | {p['category']} | ${p['price']} | {p['rating']}")

        return data

    except requests.exceptions.ConnectionError:
        print("Connection failed.")
        log_error("fetch_products", "ConnectionError", "No internet")
    except requests.exceptions.Timeout:
        print("Request timed out.")
        log_error("fetch_products", "Timeout", "Server slow")
    except Exception as e:
        print("Error:", e)
        log_error("fetch_products", "Exception", str(e))


def filter_sort_products(products):
    filtered = [p for p in products if p["rating"] >= 4.5]
    sorted_products = sorted(filtered, key=lambda x: x["price"], reverse=True)

    print("\n--- Filtered & Sorted Products ---")
    for p in sorted_products:
        print(f"{p['title']} - ${p['price']} - Rating: {p['rating']}")


def fetch_laptops():
    url = "https://dummyjson.com/products/category/laptops"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()["products"]

        print("\n--- Laptops ---")
        for p in data:
            print(f"{p['title']} - ${p['price']}")

    except Exception as e:
        log_error("fetch_laptops", "Exception", str(e))


def post_product():
    url = "https://dummyjson.com/products/add"

    payload = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        print("\nPOST Response:", response.json())

    except Exception as e:
        log_error("post_product", "Exception", str(e))


#TASK 3
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"


def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        log_error("read_file_safe", "FileNotFoundError", filename)
    finally:
        print("File operation attempt complete.")


#TASK 4 
def product_lookup_loop():
    while True:
        user_input = input("\nEnter product ID (1–100) or 'quit': ")

        if user_input.lower() == "quit":
            break

        if not user_input.isdigit():
            print("Invalid input. Please enter a number.")
            log_error("lookup_product", "InvalidInput", f"Non-numeric: {user_input}")
            continue

        product_id = int(user_input)

        if not (1 <= product_id <= 100):
            print("Invalid input. ID must be between 1 and 100.")
            log_error("lookup_product", "OutOfRange", f"{product_id}")
            continue

        url = f"https://dummyjson.com/products/{product_id}"

        try:
            response = requests.get(url, timeout=5)

            if response.status_code == 404:
                print("Product not found.")
                log_error("lookup_product", "HTTPError", f"404 for ID {product_id}")
            else:
                data = response.json()
                print(f"{data['title']} - ${data['price']}")

        except requests.exceptions.ConnectionError:
            print("Connection failed.")
            log_error("lookup_product", "ConnectionError", "No internet")
        except requests.exceptions.Timeout:
            print("Request timed out.")
            log_error("lookup_product", "Timeout", "Server slow")
        except Exception as e:
            log_error("lookup_product", "Exception", str(e))


def show_logs():
    print("\n--- ERROR LOG ---")
    try:
        with open("error_log.txt", "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip() == "":
                print("Log file is empty")
            else:
                print(content)
    except FileNotFoundError:
        print("No logs found.")


#MAIN 
if __name__ == "__main__":
    file_operations()

    products = fetch_products()
    if products:
        filter_sort_products(products)

    fetch_laptops()
    post_product()

    print("\n--- Safe Divide Tests ---")
    print(safe_divide(10, 2))
    print(safe_divide(10, 0))
    print(safe_divide("ten", 2))

    print("\n--- File Read Safe ---")
    print(read_file_safe("python_notes.txt"))
    read_file_safe("ghost_file.txt")

    product_lookup_loop()

    show_logs()