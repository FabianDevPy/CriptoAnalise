import asyncio
from datetime import datetime, timedelta
import os
import pandas as pd
import aiohttp
import matplotlib.pyplot as plt

global CURRENT_DIRECTORY
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


async def fetch_data(url, params, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            return await response.json()


async def get_crypto_data(product_id, start_date, end_date, granularity):
    url = f"https://api.exchange.coinbase.com/products/{product_id}/candles"

    delta = timedelta(seconds=granularity)
    max_candles = 300
    results = []

    while start_date < end_date:
        next_date = start_date + max_candles * delta
        next_date = next_date if next_date < end_date else end_date

        params = {
            "start": start_date.isoformat(),
            "end": next_date.isoformat(),
            "granularity": granularity
        }
        headers = {"content-type": "application/json"}

        data = await fetch_data(url, params, headers)
        results = data + results

        start_date = next_date

    df = pd.DataFrame(data=results, columns=['timestamp', "low", "high", "open", "close", "volume"])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    return df


def plot_crypto_data(data, title, save_path=None):
    plt.figure(figsize=(10, 5))
    plt.plot(data['timestamp'], data['close'], marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel('Tempo')
    plt.ylabel('Preço (USD)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
        return save_path
    else:
        plt.show()


async def ober_24h(moeda, save_path=None):
    end_date = datetime.now()
    start_date_24h = end_date - timedelta(days=1)
    crypto_data_24h = await get_crypto_data(
        product_id=moeda,
        start_date=start_date_24h,
        end_date=end_date,
        granularity=900
    )
    if save_path is None:
        plot_crypto_data(crypto_data_24h, f"{moeda} nas Últimas 24 Horas: {start_date_24h.strftime('%H:%M')} a {end_date.strftime('%H:%M')}")
    else:
        png_path_24h = plot_crypto_data(crypto_data_24h, f"{moeda} nas Últimas 24 Horas: {start_date_24h.strftime('%D%M - %H:%M')} a {end_date.strftime('%D%M - %H:%M')}",
                                        save_path=save_path)
        return png_path_24h


async def ober_1mes(moeda, save_path=None):
    end_date = datetime.now()
    start_date_1m = end_date - timedelta(days=30)
    crypto_data_1m = await get_crypto_data(
        product_id=moeda,
        start_date=start_date_1m,
        end_date=end_date,
        granularity=86400
    )
    if save_path is None:
        plot_crypto_data(crypto_data_1m, f'{moeda} no Último Mês: {start_date_1m.strftime("%d/%m/%Y")} a {end_date.strftime("%d/%m/%Y")}')
    else:
        png_path_1m = plot_crypto_data(crypto_data_1m, f'{moeda} no Último Mês: {start_date_1m.strftime("%d/%m/%Y")} a {end_date.strftime("%d/%m/%Y")}',
                                       save_path=save_path)
        return png_path_1m


async def execute_routine(moeda='BTC-USD'):
    try:
        await asyncio.gather(
            ober_24h(moeda, f'{CURRENT_DIRECTORY}/static/graficos/{moeda}_24h.png'),
            ober_1mes(moeda, f'{CURRENT_DIRECTORY}/static/graficos/{moeda}_1m.png')
        )
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

async def gerar_grafico(moeda: str):
    print(f"Gerando gráfico para {moeda}")
    
    try:
        await execute_routine(moeda = moeda.upper())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    asyncio.run(gerar_grafico(moeda='op-usd'))