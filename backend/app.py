from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# 🔁 Try connecting to MySQL with retry loop
while True:
    try:
        db = mysql.connector.connect(
            host="mysql",
            user="root",
            password="rootpass",
            database="studentDB"
        )
        cursor = db.cursor()
        print("✅ Connected to MySQL")
        break
    except Error as e:
        print("❌ MySQL not ready yet. Retrying in 2s...")
        time.sleep(2)

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    roll VARCHAR(50),
    gender VARCHAR(10)
)
""")

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    sql = "INSERT INTO students (name, roll, gender) VALUES (%s, %s, %s)"
    cursor.execute(sql, (data['name'], data['roll'], data['gender']))
    db.commit()
    return jsonify({"message": "Student added"}), 201

@app.route('/students', methods=['GET'])
def get_students():
    cursor.execute("SELECT name, roll, gender FROM students")
    results = cursor.fetchall()
    students = [{"name": row[0], "roll": row[1], "gender": row[2]} for row in results]
    return jsonify(students)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
