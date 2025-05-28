import asyncio
import json
import sys

async def main():
    try:
        # Importamos las herramientas directamente del módulo
        from backend.api.v1.tools.client_tools import (
            list_clients, 
            get_client, 
            create_client_tool, 
            update_client_tool
        )
        
        # 1. Listar clientes actuales
        print("\n1. Listando clientes actuales:")
        result = await list_clients()
        if result["success"]:
            print_clients(result["clients"])
        else:
            print(f"Error: {result.get('error')}")
            
        # 2. Crear un nuevo cliente
        print("\n2. Creando un nuevo cliente:")
        new_client_data = {
            "name": "Carlos",
            "city": "Barcelona",
            "email": "carlos@example.com"
        }
        result = await create_client_tool(**new_client_data)
        if result["success"]:
            print(f"Cliente creado con éxito: {result['client']['id']} - {result['client']['name']}")
        else:
            print(f"Error al crear cliente: {result.get('error')}")
            
        # 3. Listar clientes para ver el nuevo
        print("\n3. Listando clientes después de crear uno nuevo:")
        result = await list_clients()
        if result["success"]:
            print_clients(result["clients"])
        else:
            print(f"Error: {result.get('error')}")
            
        # 4. Obtener un cliente específico
        client_id = 1  # Suponemos que existe un cliente con ID 1
        print(f"\n4. Obteniendo cliente con ID {client_id}:")
        result = await get_client(client_id)
        if result["success"]:
            print_client(result["client"])
        else:
            print(f"Error: {result.get('error')}")
            
        # 5. Actualizar un cliente
        print("\n5. Actualizando cliente:")
        client_id = 2  # Suponemos que existe un cliente con ID 2
        update_data = {
            "city": "Valencia",  # Solo actualizamos la ciudad
        }
        result = await update_client_tool(client_id, **update_data)
        if result["success"]:
            print(f"Cliente actualizado con éxito:")
            print_client(result["client"])
        else:
            print(f"Error al actualizar cliente: {result.get('error')}")
            
        # 6. Listar clientes para ver los cambios
        print("\n6. Listando clientes después de actualizar:")
        result = await list_clients()
        if result["success"]:
            print_clients(result["clients"])
        else:
            print(f"Error: {result.get('error')}")
            
    except Exception as e:
        print(f"Error general: {str(e)}")

def print_clients(clients):
    if not clients:
        print("No hay clientes registrados.")
        return
        
    print("Clientes encontrados:")
    for client in clients:
        print_client(client)
        
def print_client(client):
    print(f"ID: {client['id']}, Nombre: {client['name']}, Ciudad: {client['city']}, Email: {client['email']}")

if __name__ == "__main__":
    asyncio.run(main()) 