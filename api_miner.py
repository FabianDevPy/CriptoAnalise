import requests
import time
from models import inserir_dados, get_cripto_analise
from script import limpar_banco, criar_banco
from graficos_coinbase import ober_1mes, ober_24h, gerar_grafico
import asyncio
import json
import os

global CURRENT_DIRECTORY 
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
   
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta uma exceção para respostas de erro HTTP
        data = response.json()
        return data.get('Markets', [])[0]
    except requests.RequestException as e:
        print(f"Erro ao buscar dados: {e}")
        return None

async def get_lista_de_criptomoedas(markets):
    _lista = []
    for crypto in markets:
        name  = crypto.get('Name')    
        _lista.append(name)    
    return _lista
    
async def process_data(markets: list, criptomoedas: list = None):   
    processed_data: dict = {}
    lista_de_criptomoedas: list = criptomoedas or []  
      
    try:
        with open(os.path.join(CURRENT_DIRECTORY, 'lista_de_criptomoedas.json'), 'r') as _lc:
            lista_de_criptomoedas = json.load(_lc)
        
    except Exception as e:
        print(e)
        
        _lc_filtrada: list = ["Bitcoin", "Ethereum", "Solana", "Polkadot", "Stellar", "Tether", "Dogecoin", "Dai", "Cardano", "Litecoin", "Chainlink", "Binance USD", "Polygon"]
        with open(os.path.join(CURRENT_DIRECTORY, 'lista_de_criptomoedas.json'), 'w') as _lc:
            json.dump(_lc_filtrada, _lc)
            
    try:
        with open(os.path.join(CURRENT_DIRECTORY, 'lista_de_criptomoedas_disponiveis.json'), 'r') as _lc:
            print("Lista de criptomoedas disponiveis: ")
            
    except Exception as e:
        print(e)
        lista_de_criptomoedas: list = await get_lista_de_criptomoedas(markets)
        
        with open(os.path.join(CURRENT_DIRECTORY, 'lista_de_criptomoedas_disponiveis.json'), 'w') as _lc:
            json.dump(lista_de_criptomoedas, _lc)
        
    for crypto in markets:
        
        name: str = crypto.get('Name')
        label = crypto.get('Label').replace('/BRL', '-USD'),
        # print("name: ", name, "label: ", label[0])
        
        if name and name in lista_de_criptomoedas:
            
            processed_data[name] = {
                'Name': name,
                'Label': label[0],
                'Price': crypto.get('Price', 0),
                'Volume_24h': crypto.get('Volume_24h', 0),
                'Timestamp': crypto.get('Timestamp', 0)
            }
            
            _analise = await get_cripto_analise(processed_data[name])
            print(_analise)
    
    return processed_data

async def main():
    try:
        url = 'https://www.worldcoinindex.com/apiservice/v2getmarkets?key=yTsY100fwhLAq98kro3wSSwyXTAku8vNFJQ&fiat=brl'
        while True:
            markets = fetch_data(url)
            processed_data = await process_data(markets) 
            limpar_banco()
            graph_list: list = []
            
            for currency, info in processed_data.items():
                print(info["Label"])
                graph_list.append( info["Label"])    
                        
                inserir_dados(currency.upper(), info)       
            # time.sleep(60)  # Intervalo de 1 minuto
            # Executar as tarefas assíncronas usando o loop de eventos padrão
            tasks = [gerar_grafico(moeda=item) for item in graph_list]
            await asyncio.gather(*tasks)
            time.sleep(60)  # Intervalo de 1 minuto
            
    except Exception as e:
        print(e)
                
if __name__ == "__main__":
    print("Executando...")
    asyncio.run(main())
