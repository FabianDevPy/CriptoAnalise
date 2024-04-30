from flask import Flask, render_template, request, url_for, make_response, send_file,Response
from script import converter_timestamp, aware_utcnow
from flask import jsonify
import sqlite3
from coinbase_api import get_crypto_data
import time
import datetime
from datetime import timezone, timedelta
import json
import os
from graficos_coinbase import ober_1mes, ober_24h

import asyncio
from graficos_coinbase import execute_routine

from PIL import Image
import io

from io import BytesIO

from flask_cors import CORS

global CURRENT_DIRECTORY
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=os.path.join(CURRENT_DIRECTORY, 'static'))
#template folder
app.template_folder = os.path.join(CURRENT_DIRECTORY, 'templates')
template_folder = app.template_folder
CORS(app)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# @app.route("/grafico24h/<criptomoeda>")
# def grafico24h(criptomoeda):
#     grafico = ober_24h(criptomoeda, os.path.join(f'/graficos/{criptomoeda}_24h.png'))   
#     return render_template("grafico24h.html", grafico=grafico)

@app.route("/grafico24h/<criptomoeda>")
def grafico24h(criptomoeda):
    grafico = f'graficos/{criptomoeda}_24h.png'    
    return render_template("grafico24h.html", criptomoeda=criptomoeda, grafico=grafico)



@app.route("/criptolist")
def criptolist():
    with open(os.path.join(CURRENT_DIRECTORY, 'lista_de_criptomoedas.json'), 'r') as f:
        criptomoedas = json.load(f)
    return jsonify(criptomoedas)

@app.route("/criptodiponivel")
def criptodiponivel():
    with open(os.path.join(CURRENT_DIRECTORY, 'lista_de_criptomoedas_disponiveis.json'), 'r') as f:
        criptomoedas = json.load(f)
    return jsonify(criptomoedas)

