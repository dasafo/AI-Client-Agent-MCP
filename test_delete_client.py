import asyncio
from backend.services.client_service import get_all_clients, delete_client, get_client_by_id

async def main():
    # Listar clientes antes de eliminar
    print("\nClientes antes de eliminar:")
    clients = await get_all_clients()
    for client in clients:
        print(f"ID: {client['id']}, Nombre: {client['name']}, Ciudad: {client['city']}, Email: {client['email']}")
    
    # ID del cliente a eliminar
    client_id = 5  # Miguel
    
    # Verificar que el cliente existe
    client = await get_client_by_id(client_id)
    if not client:
        print(f"\nEl cliente con ID {client_id} no existe.")
        return
    
    print(f"\nEliminando cliente con ID {client_id} ({client['name']})...")
    
    # Eliminar el cliente
    result = await delete_client(client_id)
    if result:
        print(f"\nCliente {client['name']} eliminado correctamente.")
    else:
        print(f"\nNo se pudo eliminar el cliente {client['name']}.")
    
    # Listar clientes después de eliminar
    print("\nClientes después de eliminar:")
    clients = await get_all_clients()
    for client in clients:
        print(f"ID: {client['id']}, Nombre: {client['name']}, Ciudad: {client['city']}, Email: {client['email']}")

if __name__ == "__main__":
    asyncio.run(main()) 