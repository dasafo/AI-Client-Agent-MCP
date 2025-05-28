import requests
import json

def main():
    # URL del endpoint para llamar a la herramienta
    url = "http://localhost:8000/tools/create_client"
    
    # Datos para crear el nuevo cliente
    data = {
        "name": "Diana",
        "city": "Sevilla",
        "email": "diana@example.com"
    }
    
    # Hacemos la petición POST
    print(f"Creando nuevo cliente con datos: {data}")
    response = requests.post(url, json=data)
    
    # Mostramos la respuesta
    print(f"Código de respuesta: {response.status_code}")
    try:
        response_data = response.json()
        print(f"Respuesta: {json.dumps(response_data, indent=2)}")
    except Exception as e:
        print(f"Error al procesar la respuesta: {str(e)}")
        print(f"Contenido de la respuesta: {response.text}")

if __name__ == "__main__":
    main() 