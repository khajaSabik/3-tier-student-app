from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://students.dev.com"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Database connection
def get_db():
    return mysql.connector.connect(
        host="student-mysql",
        user="root",
        password="rootpass",
        database="studentDB"
    )

# Create table if not exists
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            roll VARCHAR(50) NOT NULL,
            gender VARCHAR(20) NOT NULL
        )
    """)
    conn.commit()

@app.route('/api/students', methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
        with get_db() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students")
            return jsonify(cursor.fetchall())
    
    elif request.method == 'POST':
        data = request.get_json()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (name, roll, gender) VALUES (%s, %s, %s)",
                (data['name'], data['roll'], data['gender'])
            )
            conn.commit()
            return jsonify({"status": "success"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)