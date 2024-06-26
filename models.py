import sqlite3
import aiosqlite
from traceback import print_exc
import os
global CURRENT_DIRECTORY
CURRENT_DIRECTORY= os.path.dirname(os.path.abspath(__file__))
db = os.path.join(CURRENT_DIRECTORY, 'criptomoedas.db')
import pandas as pd
import json

async def get_cripto_list(lista_de_criptomoedas=None):
    # Cria a tabela se ainda não existir
    try:
        # Conectar ao banco de dados de forma assíncrona
        async with aiosqlite.connect(db) as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS Cripto_list (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT,                   
                )
                ''')
            await conn.commit()
            print("Tabela Cripto_list criada com sucesso.")

        # Checar se a criptomoeda já existe na tabela
        cursor = await conn.execute('SELECT * FROM Cripto_list')
        registro = await cursor.fetchall()

        if registro and not lista_de_criptomoedas:
            return registro
        elif not registro and lista_de_criptomoedas:
            for nome in lista_de_criptomoedas:
                await conn.execute('INSERT INTO Cripto_list (Nome) VALUES (?)', (nome))
                await conn.commit()
            print("Criptomoedas inseridas na tabela Cripto_list com sucesso.")
            return lista_de_criptomoedas
        else:
            return None
    except Exception as e:
        return (f"Erro ao acessar banco de dados: {e}")

def criar_banco():
    try:
        # Conectar ao banco de dados (será criado se não existir)
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()

            # Criar a tabela para todas as criptomoedas
            cursor.execute( '''CREATE TABLE IF NOT EXISTS Estatisticas  (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Nome TEXT,
                                Maior_alta REAL,
                                Timestamp_alta INTEGER,
                                Maior_baixa REAL, 
                                Timestamp_baixa INTEGER, 
                                Timestamp INTEGER,                              
                                Criptomoeda TEXT
                              )''')

        print("Banco de dados e tabela Estatisticascriados com sucesso.")

    
        # Conectar ao banco de dados (será criado se não existir)
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()

            # Criar a tabela para todas as criptomoedas
            cursor.execute('''CREATE TABLE IF NOT EXISTS Criptomoedas (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Label TEXT,
                                Name TEXT,
                                Price REAL,
                                Volume_24h REAL,
                                Timestamp INTEGER,
                                Criptomoeda TEXT
                              )''')

        print("Banco de dados e tabela Criptomoedas criados com sucesso.")

    except sqlite3.Error as e:
        print("Erro ao criar o banco de dados:", e)

def salvar_dados_1m(crypto_data_1m):
    # Salvar as informações no banco de dados
    print("Salvando dados 1 mês no banco de dados...")
    try:
        conn = sqlite3.connect('criptomoedas.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS CryptoData_1m
                     (timestamp TEXT, low REAL, high REAL, open REAL, close REAL, volume REAL)''')
        print("tabela CryptoData_1m criada")
        # Converter DataFrame para lista de tuplas
        data_to_insert = [tuple(row) for row in crypto_data_1m.itertuples(index=False)]
        
        # Inserir os dados na tabela
        c.executemany('INSERT INTO CryptoData_1m VALUES (?,?,?,?,?,?,?)', data_to_insert)
        conn.commit()
        conn.close()
          
    except sqlite3.Error as e:
        print("Erro ao inserir dados:", e)
        return False
    
    return True

