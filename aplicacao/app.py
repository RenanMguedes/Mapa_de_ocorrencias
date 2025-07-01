from flask import Flask, render_template, jsonify
import pymysql

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'database': 'ocorrencias',
    'user': 'root',
    'password': '1333medeiros',
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
            SELECT  codigo_ocorrencia, ocorrencia_uf, 
                    ocorrencia_latitude, ocorrencia_longitude, 
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

# Nova rota para detalhes da ocorrência
@app.route('/api/ocorrencia/<codigo>')
def get_ocorrencia_detalhes(codigo):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Busca dados principais da ocorrência
        cur.execute("SELECT * FROM ocorrencia WHERE codigo_ocorrencia = %s", (codigo,))
        ocorrencia = cur.fetchone()

        # Busca aeronaves envolvidas (tabela envolvida + tabela aeronave)
        cur.execute("""
            SELECT a.*, e.ocorrencia_dia, e.ocorrencia_hora
            FROM envolvida e
            JOIN aeronave a ON a.aeronave_matricula = e.fk_Aeronave_aeronave_matricula
            WHERE e.fk_Ocorrencia_codigo_ocorrencia = %s
        """, (codigo,))
        aeronaves = cur.fetchall()

        # Busca fatores contribuintes (relacao_Fatores + fator_contribuinte)
        cur.execute("""
            SELECT f.*
            FROM fatores rel
            JOIN fator_contribuinte f ON f.fator_nome = rel.fk_Fator_contribuinte_fator_nome
            WHERE rel.fk_Ocorrencia_codigo_ocorrencia = %s
        """, (codigo,))
        fatores = cur.fetchall()

        # Busca recomendações (possui + recomendacao)
        cur.execute("""
            SELECT r.*
            FROM possui p
            JOIN recomendacao r ON r.recomendacao_numero = p.fk_Recomendacao_recomendacao_numero
            WHERE p.fk_Ocorrencia_codigo_ocorrencia = %s
        """, (codigo,))
        recomendacoes = cur.fetchall()

        cur.close()
        conn.close()
        # Corrige campos timedelta para string
        import datetime
        def serialize_timedelta(val):
            if isinstance(val, datetime.timedelta):
                # Formata como HH:MM:SS
                total_seconds = int(val.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                return f"{hours:02}:{minutes:02}:{seconds:02}"
            return val

        for a in aeronaves:
            for k, v in a.items():
                a[k] = serialize_timedelta(v)

        return jsonify({
            'ocorrencia': ocorrencia,
            'aeronaves': aeronaves,
            'fatores': fatores,
            'recomendacoes': recomendacoes
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
