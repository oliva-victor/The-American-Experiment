from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)
DATABASE_URL = 'mysql+pymysql://root:password1!@localhost/american'
engine = create_engine(DATABASE_URL)

@app.route('/users/exists', methods=['GET'])
def check_user_exists():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username is required."}), 400  # Handle missing username

    with engine.connect() as connection:
        query = text("SELECT COUNT(*) FROM users WHERE username = :username")
        exists = connection.execute(query, {"username": username}).scalar()
    return jsonify({"exists": exists > 0})

@app.route('/signup', methods=['POST'])
def create_user():
    data = request.json
    username = data['username']
    password = data['password']
    # Add logic to create user here
    try:
        with engine.connect() as connection:
            query = text("""
                INSERT INTO users (username, password, createdAt, updatedAt, day)
                VALUES (:username, :password, NOW(), NOW(), 0)
            """)
            connection.execute(query, {"username": username, "password": password})
        return jsonify({"message": "User created!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error as JSON

if __name__ == '__main__':
    app.run(port=8501)  # Ensure this port matches your requests in Streamlit
