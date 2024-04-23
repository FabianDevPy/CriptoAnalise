import sqlite3
from datetime import datetime, timezone, timedelta
import pytz

def converter_timestamp(timestamp):
    br_timezone = timezone(timedelta(hours=-4))
    utc_br = datetime.fromtimestamp(timestamp, tz=br_timezone)
    print(utc_br.strftime('%Y-%m-%d'))
    return {'Data': utc_br.strftime('%m-%d'),  
            'Hora': utc_br.strftime('%H:%M')}

def criar_banco():
    try:
        # Conectar ao banco de dados (será criado se não existir)
        with sqlite3.connect('criptomoedas.db') as conn:
            cursor = conn.cursor()

            # Criar a tabela para todas as criptomoedas
            cursor.execute('''CREATE TABLE IF NOT EXISTS Estatisticas  (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Nome TEXT,
                                maior_alta REAL,
                                maior_baixa REAL,                                
                                data_hora INTEGER,
                                Timestamp INTEGER,
                                Criptomoeda TEXT,
                                Preco REAL
                              )''')

        print("Banco de dados e tabela criados com sucesso.")

    except sqlite3.Error as e:
        print("Erro ao criar o banco de dados:", e)

def limpar_banco():
    try:
        # Conectar ao banco de dados (será criado se não existir)
        with sqlite3.connect('criptomoedas.db') as conn:
            cursor = conn.cursor()

            # Contar quantos registros existem na tabela Criptomoedas
            cursor.execute("SELECT COUNT(*) FROM Criptomoedas")
            quantidade_registros = cursor.fetchone()[0]

            # Verificar se há mais de 500 registros antes de deletar
            if quantidade_registros >= 500:
                cursor.execute('''DELETE FROM Criptomoedas
                                WHERE id NOT IN (
                                  SELECT id
                                  FROM Criptomoedas
                                  ORDER BY Timestamp DESC
                                  LIMIT 100
                                );
                                ''')
                print("Banco de dados e tabela limpo com sucesso.")
            else:
                print("Não há mais de 500 registros na tabela, não é necessário limpar.")

    except sqlite3.Error as e:
        print("Erro ao criar o banco de dados:", e)

def aware_utcnow():    
    return datetime.now(pytz.timezone('America/Sao_Paulo'))

if __name__ == '__main__':
    
    print(aware_utcnow())
  
    