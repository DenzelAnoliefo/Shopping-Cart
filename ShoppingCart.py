"""
The provided code establishes an online shopping system with four crucial components: Product, Inventory,
ShoppingCart, and ProductCatalog. The Product class defines product attributes like name, price, and category. The
Inventory class employs a dictionary to manage product stock, offering functions for adding, updating, and retrieving
product information. The ShoppingCart class represents a buyer's cart, linked to an inventory, allowing for the
addition, removal, and display of items. The ProductCatalog class maintains a catalog of products through a set,
categorizing  and displaying them based on their prices. The code includes two functions, populate_inventory and
populate_catalog, which facilitate the instantiation of instances by reading data from files. In simpler terms, this
code serves as a framework for online shopping, ensuring efficient management of products, inventories, and shopping
carts.
"""
class Product:
    def __init__(self, name, price, category):
        # Product constructor, initializes product attributes.
        # Parameters: name (str), price (int), category (str)
        self._name = name
        self._price = price
        self._category = category

    def __eq__(self, other):
        # Overrides equality for Product instances.
        # Parameters: other (Product)
        return isinstance(other, Product) and (
            self._name == other._name and
            self._price == other._price and
            self._category == other._category
        )

    def get_name(self):
        # Get the name of the product.
        # Returns: str
        return self._name

    def get_price(self):
        # Get the price of the product.
        # Returns: int
        return self._price

    def get_category(self):
        # Get the category of the product.
        # Returns: str
        return self._category

    def __repr__(self):
        # String representation of the Product instance.
        return f"Product({self._name}, {self._price}, {self._category})"

    def __hash__(self):
        # Hash function for the Product instance.
        return hash((self._name, self._price, self._category))


class Inventory:
    def __init__(self):
        # Inventory constructor, initializes inventory as a dictionary.
        self._inventory = {}

    def add_to_productInventory(self, productName, productPrice, productQuantity):
        # Adds a new product to the inventory.
        # Parameters: productName (str), productPrice (int), productQuantity (int)
        self._inventory[productName] = {'price': productPrice, 'quantity': productQuantity}

    def add_productQuantity(self, nameProduct, addQuantity):
        # Updates quantity of a product in the inventory.
        # Parameters: nameProduct (str), addQuantity (int)
        self._inventory[nameProduct]['quantity'] += addQuantity

    def remove_productQuantity(self, nameProduct, removeQuantity):
        # Updates quantity of a product in the inventory.
        # Parameters: nameProduct (str), removeQuantity (int)
        self._inventory[nameProduct]['quantity'] -= removeQuantity

    def get_productPrice(self, nameProduct):
        # Retrieves the price of a product.
        # Parameters: nameProduct (str)
        # Returns: int
        return self._inventory[nameProduct]['price']

    def get_productQuantity(self, nameProduct):
        # Retrieves the quantity of a product.
        # Parameters: nameProduct (str)
        # Returns: int
        return self._inventory[nameProduct]['quantity']

    def display_Inventory(self):
        # Displays the inventory.
        for product_name, product_info in self._inventory.items():
            print(f"{product_name}, {product_info['price']}, {product_info['quantity']}")


class ShoppingCart:
    def __init__(self, buyer_name, inventory):
        # ShoppingCart constructor, initializes shopping cart attributes.
        # Parameters: buyer_name (str), inventory (Inventory)
        self._buyer_name = buyer_name
        self._inventory = inventory
        self._cart = {}

    def add_to_cart(self, name_product, requested_quantity):
        # Adds items to the cart and updates inventory.
        # Parameters: name_product (str), requested_quantity (int)
        # Returns: str
        if requested_quantity <= 0:
            return "Invalid quantity"

        if name_product in self._cart:
            self._cart[name_product] += requested_quantity
        else:
            self._cart[name_product] = requested_quantity

        # Check if inventory has sufficient quantity
        inventory_quantity = self._inventory.get_productQuantity(name_product)
        if requested_quantity > inventory_quantity:
            # Roll back the changes in the cart
            self._cart[name_product] -= requested_quantity
            return "Can not fill the order"

        # Update inventory
        self._inventory.remove_productQuantity(name_product, requested_quantity)

        return "Filled the order"

    def remove_from_cart(self, name_product, requested_quantity):
        # Removes items from the cart and updates inventory.
        # Parameters: name_product (str), requested_quantity (int)
        # Returns: str
        if name_product not in self._cart:
            return "Product not in the cart"

        cart_quantity = self._cart[name_product]

        if requested_quantity > cart_quantity:
            return "The requested quantity to be removed from cart exceeds what is in the cart"

        # Update cart and inventory
        self._cart[name_product] -= requested_quantity
        self._inventory.add_productQuantity(name_product, requested_quantity)

        # Remove the product from the cart if the quantity becomes zero
        if self._cart[name_product] == 0:
            del self._cart[name_product]

        return "Successful"

    def view_cart(self):
        # Displays the contents of the shopping cart and calculates the total.
        total = 0
        for name_product, quantity in self._cart.items():
            price = self._inventory.get_productPrice(name_product)
            total += price * quantity
            print(f"{name_product} {quantity}")

        print(f"Total: {total}")
        print(f"Buyer Name: {self._buyer_name}")


class ProductCatalog:
    def __init__(self):
        # ProductCatalog constructor, initializes product catalog data structure.
        self._catalog = set()

    def add_product(self, product):
        # Adds a new product to the catalog.
        # Parameters: product (Product)
        self._catalog.add(product)

    def price_category(self):
        # Categorizes products based on price and displays information.
        low_prices = set()
        medium_prices = set()
        high_prices = set()

        for product in self._catalog:
            price = product.get_price()
            name = product.get_name()

            if 0 <= price <= 99:
                low_prices.add(name)
            elif 100 <= price <= 499:
                medium_prices.add(name)
            elif price >= 500:
                high_prices.add(name)

        print(f"Number of low price items: {len(low_prices)}")
        print(f"Number of medium price items: {len(medium_prices)}")
        print(f"Number of high price items: {len(high_prices)}")

    def display_catalog(self):
        # Displays the catalog from cheapest to most expensive.
        sorted_catalog = sorted(self._catalog, key=lambda product: product.get_price())

        for product in sorted_catalog:
            name = product.get_name()
            price = product.get_price()
            category = product.get_category()
            print(f"Product: {name} Price: {price} Category: {category}")


def populate_inventory(filename):
    # Populates an Inventory object from a file.
    # Parameters: filename (str)
    # Returns: Inventory or None
    try:
        # Initialize an Inventory object
        inventory = Inventory()

        # Read the file and populate the inventory
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                name = data[0].strip()
                price = int(data[1].strip())
                quantity = int(data[2].strip())
                inventory.add_to_productInventory(name, price, quantity)

        return inventory
    except FileNotFoundError:
        print(f"Could not read file: {filename}")
        return None


def populate_catalog(filename):
    # Populates a ProductCatalog object from a file.
    # Parameters: filename (str)
    # Returns: ProductCatalog or None
    try:
        # Initialize a ProductCatalog object
        catalog = ProductCatalog()

        # Read the file and populate the catalog
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                name = data[0].strip()
                price = int(data[1].strip())
                category = data[3].strip()
                product = Product(name, price, category)
                catalog.add_product(product)

        return catalog
    except FileNotFoundError:
        print(f"Could not read file: {filename}")
        return None

