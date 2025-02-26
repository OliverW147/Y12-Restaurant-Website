import time
import json

class Bookings:
    def __init__(self, filename):
        self.filename = filename
        self.tables = 25
        self.open_hours = (10, 22)  # Restaurant is open from 10 AM to 10 PM
        self.load_bookings()

    def load_bookings(self):
        try:
            with open(self.filename, 'r') as file:
                self.bookings = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.bookings = {}
            self.save_bookings()

    def save_bookings(self):
        with open(self.filename, 'w') as file:
            json.dump(self.bookings, file)

    def is_valid_booking_time(self, booking_time):
        try:
            return True
        except ValueError:
            return False

    def create_booking(self, username, table_num, booking_time, requested_meals, stock, meals, usages):
        if not self.is_valid_booking_time(booking_time):
            return None, "Invalid booking time. Must be within open hours and in 1-hour blocks."

        booking_id = f"{username}-{booking_time}"
        if self.is_available(table_num, booking_time):
            if Meals.is_available_with_quantities(meals, stock, requested_meals):
                booking_info = {
                    "username": username,
                    "table_num": table_num,
                    "booking_time": booking_time,
                    "requested_meals": requested_meals,
                }
                self.bookings[booking_id] = booking_info
                self.save_bookings()

                try:
                    for meal, quantity in requested_meals.items():
                        for ingredient, ingredient_quantity in meals.recipes[meal].items():
                            stock.remove_quantity(ingredient, quantity * ingredient_quantity)
                            usages.log_usage(ingredient, quantity * ingredient_quantity, time.time())
                except ValueError as e:
                    self.cancel_booking(booking_id)
                    return None, str(e)

                return booking_id, None
            else:
                return None, "Insufficient ingredients in inventory."
        else:
            return None, "Table is not available at the requested time."

    def is_available(self, table_num, booking_time):
        for booking_id, booking_info in self.bookings.items():
            if booking_info["booking_time"] == booking_time and booking_info["table_num"] == table_num:
                return False
        return True

    def cancel_booking(self, booking_id):
        if booking_id in self.bookings:
            del self.bookings[booking_id]
            self.save_bookings()
            return True
        else:
            return False

    def get_available_tables(self, booking_time):
        available_tables = []
        for table_num in range(1, self.tables + 1):
            if not self.is_available(table_num, booking_time):
                continue
            available_tables.append(table_num)
        return available_tables



class Inventory:
    def __init__(self, filename):
        self.filename = filename
        self.load_inventory()

    def load_inventory(self):
        try:
            with open(self.filename, 'r') as file:
                self.items = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.items = {}
            self.save_inventory()

    def save_inventory(self):
        with open(self.filename, 'w') as file:
            json.dump(self.items, file)

    def add_ingredient(self, name, quantity):
        self.items[name] = self.items.get(name, 0) + quantity
        self.save_inventory()

    def remove_ingredient(self, name, quantity):
        if name in self.items and self.items[name] >= quantity:
            self.items[name] -= quantity
            if self.items[name] == 0:
                del self.items[name]
            self.save_inventory()
            return True
        else:
            raise ValueError(f"Insufficient quantity of {name} or item does not exist.")

    def get_stock(self):
        return self.items

    def get_quantity(self, name):
        return self.items.get(name, 0)

    def remove_quantity(self, name, quantity):
        if self.get_quantity(name) >= quantity:
            self.items[name] -= quantity
            self.save_inventory()
        else:
            raise ValueError(f"Insufficient quantity of {name}")


class Meals:
    def __init__(self, filename):
        self.filename = filename
        self.load_recipes()

    def load_recipes(self):
        try:
            with open(self.filename, 'r') as file:
                self.recipes = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.recipes = {}
            self.save_recipes()

    def save_recipes(self):
        with open(self.filename, 'w') as file:
            json.dump(self.recipes, file)

    def add_recipe(self, name, ingredients):
        self.recipes[name] = ingredients
        self.save_recipes()

    def remove_recipe(self, name):
        if name in self.recipes:
            del self.recipes[name]
            self.save_recipes()
            return True
        else:
            return False

    def is_available(self, name, inventory):
        for ingredient, quantity in self.recipes[name].items():
            if inventory.get_quantity(ingredient) < quantity:
                return False
        return True

    def is_available_with_quantities(self, inventory, desired_meals):
        needed_ingredients = {}
        for meal, quantity in desired_meals.items():
            if meal not in self.recipes:
                return False  # Handle missing recipe
            for ingredient, recipe_quantity in self.recipes[meal].items():
                needed_ingredients[ingredient] = needed_ingredients.get(ingredient, 0) + quantity * recipe_quantity

        for ingredient, needed_amount in needed_ingredients.items():
            if inventory.get_quantity(ingredient) < needed_amount:
                return False
        return True


class Usages:
    def __init__(self, filename):
        self.filename = filename
        self.load_usages()

    def load_usages(self):
        try:
            with open(self.filename, 'r') as file:
                self.logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.logs = []
            self.save_usages()

    def save_usages(self):
        with open(self.filename, 'w') as file:
            json.dump(self.logs, file)

    def log_usage(self, ingredient, quantity, timestamp):
        self.logs.append({"ingredient": ingredient, "quantity": quantity, "time": timestamp})
        self.save_usages()

    def get_usages(self, ingredient=None, start_time=None, end_time=None):
        filtered_logs = self.logs
        if ingredient:
            filtered_logs = [log for log in filtered_logs if log["ingredient"] == ingredient]
        if start_time and end_time:
            filtered_logs = [log for log in filtered_logs if start_time <= log["time"] <= end_time]
        return filtered_logs

    def predict_shortages(self, inventory, limit=0.3):
        potential_shortages = {}
        current_time = time.time()
        one_week_ago = current_time - 604800
        for log in self.logs:
            ingredient = log["ingredient"]
            current_stock = inventory.get_quantity(ingredient)
            recent_usages = [log for log in self.logs if log["ingredient"] == ingredient and log["time"] >= one_week_ago]
            usage_sum = sum(log["quantity"] for log in recent_usages)
            if current_stock - usage_sum < current_stock * limit:
                potential_shortages[ingredient] = current_stock - usage_sum
        return potential_shortages


class Accounts:
    def __init__(self, filename):
        self.filename = filename
        self.load_accounts()
        self.staff_accounts = {"staff": "pass"}

    def load_accounts(self):
        try:
            with open(self.filename, 'r') as file:
                self.accounts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.accounts = {}
            self.save_accounts()

    def save_accounts(self):
        with open(self.filename, 'w') as file:
            json.dump(self.accounts, file)

    def register(self, username, password):
        if username not in self.accounts:
            self.accounts[username] = password
            self.save_accounts()
            return True
        else:
            return False

    def login(self, username, password):
        return username in self.accounts and self.accounts[username] == password

    def staff_login(self, username, password):
        return username in self.staff_accounts and self.staff_accounts[username] == password
