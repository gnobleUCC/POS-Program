#
# pos_system.py
import datetime
import os

class Item:
    def __init__(self, item_id, item_name, unit_price, available_stock):
        self.item_id = item_id
        self.item_name = item_name
        self.unit_price = unit_price
        self.available_stock = available_stock

    def __str__(self):
        return f"{self.item_name} - ${self.unit_price:.2f} ({self.available_stock} in stock)"


class Cart:
    def __init__(self):
        self.cart_contents = {}  # {item_id: quantity}

    def add_item(self, item, quantity):
        if item.item_id in self.cart_contents:
            self.cart_contents[item.item_id] += quantity
        else:
            self.cart_contents[item.item_id] = quantity

    def remove_item(self, item_id, quantity=None):
        if item_id in self.cart_contents:
            if quantity is None or quantity >= self.cart_contents[item_id]:
                del self.cart_contents[item_id]
            else:
                self.cart_contents[item_id] -= quantity
            return True
        return False

    def get_summary(self, item_catalog):
        summary = [ ]
        for item_id, qty in self.cart_contents.items():
            item = item_catalog[item_id]
            summary.append({
                'item': item,
                'quantity': qty,
                'total_price': item.unit_price * qty
            })
        return summary

    def empty(self):
        self.cart_contents = {}


