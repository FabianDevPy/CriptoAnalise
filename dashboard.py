import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation
from threading import Thread

# Configuração inicial dos subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

def run_in_threads(func):
    thead = Thread(target=func)
    thead.start()
    return thead
    
# Função para obter os dados de uma tabela
def obter_dados(criptomoeda):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('criptomoedas.db')
        cursor = conn.cursor()

        # Executar a consulta na tabela correspondente
        cursor.execute(f"SELECT * FROM {criptomoeda} ORDER BY Timestamp DESC LIMIT 20")
        dados = cursor.fetchall()

        return dados

    except sqlite3.Error as e:
        print("Erro ao obter dados:", e)
        #no such table

    finally:
        # Fechar a conexão com o banco de dados
        if conn:
            conn.close()

# Função para atualizar os dados dos gráficos
def atualizar_graficos(frame):
    for ax, criptomoeda in zip(axes.flat, ['SOLANA', 'BITCOIN', 'ETHEREUM']):
        dados = obter_dados(criptomoeda)
        if dados:
            ax.clear()
            labels = []
            prices = []
            for dado in dados:
                labels.append(datetime.fromtimestamp(dado[4]).strftime('%H:%M:%S'))
                prices.append(dado[2])

            ax.plot(labels, prices)
            ax.set_title(f'Gráfico de Preços - {criptomoeda}')
            ax.set_xlabel('Timestamp')
            ax.set_ylabel('Price')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True)

def animate():
    while True:
        atualizar_graficos(0)

# Iniciar a animação em uma thread separada
run_in_threads(animate)

# Mostrar os gráficos
plt.tight_layout()
plt.show()
