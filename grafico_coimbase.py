from datetime import datetime, timedelta
import pandas as pd
import requests
import matplotlib.pyplot as plt
import os


global CURRENT_DIRECTORY
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_crypto_data(product_id, start_date, end_date, granularity):
    # Montar URL
    url = f"https://api.exchange.coinbase.com/products/{product_id}/candles"

    # Delta é o incremento de tempo de uma vela para outra
    delta = timedelta(seconds=granularity)

    # Coinbase's limitation
    max_candles = 300

    # Nós adicionaremos os resultados em cada iteração a esta lista
    results = []

    # Iterar sobre o intervalo
    while start_date < end_date:
        # Obter próxima data. É a data atual + incremento se ainda estiver dentro do intervalo,
        # senão é a data final
        next_date = start_date + max_candles * delta
        next_date = next_date if next_date < end_date else end_date

        # Certifique-se de passar as datas como ISO
        params = {
            "start": start_date.isoformat(),
            "end": next_date.isoformat(),
            "granularity": granularity
        }

        headers = {"content-type": "application/json"}

        data = requests.get(url, params=params, headers=headers)
        data = data.json()

        # Certifique-se de adicionar os dados mais recentes no topo da lista
        results = data + results

        # Atualize o cursor
        start_date = next_date

    # Criar um DataFrame com os resultados
    df = pd.DataFrame(data=results, columns=['timestamp', "low", "high", "open", "close", "volume"])

    # Converter o timestamp para datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    return df

def plot_crypto_data(data, title, save_path=None):
    # Plotar o gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(data['timestamp'], data['close'], marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel('Tempo')
    plt.ylabel('Preço (USD)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Salvar o gráfico em um arquivo PNG, se o caminho de salvamento for fornecido
    if save_path:
        plt.savefig(save_path)
        plt.close()
        return save_path
    else:
        plt.show()


def ober_24h(moeda, save_path=None):
  # Obter os dados das últimas 24 horas
  end_date = datetime.now()
  start_date_24h = end_date - timedelta(days=1)
  crypto_data_24h = get_crypto_data(
      product_id=moeda,
      start_date=start_date_24h,
      end_date=end_date,
      granularity=900
  )
  if save_path is None:
    # Plotar o gráfico das 24 horas
    plot_crypto_data(crypto_data_24h, 'Variação do Preço do Bitcoin nas Últimas 24 Horas')
  else:
    # Plotar o gráfico das 24 horas e salva-o em um arquivo
    png_path_24h = plot_crypto_data(crypto_data_24h, 'Variação do Preço do Bitcoin nas Últimas 24 Horas', save_path=save_path)
    return png_path_24h
  
def ober_1mes(moeda, save_path=None):
  end_date = datetime.now()
  # Obter os dados do último mês
  start_date_1m = end_date - timedelta(days=30)
  crypto_data_1m = get_crypto_data(
      product_id=moeda,
      start_date=start_date_1m,
      end_date=end_date,
      granularity=86400  # Um dia em segundos
  )
  if save_path is None:
    # Plotar o gráfico do último mês
    plot_crypto_data(crypto_data_1m, 'Variação do Preço do Bitcoin no Último Mês')
  else:
    # Plotar o gráfico do último mês e salva-o em um arquivo
    png_path_1m = plot_crypto_data(crypto_data_1m, 'Variação do Preço do Bitcoin no Último Mês', save_path=save_path)
    return png_path_1m

if __name__ == "__main__":
  print(ober_24h('BTC-USD', 'BTC-USD_24h.png'))
  print(ober_1mes('BTC-USD', 'BTC-USD_1m.png'))
  