class PointOfSale:
    def __init__(self, shop_title):
        self.shop_title = shop_title
        self.catalog = self.load_items()
        self.cart = Cart()
        self.vat_rate = 0.10
        self.discount_limit = 5000
        self.discount_percentage = 0.05
        self.restock_alert_level = 5

    def load_items(self):
        items = {}

            (1, "Hand Towel", 300.00, 15),
            (2, "Tissue", 200.00, 25),
            (3, "Rice", 200.00, 40),
            (4, "Sugar", 350.00, 12),
            (5, "Pepsi", 200.00, 30),
            (6, "Water", 100.00, 35),
            (7, "Orange Juice", 200.00, 8),
            (8, "Bread", 550.00, 20),
            (9, "Oil", 300.00, 15),
            (10, "Butter", 90.00, 18),
            (11, "Betty Milk", 450.00, 10),
            (12, "Cornbeef", 550.00, 7)
        ]

        for item_id, name, price, stock in predefined_data:
            items[item_id] = Item(item_id, name, price, stock)

        return items

    def show_catalog(self):
        print("\n" + "=" * 50)
        print(f"{self.shop_title} - AVAILABLE ITEMS")
        print("=" * 50)
        print(f"{'ID':<5}{'Item':<25}{'Price':<10}{'Stock':<8}")
        print("-" * 50)

        for item_id, item in self.catalog.items():
            print(f"{item_id:<5}{item.item_name:<25}${item.unit_price:<9.2f}{item.available_stock:<8}")
            if item.available_stock < self.restock_alert_level:
                print(f"⚠️  LOW STOCK ALERT: {item.item_name} - Only {item.available_stock} left!")

        print("=" * 50)

    def add_item_to_cart(self):
        try:
            item_id = int(input("\nEnter item ID: "))
            if item_id not in self.catalog:
                print("Invalid ID. Try again.")
                return

            item = self.catalog[item_id]
            quantity = int(input(f"Enter quantity for {item.item_name}: "))

            if quantity <= 0:
                print("Quantity must be greater than zero.")
                return
            if quantity > item.available_stock:
                print(f"Only {item.available_stock} in stock.")
                return

            self.cart.add_item(item, quantity)
            item.available_stock -= quantity
            print(f"{quantity} x {item.item_name} added.")

        except ValueError:
            print("Please enter a valid number.")

    def remove_item_from_cart(self):
        if not self.cart.cart_contents:
            print("Your cart is empty.")
            return

        self.display_cart()
        try:
            item_id = int(input("\nEnter item ID to remove: "))
            if item_id not in self.cart.cart_contents:
                print("Item not found in cart.")
                return

            current_qty = self.cart.cart_contents[item_id]
            qty_input = input(f"Enter quantity to remove (press Enter to remove all {current_qty}): ")

            if qty_input == "":
                quantity = None
            else:
                quantity = int(qty_input)
                if quantity <= 0:
                    print("Update stock.")
                    return

            restore_amount = quantity if quantity is not None else current_qty
            self.catalog[item_id].available_stock += restore_amount

            if self.cart.remove_item(item_id, quantity):
                item_name = self.catalog[item_id].item_name
                print(f"Removed {restore_amount} x {item_name} from cart.")
            else:
                print("Could not remove item.")

        except ValueError:
            print("Please enter a valid number.")

    def display_cart(self):
        items = self.cart.get_summary(self.catalog)

        if not items:
            print("\nCart is empty.")
            return False

        print("\n" + "=" * 60)
        print(f"{self.shop_title} - CURRENT CART")
        print("=" * 60)
        print(f"{'ID':<13}{'Item':<25}{'Price':>12}{'Qty':>10}{'Total':>10}")
        print("-" * 60)

        subtotal = 0
        for entry in items:
            item = entry['item']
            qty = entry['quantity']
            total = entry['total_price']
            subtotal += total

            print(f"{item.item_id:>12}{item.item_name:>25}${item.unit_price:>11.2f}{qty:>5}${total:.2f}")

        print("-" * 60)
        print(f"{'Subtotal:':<43}${subtotal:.2f}")

        discount = 0
        if subtotal >= self.discount_limit:
            discount = subtotal * self.discount_percentage
            print(f"{'Discount (5%):':<43}-${discount:.2f}")
            subtotal -= discount

        Tax = subtotal * self.vat_rate
        grand_total = subtotal + tax

        print(f"{'Tax (10%):':<43}+${vat:.2f}")
        print(f"{'TOTAL:':<43}${grand_total:.2f}")
        print("=" * 60)

        return True

    def checkout(self):
        if not self.display_cart():
            return False

        summary = self.cart.get_summary(self.catalog)
        subtotal = sum(i['total_price'] for i in summary)
        discount = subtotal * self.discount_percentage if subtotal >= self.discount_limit else 0
        subtotal -= discount
        tax = subtotal * self.vat_rate
        final_amount = subtotal + tax

        try:
            payment = float(input(f"\nTotal due: ${final_amount:.2f}\nEnter payment amount: $"))
            if payment < final_amount:
                print("Insufficient payment.")
                for entry in summary:
                    entry['item'].available_stock += entry['quantity']
                return False

            change_due = payment - final_amount
            print(f"Payment accepted. Change: ${change_due:.2f}")
            self.print_receipt(summary, subtotal, discount, tax, final_amount, payment, change_due)
            self.cart.empty()
            return True

        except ValueError:
            print("Invalid amount entered.")
            return False

    def print_receipt(self, items, subtotal, discount, tax, total, payment, change):
        os.system('cls' if os.name == 'nt' else 'clear')

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        receipt_id = now.strftime("%Y%m%d%H%M%S")

        print("\n" + "=" * 50)
        print(f"{self.shop_title} - RECEIPT")
        print("=" * 50)
        print(f"Receipt #: {receipt_id}")
        print(f"Date: {timestamp}")
        print("-" * 50)
        print(f"{'Item':<25}{'Price':<8}{'Qty':<5}{'Total':<8}")
        print("-" * 50)

        original_total = sum(i['total_price'] for i in items)

        for entry in items:
            item = entry['item']
            qty = entry['quantity']
            total_price = entry['total_price']
            print(f"{item.item_name[:24]:<25}${item.unit_price:<7.2f}{qty:<5}${total_price:.2f}")

        print("-" * 50)
        print(f"{'Subtotal:':<30}${original_total:.2f}")
        if discount > 0:
            print(f"{'Discount (5%):':<30}-${discount:.2f}")
        print(f"{'Tax (10%):':<30}+${tax:.2f}")
        print(f"{'TOTAL:':<30}${total:.2f}")
        print("-" * 50)
        print(f"{'Paid:':<30}${payment:.2f}")
        print(f"{'Change:':<30}${change:.2f}")
        print("-" * 50)
        print(f"\nThank you for shopping at {self.shop_title}!")
        print("We appreciate your business!")
        print("=" * 50)
        input("\nPress Enter to continue...")

    def start(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{self.shop_title} - POS Menu")
            print("1. View Catalog")
            print("2. Add Item to Cart")
            print("3. Remove Item from Cart")
            print("4. View Cart")
            print("5. Checkout")
            print("0. Exit")

            option = input("\nChoose an option: ")

            if option == '1':
                self.show_catalog()
            elif option == '2':
                self.show_catalog()
                self.add_item_to_cart()
            elif option == '3':
                self.remove_item_from_cart()
            elif option == '4':
                self.display_cart()
            elif option == '5':
                if self.checkout():
                    print("Purchase completed.")
            elif option == '0':
                print("Thanks for using the POS system. Goodbye!")
                break
            else:
                print("Invalid choice. Please select again.")

            input("\nPress Enter to continue...")


if __name__ == "__main__":
    shop_name = "Ultra WalMart"
    system = PointOfSale(shop_name)
    system.start()




