from flask import Flask, jsonify
import os
import time

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SERVER_NAME = os.getenv('SERVER_NAME', 'local-server')
APP_PORT = int(os.getenv('APP_PORT', '5000'))

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5432')),
    'database': os.getenv('DB_NAME', 'serverdb'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}


def db_get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"erreur de connexion DB: {e}")
        return None


@app.route('/health', methods=['GET'])
def health():
    try:
        conn = db_get_connection()
        if conn is None:
            return jsonify({
                'status': 'unhealthy',
                'server': SERVER_NAME,
                'database': 'disconnected'
            }), 503

        cur = conn.cursor()
        cur.execute('SELECT NOW()')
        res = cur.fetchone()
        cur.close()
        conn.close()

        return jsonify({
            'status': 'healthy',
            'server': SERVER_NAME,
            'database': 'connected',
            'timestamp': str(res[0])
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503


@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'server_name': SERVER_NAME,
        'uptime': time.time(),
        'timestamp': time.time()
    })


@app.route('/', methods=['GET'])
def home():
    """
    Endpoint racine, affiche un message de bienvenue
    """
    return jsonify({
        'message': 'Bienvenue !',
        'server': SERVER_NAME,
        'endpoints': [
            'GET /',
            'GET /health',
            'GET /status',
            'GET /servers',
            'POST /servers'
        ]
    }), 200


if __name__ == '__main__':
    print(f"[+] {SERVER_NAME} demarre sur 0.0.0.0:{APP_PORT}")
    app.run(debug=False, host='0.0.0.0', port=APP_PORT)
