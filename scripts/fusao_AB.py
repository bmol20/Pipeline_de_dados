import csv # Importa a biblioteca para leitura e manipulação de arquivos CSV
import json # Importa a biblioteca para leitura e manipulação de arquivos JSON

# ============================
# 1. Leitura dos arquivos
# ============================

dados_csv = []

path_json = 'data_raw/dados_empresaA.json' # Indica onde está o arquivo JSON no sistema

with open(path_json, 'r') as file: # indica que arquivo JSON é apenas para leitura e carrega o caminho na variável file
    dados_json = json.load(file) # Carrega o arquivo, o transforma em uma lista de dicionários e salva na variável dados_json

# print(dados_json[0].keys()) # Faz a leitura da primeira linha, indicando os nomes das colunas no terminal

path_csv = 'data_raw/dados_empresaB.csv' # Indica onde está o arquivo CSV no sistema

with open(path_csv, 'r') as file: # indica que arquivo CSV é apenas para leitura e carrega o caminho na variável file
    spamreader = csv.DictReader(file, delimiter=",")
    # Carrega o arquivo, o transforma em uma lista de dicionários separados por "," e salva na variável dados_csv
    for row in spamreader:
        dados_csv.append(row) # Adiciona os dados do spamreader para a variável dados_csv linha a linha

# print(dados_csv[0].keys()) # Faz a leitura da primeira linha, indicando os nomes das colunas no terminal

# ============================
# 2. Manipulação dos dados
# ============================

key_mapping = {'Nome do Item': 'Nome do Produto',
                'Classificação do Produto': 'Categoria do Produto',
                'Valor em Reais (R$)': 'Preço do Produto (R$)',
                'Quantidade em Estoque': 'Quantidade em Estoque',
                'Nome da Loja': 'Filial',
                'Data da Venda': 'Data da Venda'} # Indica os nomes para padronizar as colunas

new_dados_csv = [] # Lista onde iremos salvar os dados após serem tratados

for old_dict in dados_csv: # old_dict irá ler linha por linha de dados_csv
    dict_temp = {} # Variável temporária para salvar as alterações realizadas em cada repetição "for" e guardar na nova variável
    for old_key, value in old_dict.items(): # items() irá atribuir a chave e o valor de cada linha de dados_csv
        dict_temp[key_mapping[old_key]] = value # Adiciona cada valor da antiga lista a nova chave
    new_dados_csv.append(dict_temp) # Salva os dados temporários na lista nova

combined_list = [] # Cria a variável onde o programa irá mesclar os dois arquivos
combined_list.extend(dados_json) # Inclui a variável em JSON
combined_list.extend(new_dados_csv) # Inclui a variável em CSV

nomes_colunas = list(combined_list[-1].keys()) # Salva o nome das colunas em uma lista para utilizar futuramente

dados_combinados_tabela = [nomes_colunas] 
# Variável criada para corrigir a falta de dados em uma coluna, por conta da diferença de tabelas. Além de ser criada para salvar
# arquivos no formato de CSV padrão ao invés do dict. Foi adicionado a primeira linha os nomes das colunas

for row in combined_list: # For criado para adicionar todas as informações a nova tabela corrigida
    linha = [] # Variável temporária para armazena linha a linha do antigo CSV
    for coluna in nomes_colunas:
        linha.append(row.get(coluna,'Indisponível')) # Preenche com 'Indisponível' caso a coluna não exista em uma das origens de dados
    
    dados_combinados_tabela.append(linha) # Inserindo os dados na tabela

# ============================
# 3. Escrita de dados
# ============================

path_dados_combinados = 'data_processed/dados_combinados.csv' # Indica o caminho onde iremos salvar a lista de dados corrigida

with open(path_dados_combinados, 'w') as file: # Indica que o caminho informado é para escrita e foi armazenado em file
    writer = csv.DictWriter(file, fieldnames=nomes_colunas) # Salva os nomes das colunas na variável writer e o caminho
    writer.writeheader() # Salva no arquivo os nomes das colunas

    for row in combined_list: # Percorre linha a linha da lista e armazena na variável "row"
        writer.writerow(row) # Salva linha a linha da lista no arquivo no sistema em formato de dict

path_dados_combinados_tabela = 'data_processed/dados_combinados_tabela.csv'
# Indica o caminho onde iremos salvar a lista de dados corrigida

with open(path_dados_combinados_tabela, 'w') as file: # Indica que o caminho informado é para escrita e foi armazenado em file
    writer = csv.writer(file) # Salva os nomes das colunas na variável writer e o caminho
    writer.writerows(dados_combinados_tabela) # Salva linha a linha da lista no arquivo no sistema no formato CSV