import asyncio
from datetime import datetime, timedelta
import os
import pandas as pd
import aiohttp
import matplotlib.pyplot as plt
import traceback
import json

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
        try:
            data = await fetch_data(url, params, headers)
            if type(data) == list and type(results) == list:
                results.extend(data)
                start_date = next_date
            else:
                print(data)
                print(f"Error getting data for {product_id}: {data}")
                break
        except:
            # print_exc()
            print(f"Error getting data for {product_id}: {data}")
            break

    df = pd.DataFrame(data=results, columns=['timestamp', "low", "high", "open", "close", "volume"])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')  # Converta o timestamp para o formato de data/hora
    return df


async def obter_24h(moeda):
    end_date = datetime.now()
    start_date_24h = end_date - timedelta(days=1)

    crypto_data_24h = await get_crypto_data(
        product_id=moeda,
        start_date=start_date_24h,
        end_date=end_date,
        granularity=900
    )

    if crypto_data_24h is None:
        return None

    return crypto_data_24h


async def obter_1mes(moeda):
    end_date = datetime.now()
    start_date_1m = end_date - timedelta(days=30)

    crypto_data_1m = await get_crypto_data(
        product_id=moeda,
        start_date=start_date_1m,
        end_date=end_date,
        granularity=86400
    )

    if crypto_data_1m is None:
        return None
  
    return crypto_data_1m

async def obter_1hora(moeda):
    end_date = datetime.now()
    start_date_1h = end_date - timedelta(hours=1)

    crypto_data_1h = await get_crypto_data(
        product_id=moeda,
        start_date=start_date_1h,
        end_date=end_date,
        granularity=60  # Granularidade de 60 segundos para 1 hora
    )

    if crypto_data_1h is None:
        return None

    return crypto_data_1h

async def obter_1semana(moeda):
    end_date = datetime.now()
    start_date_1w = end_date - timedelta(days=7)

    crypto_data_1w = await get_crypto_data(
        product_id=moeda,
        start_date=start_date_1w,
        end_date=end_date,
        granularity=86400  # Granularidade de 86400 segundos para 1 dia (1 semana tem 7 dias)
    )

    if crypto_data_1w is None:
        return None

    return crypto_data_1w

async def obter_1ano(moeda):
    end_date = datetime.now()
    start_date_1y = end_date - timedelta(days=365)

    crypto_data_1y = await get_crypto_data(
        product_id=moeda,
        start_date=start_date_1y,
        end_date=end_date,
        granularity=86400  # Granularidade de 86400 segundos para 1 dia
    )

    if crypto_data_1y is None:
        return None

    return crypto_data_1y
async def gerar_grafico(moeda='BTC-USD'):
    try:
        result_24h, result_1m = await asyncio.gather(obter_24h(moeda), obter_1mes(moeda))

        if result_24h and result_1m:
            series = [result_24h, result_1m]
            print(f"Os dados de 24 horas foram inseridos com sucesso.")
            return series
        else:
            print(f"Erro ao obter dados de {moeda}")
            return []

    except Exception as e:
        print(f"Erro ao obter dados: {e}")
        print(traceback.format_exc())
        return []


if __name__ == '__main__':
    asyncio.run(gerar_grafico(moeda='op-usd'))
