import pandas as pd
import re

# Função para formatar a latitude/longitude
def formatar_coordenada(coordenada):
    # Converte para string para evitar erro com float ou NaN
    coordenada = str(coordenada).strip()
    # Verifica se é um valor vazio ou inválido
    if coordenada == '' or coordenada == '.' or coordenada == '***' or coordenada.lower() == 'nan':
        return ''
    try:
        # Remove qualquer caractere que não seja número, ponto ou traço
        coordenada = re.sub(r'[^0-9\.-]', '', coordenada)
        # Se tiver mais de um ponto, remove todos os pontos exceto o primeiro
        if coordenada.count('.') > 1:
            coordenada = coordenada.split('.')[0] + '.' + coordenada.split('.')[1]
        # Se não tem ponto, insere após os dois primeiros dígitos (após o sinal)
        if '.' not in coordenada:
            sinal = ''
            num = coordenada
            if coordenada.startswith('-'):
                sinal = '-'
                num = coordenada[1:]
            if len(num) > 2:
                coordenada = f"{sinal}{num[:2]}.{num[2:]}"
            else:
                return ''
        valor = float(coordenada)
        # Validação de faixa para latitude e longitude do Brasil
        if -80 <= valor <= 0 or 0 <= valor <= -30:  # longitude (negativa, Brasil)
            return f"{valor:.8f}"
        if -33 <= valor <= 5:  # latitude
            return f"{valor:.8f}"
        return ''
    except ValueError:
        # Se não for um número válido, retorna vazio
        return ''

# Carregar o arquivo CSV
df = pd.read_csv('entidade_OcorrenciaOK.csv')

# Verificar e corrigir as colunas de latitude e longitude
df['ocorrencia_longitude'] = df['ocorrencia_longitude'].apply(formatar_coordenada)
df['ocorrencia_latitude'] = df['ocorrencia_latitude'].apply(formatar_coordenada)

# Salvar o DataFrame modificado em um novo arquivo CSV
df.to_csv('ocorrencias_corrigidas.csv', index=False)

print("Arquivo CSV corrigido com sucesso!")