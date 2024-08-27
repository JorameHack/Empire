from flask import Flask, request, jsonify
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empire.db'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/api/trade', methods=['POST'])
def trade():
    if 'user_id' not in request.cookies:
        return jsonify({'error': 'Not logged in'}), 401

    user_id = int(request.cookies.get('user_id'))
    amount = request.json.get('amount')
    action = request.json.get('action')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if action == 'buy':
        user.balance += float(amount)
    elif action == 'sell':
        user.balance -= float(amount)
    else:
        return jsonify({'error': 'Invalid action'}), 400

    db.session.commit()
    return jsonify({'user': {'name': user.name, 'balance': user.balance}})
