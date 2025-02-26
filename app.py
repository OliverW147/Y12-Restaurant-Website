from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
import time
from backend import Inventory, Bookings, Meals, Usages, Accounts

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Initialize your previously defined classes
inventory = Inventory('inventory.txt')
bookings = Bookings('bookings.txt')
meals = Meals('meals.txt')
usages = Usages('usage_logs.txt')
accounts = Accounts('accounts.txt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if accounts.login(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('staff_username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if accounts.register(username, password):
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.', 'error')
    return render_template('register.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        table_num = int(request.form['table_num'])
        booking_time = request.form['booking_time']

        requested_meals = {}
        for meal in meals.recipes.keys():
            if meal in request.form and request.form[meal]:
                requested_meals[meal] = int(request.form[meal])

        booking_id, error = bookings.create_booking(session['username'], table_num, booking_time, requested_meals, inventory, meals, usages)
        if booking_id:
            flash('Booking successful', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Booking failed: {error}', 'error')
            return redirect(url_for('book'))

    available_tables = bookings.get_available_tables(request.args.get('booking_time', ''))
    return render_template('booking.html', meals=meals.recipes, available_tables=available_tables)

@app.route('/staff', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if accounts.staff_login(username, password):
            session['staff_username'] = username
            return redirect(url_for('staff_dashboard'))
        else:
            flash('Invalid staff login.', 'error')

    return render_template('staff_login.html')

@app.route('/staff/dashboard')
def staff_dashboard():
    if 'staff_username' not in session:
        return redirect(url_for('staff_login'))

    return render_template('staff_interface.html')

@app.route('/staff/bookings')
def staff_bookings():
    if 'staff_username' not in session:
        return redirect(url_for('staff_login'))

    all_bookings = bookings.bookings
    return render_template('staff_bookings.html', bookings=all_bookings)

@app.route('/staff/inventory', methods=['GET', 'POST'])
def staff_inventory():
    if 'staff_username' not in session:
        return redirect(url_for('staff_login'))

    if request.method == 'POST':
        action = request.form['action']
        ingredient = request.form['ingredient']
        quantity = int(request.form['quantity'])
        if action == 'add':
            inventory.add_ingredient(ingredient, quantity)
            flash(f'Added {quantity} of {ingredient} to inventory.', 'success')
        elif action == 'remove':
            try:
                inventory.remove_ingredient(ingredient, quantity)
                flash(f'Removed {quantity} of {ingredient} from inventory.', 'success')
            except ValueError as e:
                flash(str(e), 'error')

    stock = inventory.get_stock()
    return render_template('staff_inventory.html', stock=stock)

@app.route('/staff/usages')
def staff_usages():
    if 'staff_username' not in session:
        return redirect(url_for('staff_login'))

    usage_logs = [
        {
            "ingredient": log["ingredient"],
            "quantity": log["quantity"],
            "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(log["time"]))
        }
        for log in usages.logs
    ]
    return render_template('staff_usages.html', usages=usage_logs)

@app.route('/staff/meals', methods=['GET', 'POST'])
def staff_meals():
    if 'staff_username' not in session:
        return redirect(url_for('staff_login'))

    if request.method == 'POST':
        action = request.form['action']
        meal_name = request.form['meal_name']
        ingredients = {}
        ingredient_index = 1
        while f'ingredient_{ingredient_index}' in request.form:
            ingredient_name = request.form[f'ingredient_{ingredient_index}']
            ingredient_quantity = int(request.form[f'quantity_{ingredient_index}'])
            ingredients[ingredient_name] = ingredient_quantity
            ingredient_index += 1

        if action == 'add':
            meals.add_recipe(meal_name, ingredients)
            flash(f'Added meal {meal_name} to menu.', 'success')
        elif action == 'remove':
            if meals.remove_recipe(meal_name):
                flash(f'Removed meal {meal_name} from menu.', 'success')
            else:
                flash(f'Meal {meal_name} not found.', 'error')

    all_meals = meals.recipes
    return render_template('staff_meals.html', meals=all_meals)

@app.route('/menu')
def menu():
    all_meals = meals.recipes
    return render_template('menu.html', meals=all_meals)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/staff/bookings/cancel', methods=['POST'])
def cancel_booking():
    if 'staff_username' not in session:
        return redirect(url_for('staff_login'))

    booking_id = request.form['booking_id']
    if bookings.cancel_booking(booking_id):
        flash('Booking cancelled successfully.', 'success')
    else:
        flash('Failed to cancel booking.', 'error')
    return redirect(url_for('staff_bookings'))

if __name__ == '__main__':
    app.run(debug=True)
