import requests
import json
import sys
from pathlib import Path

def test_healt():
    x = requests.get('http://0.0.0.0:8080/api/health')
    return x.json()

def test_query():
    url = 'http://0.0.0.0:8080/api/inference'
    payload = { "query": "Oye haz la función de fibonacci en TypeScript",
                "system_prompt": "Eres un asistente útil y conciso.",
                "stream": False}
    x = requests.post(url, json=payload)
    return x.json()

def test_query_stream():
    url = 'http://0.0.0.0:8080/api/inference'
    payload = {
        "query": "Oye haz la función de fibonacci en TypeScript",
        "system_prompt": "Eres un asistente útil y conciso.",
        "stream" : True
    }
    
    # Usar stream=True en la petición para recibir la respuesta por partes
    response = requests.post(url, json=payload, stream=True)
    
    if response.status_code == 200:
        # Procesar la respuesta SSE línea por línea
        for line in response.iter_lines():
            if line:
                # Las líneas SSE comienzan con "data: "
                line = line.decode('utf-8')
                if line.startswith('data:'):
                    # Extraer el JSON después de "data: "
                    json_str = line[6:]  # Saltamos los primeros 6 caracteres ("data: ")
                    try:
                        chunk_data = json.loads(json_str)
                        chunk = chunk_data.get('chunk', '')
                        sys.stdout.write(chunk)
                        sys.stdout.flush()
                    except json.JSONDecodeError as e:
                        print(f"Error decodificando JSON: {e}")
    else:
        print(f"Error: {response.status_code}")
        try:
            print(response.json())
        except:
            print(response.text)

def test_query_stream_multimodal():
    url = 'http://0.0.0.0:8080/api/inference'

    image_path = Path("Logo.png").resolve()
    
    # Convertir a string para asegurar compatibilidad
    image_path_str = str(image_path)
    
    print(f"Usando ruta completa: {image_path_str}")

    payload = {
        "query": "Oye describe la imagen que te estoy pasando",
        "system_prompt": "Eres un asistente útil y conciso.",
        "image_path" : image_path_str,
        "stream" : True
    }
    
    # Usar stream=True en la petición para recibir la respuesta por partes
    response = requests.post(url, json=payload, stream=True)
    
    if response.status_code == 200:
        # Procesar la respuesta SSE línea por línea
        for line in response.iter_lines():
            if line:
                # Las líneas SSE comienzan con "data: "
                line = line.decode('utf-8')
                if line.startswith('data:'):
                    # Extraer el JSON después de "data: "
                    json_str = line[6:]  # Saltamos los primeros 6 caracteres ("data: ")
                    try:
                        chunk_data = json.loads(json_str)
                        chunk = chunk_data.get('chunk', '')
                        sys.stdout.write(chunk)
                        sys.stdout.flush()
                    except json.JSONDecodeError as e:
                        print(f"Error decodificando JSON: {e}")
    else:
        print(f"Error: {response.status_code}")
        try:
            print(response.json())
        except:
            print(response.text)

query = test_query_stream_multimodal()

print(query)


#health = test_healt()
#query = test_query_stream()
#print(health)
#print(query)
