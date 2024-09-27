from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production!

# In-memory storage for bookings
bookings = []

# Admin credentials
admin_username = "Mohan56"
admin_password = "raj56"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    
    if username == admin_username and password == admin_password:
        session['logged_in'] = 'admin'
        return redirect(url_for('admin'))  # Redirect to admin dashboard

    session['logged_in'] = 'user' if username and password else None
    return redirect(url_for('home'))  # Redirect to home for users

@app.route('/home')
def home():
    if session.get('logged_in') != 'user':
        return redirect(url_for('login'))  # Redirect if not logged in as user
    return render_template('home.html')

@app.route('/book', methods=['POST'])
def book():
    if session.get('logged_in') != 'user':
        return redirect(url_for('login'))

    name = request.form['name']
    phone = request.form['phone']
    car_number = request.form['car_number']
    date = request.form['date']
    
    # Save booking information
    bookings.append({
        'name': name,
        'phone': phone,
        'car_number': car_number,
        'date': date
    })
    return redirect(url_for('result'))

@app.route('/result')
def result():
    if session.get('logged_in') != 'user':
        return redirect(url_for('login'))
    return render_template('result.html', bookings=bookings)

@app.route('/admin')
def admin():
    if session.get('logged_in') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin.html', bookings=bookings)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
