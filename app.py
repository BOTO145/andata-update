from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, esp32_id TEXT, timestamp TEXT, value TEXT)')
    conn.commit()
    conn.close()

@app.route('/store', methods=['POST'])
def store_data():
    data = request.json
    esp32_id = data.get('esp32_id')  # Get the ESP32 ID
    timestamp = data.get('timestamp')
    value = data.get('value')

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO data (esp32_id, timestamp, value) VALUES (?, ?, ?)', (esp32_id, timestamp, value))
    conn.commit()
    conn.close()

    return jsonify({"message": "Data stored successfully"}), 201

@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT esp32_id FROM data')
    esp32_ids = c.fetchall()
    conn.close()
    return jsonify(esp32_ids)

@app.route('/data/<esp32_id>', methods=['GET'])
def get_device_data(esp32_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM data WHERE esp32_id = ?', (esp32_id,))
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/')
def index():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT esp32_id FROM data')
    esp32_ids = c.fetchall()
    conn.close()
    return render_template('index.html', esp32_ids=esp32_ids)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