def salvar_dados_24h(crypto_data_24h):
    #salvar dataframe cripto_data_24h em um json com padas
    df = pd.DataFrame(crypto_data_24h)

    # Salvando o DataFrame em um arquivo JSON
    df.to_json('dados.json', orient='records')
        
    # Salvar as informações no banco de dados
    print("Salvando dados no banco de dados...")
    try:
        with sqlite3.connect(db) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS CryptoData_24h
                        (Nome TEXT, timestamp TEXT, low REAL, high REAL, open REAL, close REAL, volume REAL)''')
            print("tabela CryptoData_24h criada")
            # Converter DataFrame para lista de tuplas
            data_to_insert = [tuple(row) for row in crypto_data_24h.itertuples(index=False)]
            
            # Inserir os dados na tabela
            c.executemany('INSERT INTO CryptoData_24h VALUES (?,?,?,?,?,?,?)', data_to_insert)
          
    except sqlite3.Error as e:
        print("Erro ao inserir dados:", e)
        return False
    except Exception as e:
        print("Erro ao inserir dados:", e)
        return False

    print("Os dados foram 24h inseridos com sucesso.")
    return True

def inserir_dados(criptomoeda, dados):
    
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()

            # Inserir os dados na tabela de Criptomoedas
            cursor.execute('''INSERT INTO Criptomoedas (Label, Name, Price, Volume_24h, Timestamp, Criptomoeda) 
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (dados["Label"], dados["Name"], dados["Price"], dados["Volume_24h"], dados["Timestamp"], criptomoeda))

            print(f"{criptomoeda} inseridos com sucesso.")
            # print(f'{dados}\n')
    # if no such table, already exists
    except sqlite3.OperationalError as e:
        if e.args[0] == 'no such table: Criptomoedas':
            criar_banco()
            inserir_dados(criptomoeda, dados)
        else:
            print("Erro ao inserir dados:", e)

    except sqlite3.Error as e:
        print("Erro ao inserir dados:", e)

async def get_cripto_analise(data):
    Nome: str = data['Name']
    # print('\nAnalisando Criptomoeda:=====>\n', Nome)
    
    # print("\nCriptomoeda: \n", data)
    
    try:
        # Conectar ao banco de dados de forma assíncrona
        async with aiosqlite.connect(db) as conn:           

            # Checar se a criptomoeda já existe na tabela
            cursor = await conn.execute('SELECT * FROM Estatisticas WHERE Nome = ?', (data['Name'],))
            registro = await cursor.fetchone()

            if registro:
                # Atualiza o registro se necessário
                maior_alta = max(registro[2], data['Price'])
                timestamp_alta = data['Timestamp'] if max(registro[2], data['Price'])==data['Price'] else registro[3]
                maior_baixa = min(registro[4], data['Price'])
                timestamp_baixa = data['Timestamp'] if min(registro[4], data['Price'])==data['Price'] else registro[5]

                await conn.execute('UPDATE estatisticas SET Maior_alta = ?, Timestamp_alta = ?, Maior_baixa = ?, Timestamp_baixa = ?, Timestamp = ?  WHERE Nome = ?', 
                                   (maior_alta, timestamp_alta, maior_baixa, timestamp_baixa, data['Timestamp'], data['Name']))

                result = f"{data['Name']} ATUALIZADO com sucesso.\n"
            else:
                # Insere um novo registro caso não exista
                await conn.execute('INSERT INTO estatisticas (Nome, Maior_alta, Timestamp_alta, Maior_baixa, Timestamp_baixa, Timestamp, Criptomoeda) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (data['Name'], data['Price'], data['Timestamp'], data['Price'], data['Timestamp'], data['Timestamp'], data['Label']))

                result = f"{data['Name']} criado com sucesso.\n"

            await conn.commit()

            return result
    except sqlite3.Error as e:
        return f"Erro ao acessar banco de dados: {e}"


if __name__ == "__main__":

    # Exemplo de dados
    dados_solana = {
        "Label": "SOL/BRL",
        "Name": "Solana",
        "Price": 945.936597172600,
        "Volume_24h": 14897047382.094817672932109788,
        "Timestamp": 1711416180
    }

    dados_bitcoin = {
        "Label": "BTC/BRL",
        "Name": "Bitcoin",
        "Price": 30000.00,
        "Volume_24h": 50000000.00,
        "Timestamp": 1711416180
    }

    dados_ethereum = {
        "Label": "ETH/BRL",
        "Name": "Ethereum",
        "Price": 2000.00,
        "Volume_24h": 3000000.00,
        "Timestamp": 1711416180
    }

    # Criar o banco de dados e a tabela Criptomoedas
    criar_banco()

    # Inserir os dados nas tabelas correspondentes
    inserir_dados("SOLANA", dados_solana)
    inserir_dados("BITCOIN", dados_bitcoin)
    inserir_dados("ETHEREUM", dados_ethereum)
