from flask import Flask, jsonify
import os
import redis
import psycopg2

app = Flask(__name__)

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)

db_host = os.environ.get('DB_HOST', 'localhost')
db_name = os.environ.get('DB_NAME', 'mydatabase')
db_user = os.environ.get('DB_USER', 'myuser')
db_password = os.environ.get('DB_PASSWORD', 'mypassword')

def get_db_connection():
    conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
    return conn

@app.route('/')
def hello():
    return "Hello from Case 5 Web App!"

@app.route('/data')
def get_data():
    cached_data = redis_client.get('my_data')
    if cached_data:
        return jsonify({"source": "cache", "data": cached_data})

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM my_table LIMIT 1;")
        db_data = cur.fetchone()
        cur.close()
        conn.close()

        if db_data:
            redis_client.setex('my_data', 60, str(db_data))
            return jsonify({"source": "database", "data": db_data})
        else:
            return jsonify({"source": "database", "data": "No data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)