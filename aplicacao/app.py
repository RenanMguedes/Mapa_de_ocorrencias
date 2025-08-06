# =================== IMPORTS ===================
from flask import Flask, render_template, jsonify
import pymysql
import datetime
from dotenv import load_dotenv
import os

# =================== CONFIGURAÇÃO ===================
load_dotenv()

app = Flask(__name__)


# Carrega variáveis do .env
DB_DATABASE = os.getenv('DB_DATABASE', 'ocorrencias')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '1333medeiros')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))

DB_CONFIG = {
    'database': DB_DATABASE,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT,
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

# =================== ROTAS ===================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ocorrencias')
def get_ocorrencias():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Usa o nome da tabela em minúsculo para garantir compatibilidade com o endpoint de detalhes
        cur.execute("""
            SELECT codigo_ocorrencia, ocorrencia_uf, 
                   ocorrencia_latitude, ocorrencia_longitude, 
                   ocorrencia_cidade, ocorrencia_classificacao
            FROM ocorrencia
            WHERE ocorrencia_latitude IS NOT NULL 
            AND ocorrencia_longitude IS NOT NULL
        """)
        ocorrencias = cur.fetchall()
        # Loga a quantidade de registros encontrados (apenas para debug)
        print(f"[DEBUG] Ocorrencias retornadas: {len(ocorrencias)}")
        # Garante que os campos latitude/longitude sejam float (para o frontend)
        for o in ocorrencias:
            try:
                o['ocorrencia_latitude'] = float(o['ocorrencia_latitude'])
                o['ocorrencia_longitude'] = float(o['ocorrencia_longitude'])
            except Exception:
                o['ocorrencia_latitude'] = None
                o['ocorrencia_longitude'] = None
        # Remove registros com lat/lon inválidos
        ocorrencias = [o for o in ocorrencias if o['ocorrencia_latitude'] is not None and o['ocorrencia_longitude'] is not None]
        cur.close()
        conn.close()
        return jsonify(list(ocorrencias))
    except Exception as e:
        print(f"[ERROR] /api/ocorrencias: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ocorrencia/<codigo>')
def get_ocorrencia_detalhes(codigo):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ocorrencia WHERE codigo_ocorrencia = %s", (codigo,))
        ocorrencia = cur.fetchone()

        cur.execute("""
            SELECT a.*, e.ocorrencia_dia, e.ocorrencia_hora
            FROM envolvida e
            JOIN aeronave a ON a.aeronave_matricula = e.fk_Aeronave_aeronave_matricula
            WHERE e.fk_Ocorrencia_codigo_ocorrencia = %s
        """, (codigo,))
        aeronaves = cur.fetchall()

        cur.execute("""
            SELECT f.*
            FROM fatores rel
            JOIN fator_contribuinte f ON f.fator_nome = rel.fk_Fator_contribuinte_fator_nome
            WHERE rel.fk_Ocorrencia_codigo_ocorrencia = %s
        """, (codigo,))
        fatores = cur.fetchall()

        cur.execute("""
            SELECT r.*
            FROM possui p
            JOIN recomendacao r ON r.recomendacao_numero = p.fk_Recomendacao_recomendacao_numero
            WHERE p.fk_Ocorrencia_codigo_ocorrencia = %s
        """, (codigo,))
        recomendacoes = cur.fetchall()

        cur.close()
        conn.close()

        def serialize_timedelta(val):
            if isinstance(val, datetime.timedelta):
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

@app.route('/api/estatisticas/acidentes-por-aeronave')
def get_acidentes_por_aeronave():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                A.aeronave_matricula,
                A.aeronave_modelo,
                FAB.Nome AS Fabricante,
                COUNT(O.codigo_ocorrencia) AS Total_Acidentes
            FROM
                Aeronave AS A
            INNER JOIN
                envolvida AS E ON A.aeronave_matricula = E.fk_Aeronave_aeronave_matricula
            INNER JOIN
                Ocorrencia AS O ON E.fk_Ocorrencia_codigo_ocorrencia = O.codigo_ocorrencia
            INNER JOIN
                Fabricante AS FAB ON A.fk_Fabricante_Nome = FAB.Nome
            WHERE
                O.ocorrencia_classificacao = 'ACIDENTE'
            GROUP BY
                A.aeronave_matricula,
                A.aeronave_modelo,
                FAB.Nome
            ORDER BY
                Total_Acidentes DESC
            LIMIT 20
        """)
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(list(resultados))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estatisticas/acidentes-por-fabricante')
def get_acidentes_por_fabricante():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                F.Nome AS Fabricante,
                IFNULL(F.Pais, 'Desconhecido') AS Pais,
                COUNT(DISTINCT O.codigo_ocorrencia) AS Numero_de_Acidentes
            FROM
                Fabricante AS F
            JOIN
                Aeronave AS A ON F.Nome = A.fk_Fabricante_Nome
            JOIN
                envolvida AS E ON A.aeronave_matricula = E.fk_Aeronave_aeronave_matricula
            JOIN
                Ocorrencia AS O ON E.fk_Ocorrencia_codigo_ocorrencia = O.codigo_ocorrencia
            WHERE
                O.ocorrencia_classificacao = 'ACIDENTE'
            GROUP BY
                F.Nome, F.Pais
            ORDER BY
                Numero_de_Acidentes DESC
        """)
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(list(resultados))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estatisticas/data-ultima-ocorrencia-fabricante')
def get_data_ultima_ocorrencia_fabricante():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                F.Nome AS Fabricante,
                (
                    SELECT DATE(MAX(E_sub.ocorrencia_dia))
                    FROM envolvida AS E_sub
                    INNER JOIN Aeronave AS A_sub ON E_sub.fk_Aeronave_aeronave_matricula = A_sub.aeronave_matricula
                    WHERE A_sub.fk_Fabricante_Nome = F.Nome
                ) AS Data_Ultima_Ocorrencia
            FROM Fabricante AS F
            ORDER BY Data_Ultima_Ocorrencia DESC
        """)
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        # Ajusta o formato da data para YYYY-MM-DD (apenas data)
        for item in resultados:
            data = item.get('Data_Ultima_Ocorrencia')
            if data:
                # Se vier como datetime/date, converte para string YYYY-MM-DD
                if hasattr(data, 'strftime'):
                    item['Data_Ultima_Ocorrencia'] = data.strftime('%Y-%m-%d')
                else:
                    # Se vier como string, tenta cortar só a parte da data
                    item['Data_Ultima_Ocorrencia'] = str(data).split(' ')[0]
        return jsonify(list(resultados))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para listar todos os fatores únicos
@app.route('/api/fatores-unicos')
def get_fatores_unicos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT fator_nome FROM Fator_contribuinte ORDER BY fator_nome
        """)
        fatores = [row['fator_nome'] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(fatores)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para listar aeronaves e recomendações por fator_nome
@app.route('/api/estatisticas/aeronaves-recomendacoes-por-fator/<fator_nome>')
def get_aeronaves_recomendacoes_por_fator(fator_nome):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT
                A.aeronave_matricula,
                A.aeronave_modelo,
                FC.fator_nome,
                R.recomendacao_conteudo
            FROM
                Ocorrencia AS O
            INNER JOIN
                Fatores AS FTS ON O.codigo_ocorrencia = FTS.fk_Ocorrencia_codigo_ocorrencia
            INNER JOIN
                Fator_contribuinte AS FC ON FTS.fk_Fator_contribuinte_fator_nome = FC.fator_nome
            INNER JOIN
                envolvida AS E ON O.codigo_ocorrencia = E.fk_Ocorrencia_codigo_ocorrencia
            INNER JOIN
                Aeronave AS A ON E.fk_Aeronave_aeronave_matricula = A.aeronave_matricula
            LEFT JOIN
                Possui AS P ON O.codigo_ocorrencia = P.fk_Ocorrencia_codigo_ocorrencia
            LEFT JOIN
                Recomendacao AS R ON P.fk_Recomendacao_recomendacao_numero = R.recomendacao_numero
            WHERE
                FC.fator_nome LIKE %s
        """, (fator_nome + '%',))
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(list(resultados))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Nova rota para top 10 matrículas de aeronaves com mais acidentes
@app.route('/api/estatisticas/top-matriculas-acidentes')
def get_top_matriculas_acidentes():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                A.aeronave_matricula,
                A.aeronave_modelo,
                FAB.Nome AS Fabricante,
                COUNT(O.codigo_ocorrencia) AS Total_Acidentes
            FROM
                Aeronave AS A
            INNER JOIN
                envolvida AS E ON A.aeronave_matricula = E.fk_Aeronave_aeronave_matricula
            INNER JOIN
                Ocorrencia AS O ON E.fk_Ocorrencia_codigo_ocorrencia = O.codigo_ocorrencia
            INNER JOIN
                Fabricante AS FAB ON A.fk_Fabricante_Nome = FAB.Nome
            WHERE
                O.ocorrencia_classificacao = 'ACIDENTE'
            GROUP BY
                A.aeronave_matricula,
                A.aeronave_modelo,
                FAB.Nome
            ORDER BY
                Total_Acidentes DESC
            LIMIT 10
        """)
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(list(resultados))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =================== MAIN ===================
if __name__ == '__main__':
    app.run(debug=True)
