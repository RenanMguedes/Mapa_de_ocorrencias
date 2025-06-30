# -*- coding: utf-8 -*-
import csv
import chardet

# --- Configuração ---
# Nome do arquivo CSV de entrada
arquivo_csv_entrada = 'relacao_.csv'
# Nome do arquivo SQL de saída
arquivo_sql_saida = 'inserts_Possui.sql'
# Nome da tabela no banco de dados
nome_tabela = 'possui' # Você pode alterar para o nome correto da sua tabela

print("Iniciando o processo de conversão...")

try:
    # --- Passo 1: Detectar a codificação do arquivo de entrada ---
    # Isso ajuda a evitar erros de leitura com caracteres especiais
    with open(arquivo_csv_entrada, 'rb') as f:
        resultado_chardet = chardet.detect(f.read())
        codificacao_detectada = resultado_chardet['encoding']
        print(f"Codificação do arquivo detectada: {codificacao_detectada}")

    # --- Passo 2: Ler o CSV e gerar os comandos INSERT ---
    # Abre o arquivo de entrada para leitura e o de saída para escrita
    with open(arquivo_csv_entrada, mode='r', encoding=codificacao_detectada, newline='') as f_entrada, \
         open(arquivo_sql_saida, mode='w', encoding='utf-8') as f_saida:

        # Lê a primeira linha para obter o cabeçalho
        leitor = csv.reader(f_entrada)
        cabecalho_raw = next(leitor)[0]

        # Separa o cabeçalho em duas colunas usando a barra como delimitador
        colunas = cabecalho_raw.split('/')
        if len(colunas) != 2:
            raise ValueError("O cabeçalho não contém os dois nomes de coluna esperados, separados por '/'.")

        # Junta os nomes das colunas para o comando SQL
        nomes_colunas_sql = f"`{colunas[0].strip()}`, `{colunas[1].strip()}`"
        
        print(f"Colunas identificadas: {nomes_colunas_sql}")
        print("Processando as linhas do arquivo...")

        # Itera sobre cada linha do arquivo CSV
        for i, linha_raw in enumerate(leitor, start=2):
            if not linha_raw:
                print(f"[Linha {i}] Ignorada: linha em branco.")
                continue

            # A estrutura do seu CSV parece ter os dois valores na primeira célula, separados por '/'
            linha_completa = linha_raw[0]

            # Separa os valores na primeira ocorrência da barra '/'
            try:
                valor1, valor2 = linha_completa.split('/', 1)
            except ValueError:
                print(f"[Linha {i}] Ignorada: não foi possível separar os valores. Linha: '{linha_completa}'")
                continue

            # --- Tratamento dos valores ---
            # Remove espaços em branco e aspas desnecessárias
            valor1_tratado = valor1.strip()
            valor2_tratado = valor2.strip().strip('"')

            # Escapa aspas simples dentro dos valores para evitar erros no SQL
            valor1_final = valor1_tratado.replace("'", "''")
            valor2_final = valor2_tratado.replace("'", "''")

            # Monta o comando INSERT para a linha atual
            # Usamos INSERT IGNORE para evitar erros de chave duplicada, caso existam
            insert_sql = f"INSERT IGNORE INTO `{nome_tabela}` ({nomes_colunas_sql}) VALUES ('{valor1_final}', '{valor2_final}');"

            # Escreve o comando no arquivo .sql
            f_saida.write(insert_sql + '\n')

    print(f"✅ Processo concluído! O arquivo '{arquivo_sql_saida}' foi gerado com sucesso.")

except FileNotFoundError:
    print(f"❌ ERRO: O arquivo de entrada '{arquivo_csv_entrada}' não foi encontrado.")
except Exception as e:
    print(f"❌ Ocorreu um erro inesperado: {e}")

