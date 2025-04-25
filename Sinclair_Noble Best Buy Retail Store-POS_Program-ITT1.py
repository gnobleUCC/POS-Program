# Best Buy Retail Store-POS_Program-ITT103-SP2025

def initialize_catalog():
    return {
        "CornBeef": {"price": 420.00, "stock": 20},
        "Mackerel": {"price": 230.00, "stock": 12},
        "Salt Fish": {"price": 250.00, "stock": 25},
        "Box Milk": {"price": 320.00, "stock": 14},
        "Butter": {"price": 220.00, "stock": 7},
        "White Bread": {"price": 600.00, "stock": 14},
        "Brown Bread": {"price": 480.0, "stock": 10},
        "Eggs": {"price": 1200.00, "stock": 40},
        "Sugar": {"price": 200.00, "stock": 8},
        "Rice": {"price": 250.00, "stock": 12},
        "Flour": {"price": 210.00, "stock": 13},
        "Chicken": {"price": 1100.00, "stock": 6},
        "Minced Beef": {"price": 700.00, "stock": 4},
        "Ketchup": {"price": 300.00, "stock": 2},
        "Vegetable Oil": {"price": 250.00, "stock": 9},
        "Cocnut Oil": {"price": 650.00, "stock": 1},
        "Fruit Juice": {"price": 180.00, "stock": 50},
        "Bigga Soda" : {"price": 120.00, "stock": 50},
        "Local Beer": {"price": 155.50, "stock": 19}
    }

# Main Customer Interface/Product Selection
 
def display_catalog(catalog):
    print("---Best Buy Retail Store---")
    print("\n--- Product Catalog ---")
    for product, details in catalog.items():
        print(f"{product}: ${details['price']:.2f} | Stock: {details['stock']}")
        if details['stock'] < 4:
            print("  [!] Low Stock Alert!")

def add_to_cart(catalog, cart):
    product = input("Enter product name to add: ").title()
    if product in catalog:
        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("Quantity must be positive.")
            elif quantity > catalog[product]['stock']:
                print("Insufficient stock.")
            else:
                cart[product] = cart.get(product, 0) + quantity
                catalog[product]['stock'] -= quantity
                print(f"Added {quantity} x {product} to cart.")
        except ValueError:
            print("Invalid quantity.")
    else:
        print("Product not found.")

def remove_from_cart(catalog, cart):
    product = input("Enter product name to remove: ").title()
    if product in cart:
        try:
            quantity = int(input("Enter quantity to remove: "))
            if quantity <= 0:
                print("Quantity must be positive.")
            elif quantity > cart[product]:
                print("You are removing more than in cart.")
            else:
                cart[product] -= quantity
                catalog[product]['stock'] += quantity
                if cart[product] == 0:
                    del cart[product]
                print(f"Removed {quantity} x {product} from cart.")
        except ValueError:
            print("Invalid quantity.")
    else:
        print("Product not in cart.")

def view_cart(cart, catalog):
    print("\n--- Shopping Cart ---")
    total = 0
    for product, quantity in cart.items():
        price = catalog[product]['price']
        item_total = price * quantity
        print(f"{product}: {quantity} x ${price:.2f} = ${item_total:.2f}")
        total += item_total
    print(f"Subtotal: ${total:.2f}")

def checkout(cart, catalog):
    if not cart:
        print("Cart is empty.")
        return

    subtotal = sum(catalog[item]['price'] * qty for item, qty in cart.items())
    discount = 0.05 * subtotal if subtotal > 5000 else 0
    tax = 0.10 * (subtotal - discount)
    total = subtotal - discount + tax

    print("\n--- Checkout ---")
    print(f"Subtotal: ${subtotal:.2f}")
    if discount > 0:
        print(f"Discount (5%): -${discount:.2f}")
    print(f"Sales Tax (10%): +${tax:.2f}")
    print(f"Total Amount Due: ${total:.2f}")

    while True:
        try:
            amount_received = float(input("Enter amount received: $"))
            if amount_received < total:
                print("Insufficient payment. Try again.")
            else:
                change = amount_received - total
                print_receipt(cart, catalog, subtotal, discount, tax, total, amount_received, change)
                cart.clear()
                break
        except ValueError:
            print("Invalid input. Enter a valid amount.")

def print_receipt(cart, catalog, subtotal, discount, tax, total, amount_paid, change):
    print("\n========= STORE RECEIPT =========")
    print("Best Buy Retail Store")
    print("------------------------------")
    for product, qty in cart.items():
        price = catalog[product]['price']
        item_total = price * qty
        print(f"{product}: {qty} x ${price:.2f} = ${item_total:.2f}")
    print("------------------------------")
    print(f"Subtotal: ${subtotal:.2f}")
    if discount > 0:
        print(f"Discount: -${discount:.2f}")
    print(f"Tax: +${tax:.2f}")
    print(f"Total: ${total:.2f}")
    print(f"Amount Paid: ${amount_paid:.2f}")
    print(f"Change: ${change:.2f}")
    print("==============================")
    print("Thank you for shopping with us!")

# Main POS System Loop

catalog = initialize_catalog()

while True:
    cart = {}
    while True:
        display_catalog(catalog)
        print("\n1. Add Item to Cart")
        print("2. Remove Item from Cart")
        print("3. View Cart")
        print("4. Checkout")
        print("5. Exit POS System")

        choice = input("Select an option: ")

        if choice == "1":
            add_to_cart(catalog, cart)
        elif choice == "2":
            remove_from_cart(catalog, cart)
        elif choice == "3":
            view_cart(cart, catalog)
        elif choice == "4":
            checkout(cart, catalog)
            break
        elif choice == "5":
            print("Exiting POS System. Thank You For Shopping! Goodbye!")
            exit()
        else:
            print("Invalid option. Please choose between 1-5.")
