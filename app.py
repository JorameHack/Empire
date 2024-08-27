from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from models import db, User

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a real secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empire.db'
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('index.html', user=user)
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        name = request.form['name']
        password = request.form['password']

        if User.query.filter_by(name=name).first():
            return 'User already exists'

        user = User(first_name=first_name, last_name=last_name, phone_number=phone_number, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(name=name).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        return 'Invalid credentials'
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/api/trade', methods=['POST'])
def trade():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    user_id = session['user_id']
    amount = request.json.get('amount')
    action = request.json.get('action')

    user = User.query.get(user_id)
    if action == 'buy':
        user.balance += float(amount)
    elif action == 'sell':
        user.balance -= float(amount)
    else:
        return jsonify({'error': 'Invalid action'}), 400

    db.session.commit()
    return jsonify({'user': {'name': user.name, 'balance': user.balance}})


if __name__ == '__main__':
    app.run()