@app.route("/editarlista", methods=['POST'])
def editarlista():
    try:
        lista = request.get_json()
        print("lista: ", lista)
        with open(os.path.join(CURRENT_DIRECTORY, 'lista_de_criptomoedas.json'), 'w') as f:
            json.dump(lista, f)
        return jsonify({'status': 'ok'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route("/demo_1")
def demo1():
    return render_template("demo_1.html")

@app.route('/api/analise/<criptomoeda>', methods=['GET'])
def analise(criptomoeda):
    # criptomoeda = request.args.get('criptomoeda') 
    try:
        graficos_array = []
        pasta_graficos = os.path.join(CURRENT_DIRECTORY, 'static', 'graficos')
        for arquivo in os.listdir(pasta_graficos):
            if arquivo.endswith('.png'):
                graficos_array.append(arquivo)
        with sqlite3.connect(os.path.join(CURRENT_DIRECTORY, 'criptomoedas.db')) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM estatisticas WHERE Nome = ?", (criptomoeda,))
            registro = cursor.fetchall()
            
            if registro:     
                grafico_24h = f'/graficos/{registro[0][7]}_24h.png'
                grafico_1m = f'/graficos/{registro[0][7]}_1m.png'              
                registro_dict = {
                'Name': registro[0][1],
                'Maior': registro[0][2],
                'timestamp_max':converter_timestamp( registro[0][3] )["Hora"],
                'Menor': registro[0][4],
                'timestamp_min':converter_timestamp( registro[0][5] )["Hora"],
                'Timestamp': converter_timestamp(registro[0][6] )["Data"],
                'Label': registro[0][7], 
                "grafico_24h":  grafico_24h,
                'grafico_1m': grafico_1m
               
                }
                
                
                   
                    
                    
            return registro_dict
            
    except sqlite3.Error as e:
        print("Erro ao obter dados:", e)
        return jsonify(e.args)    
    
@app.route('/api/criptomoedas', methods=['GET'])
def get_criptomoedas():
    try:
        # Conexão com o banco de dados (substitua pelos seus detalhes de conexão)
        conn = sqlite3.connect(os.path.join(CURRENT_DIRECTORY, 'criptomoedas.db')) as conn:
        cursor = conn.cursor()
        # Consulta SQL para obter os dados das criptomoedas
        query ='SELECT Name, Label, Price, Volume_24h, MAX(Timestamp) AS Max_Timestamp FROM criptomoedas GROUP BY Name;'
        cursor.execute(query)
        
        # Obter os resultados da consulta
        criptomoedas = cursor.fetchall()
        
        # Converter os resultados para um formato JSON
        criptomoedas_json = []
        with open(os.path.join(CURRENT_DIRECTORY, 'lista_de_criptomoedas.json'), 'r') as f:
            lsta_de_criptomoedas = json.load(f)
        
        
        for criptomoeda in criptomoedas:

            if criptomoeda[0] in lsta_de_criptomoedas:
                timestamp = criptomoeda[4]           
                # Criando o dicionário para cada criptomoeda
                criptomoeda_dict = {
                    'Name': criptomoeda[0],
                    'Label': criptomoeda[1],
                    'Price': criptomoeda[2],
                    'Volume_24h': criptomoeda[3],
                    'Timestamp': timestamp,
                    'Data': converter_timestamp(timestamp)["Data"],  # Corrigido: uso de strftime diretamente
                    'Hora': converter_timestamp(timestamp)["Hora"],   # Corrigido: uso de strftime diretamente
                    }
                criptomoedas_json.append(criptomoeda_dict)
            else:
                print("criptomoeda nao encontrada: ", criptomoeda[0])	   
        # Fechar a conexão com o banco de dados
        conn.close()
        
        # Retornar os dados JSON como resposta da rota
        return jsonify(criptomoedas_json)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/<criptomoeda>', methods=['GET'])
def get_criptomoeda(criptomoeda):
    print(criptomoeda)
    if not criptomoeda.isalpha():
        criptomoeda = criptomoeda.upper()
    if len(criptomoeda) == 3:
        criptomoeda = str(criptomoeda+'-brl').upper()
    if len(criptomoeda) == 7:
        pass
    else:
        return jsonify({'error': 'Invalid criptomoeda'}), 400
    try:
        print(criptomoeda)
        # Obtenha a hora atual no formato correto
        hora_atual = aware_utcnow().strftime("%H:%M:%S")        

        # Obtenha a data e hora atual
        data_atual = datetime.datetime.now().strftime("%Y-%m-%dT")
        
        start_date = data_atual + '00:00:00'
        
        # Concatene a data e hora atual com a hora atual formatada
        end_date = data_atual + hora_atual


        # Agora você pode usar start_date e end_date na sua chamada get_crypto_data
        _data = get_crypto_data(
            product_id=criptomoeda,
            start_date=start_date,
            end_date=end_date,
            granularity=900
        )        

        return _data

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@app.route('/executar-rotina', methods=['GET'])
def executar_rotina():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(execute_routine())
        return jsonify({'success': True, 'result': "result"}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/progresso', methods=['GET'])
def progresso():
    slug = request.args.get('slug')
    print("slug: ", slug)
    # progress_bar_path = os.path.join(app.template_folder, 'progress_bar.html')
    # return send_file(progress_bar_path)
from flask import send_from_directory

# Rota para servir imagens de 24 horas
# @app.route('/graficos/<nome_moeda>/24h')
# def enviar_grafico_24h(nome_moeda):
    
#     return send_from_directory(directory='caminho/para/static/graficos',filename= f'{nome_moeda}_24h.png')

# # Rota para servir imagens de 1 mês
# @app.route('/graficos/<nome_moeda>/1m')
# def enviar_grafico_1m(nome_moeda):  
#     nome_moeda = nome_moeda.replace('-BRL', '-USD')

#     with open (f'{CURRENT_DIRECTORY}/static/graficos/{nome_moeda}_1m.png', 'rb') as image:        
#         image_name = image.filename.split(".")[0] + ".png"
#         image = Image.open(image)
#         image = image.convert("RGB")
#         byte_io=io.BytesIO()
#         image.save(byte_io,"PNG" )
#         byte_io.seek(0)
#         response=Response(byte_io, content_type='image/png')
#         response.headers.set('Content-Disposition', 'attachment', filename={image_name})
#         print(response.headers)
   
#     return response

@app.route('/graficos/<path:filename>')
def servir_imagem(filename):
    return send_from_directory(os.path.join(app.static_folder, 'graficos'), filename)


if __name__ == '__main__':
    app.run(debug=True)