from flask import Flask, render_template, jsonify
import pymysql

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'database': 'ocorrencias',
    'user': 'root',
    'password': 'lemos ama jojo',
    'host': 'localhost',
    'port': 3306,
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ocorrencias')
def get_ocorrencias():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT ocorrencia_latitude, ocorrencia_longitude, 
                   ocorrencia_cidade, ocorrencia_classificacao
            FROM ocorrencia
            WHERE ocorrencia_latitude IS NOT NULL 
            AND ocorrencia_longitude IS NOT NULL
        """)
        ocorrencias = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(list(ocorrencias))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
