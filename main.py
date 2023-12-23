import csv
from datetime import datetime

# Function to read the CSV file and return a list of dictionaries
def read(filename):
    sales = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            sales = list(reader)
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    return sales

# Function to calculate the total sales for a given product
def calculate_total_sales(sales):
    total_revenue = 0
    for sale in sales:
        try:
            quantity = int(sale['Quantity Sold'])
            price = float(sale['Unit Price'])
            total_revenue += quantity * price
        except (KeyError, ValueError):
            print(f"Error analyzing sale: {sale}")
    return round(total_revenue, 2)

# Function to calculate the best-selling product
def best_selling_product(sales):
    product_quantities = {}
    for sale in sales:
        product = sale['Product']
        quantity = int(sale['Quantity Sold'])
        product_quantities[product] = product_quantities.get(product, 0) + quantity

    best_product = max(product_quantities, key=product_quantities.get)
    max_quantity = product_quantities[best_product]
    return best_product, max_quantity

# Function to display total revenue
def display_total_revenue(total_revenue):
    print(f"The total revenue is ${total_revenue}")

# Function to display the best-selling product
def display_best_product(best_product, max_quantity):
    print(f"The best-selling product is {best_product} with a quantity of {max_quantity}")

# Function to add a product to sales
def add_product(sales):
    product = input("Enter the product name: ")
    if not product:
        print("Product name cannot be empty.")
        return

    try:
        quantity = int(input("Enter the quantity sold: "))
        if quantity == 0:
            print("Quantity cannot be zero.")
            return

        price = float(input("Enter the unit price: "))
        if price == 0:
            print("Price cannot be zero.")
            return
    except ValueError:
        print("Error: Please enter valid numeric values.")
        return

    date = datetime.now().strftime("%Y-%m-%d")
    new_sale = {
        'Product': product,
        'Quantity Sold': quantity,
        'Unit Price': price,
        'Sale Date': date
    }

    with open(sales, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=['Product', 'Quantity Sold', 'Unit Price', 'Sale Date'])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(new_sale)

    print('')
    print(f"{product} added successfully on {date}.")

# Function to display all products
def display_all_products(sales):
    print("| {:<12} | {:<4} | {:<5} | {:<12} |".format("Product", "Qty", "Price", "Sale Date"))
    print("|" + "-" * 14 + "|" + "-" * 6 + "|" + "-" * 7 + "|" + "-" * 14 + "|")

    products = []
    with open(sales, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            product = row['Product']
            quantity = row['Quantity Sold']
            price = row['Unit Price']
            date = row['Sale Date']
            products.append({'product': product, 'quantity': quantity, 'price': price, 'date': date})
            print("| {:<12} | {:<4} | {:<5} | {:<12} |".format(product, quantity, price, date))

    return products

# Main program and menu
if __name__ == '__main__':
    filename = 'sales.csv'

    print("SALES MANAGEMENT")

    while True:
        print('')
        print("""MAIN MENU

        1- Display total revenue
        2- Display best-selling product
        3- Add a sold product
        4- View all data
        5- Quit the program
        """)

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Error: Please enter an integer.")
            continue

        if choice == 1:
            sales_data = read(filename)
            total_revenue = calculate_total_sales(sales_data)
            print('-----------------')
            print('')
            display_total_revenue(total_revenue)
            print('')
            print('-----------------')

        elif choice == 2:
            sales_data = read(filename)
            best_product_name, max_quantity_sold = best_selling_product(sales_data)
            print('-----------------')
            print('')
            display_best_product(best_product_name, max_quantity_sold)
            print('')
            print('-----------------')

        elif choice == 3:
            print('')
            add_confirmation = input(f"Do you want to add a product to {filename}? (Y/N) ")
            if add_confirmation.lower() == 'y':
                print('')
                add_product(filename)
                print('')
            else:
                print('')
                print("Thank you for your response!")
                print('')

        elif choice == 4:
            print('')
            display_all_products(filename)

        elif choice == 5:
            print('')
            exit_confirmation = input("Do you want to quit the program? (Y/N) ")
            if exit_confirmation.lower() == 'y':
                print('')
                print('Thank you for using the program.')
                print('')
                print("Restart the server to return. Goodbye!")
                print('')
                break
            else:
                print('')

        else:
            print('')
            print("Invalid choice. Please try again.")