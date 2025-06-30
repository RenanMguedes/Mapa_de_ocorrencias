import csv
import chardet

arquivo_csv = 'entidade_OcorrenciaOK.csv'
nome_tabela = 'ocorrencia'
output_file = 'inserts_ocorrencia.sql'

# 🔍 Detectar a codificação do arquivo CSV
with open(arquivo_csv, 'rb') as f:
    resultado = chardet.detect(f.read())
    codificacao_detectada = resultado['encoding']
    print(f"Codificação detectada: {codificacao_detectada}")

# ✅ Abrir o CSV com a codificação correta e salvar o .sql em UTF-8
with open(arquivo_csv, encoding=codificacao_detectada) as f, open(output_file, 'w', encoding='utf-8') as saida:
    leitor = csv.reader(f, delimiter=',')  # <--- aqui está a correção
    colunas = next(leitor)

    for i, linha in enumerate(leitor, start=2):
        if len(linha) != len(colunas):
            print(f"Linha {i} com erro: número de colunas incorreto. Ignorada.")
            continue

        valores_tratados = []
        for v in linha:
            if v.strip() == '':
                valores_tratados.append('NULL')
            else:
                try:
                    float(v)
                    valores_tratados.append(v)
                except ValueError:
                    v = v.replace("'", "''")
                    valores_tratados.append(f"'{v}'")

        insert_sql = f"INSERT IGNORE INTO {nome_tabela} ({', '.join(colunas)}) VALUES ({', '.join(valores_tratados)});"
        saida.write(insert_sql + '\n')
