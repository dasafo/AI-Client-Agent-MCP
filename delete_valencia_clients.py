import asyncio
from backend.services.client_service import get_all_clients, delete_client

async def main():
    # Listar clientes antes de eliminar
    print("\nClientes antes de eliminar:")
    clients = await get_all_clients()
    for client in clients:
        print(f"ID: {client['id']}, Nombre: {client['name']}, Ciudad: {client['city']}, Email: {client['email']}")
    
    # Filtrar clientes de Valencia
    valencia_clients = [client for client in clients if client['city'] == 'Valencia']
    
    if not valencia_clients:
        print("\nNo hay clientes de Valencia para eliminar.")
        return
    
    print(f"\nSe encontraron {len(valencia_clients)} clientes de Valencia para eliminar:")
    for client in valencia_clients:
        print(f"ID: {client['id']}, Nombre: {client['name']}, Email: {client['email']}")
    
    # Eliminar clientes de Valencia
    deleted_count = 0
    for client in valencia_clients:
        print(f"\nEliminando cliente con ID {client['id']} ({client['name']})...")
        result = await delete_client(client['id'])
        if result:
            print(f"Cliente {client['name']} eliminado correctamente.")
            deleted_count += 1
        else:
            print(f"No se pudo eliminar el cliente {client['name']}.")
    
    print(f"\nSe eliminaron {deleted_count} de {len(valencia_clients)} clientes de Valencia.")
    
    # Listar clientes después de eliminar
    print("\nClientes después de eliminar:")
    remaining_clients = await get_all_clients()
    for client in remaining_clients:
        print(f"ID: {client['id']}, Nombre: {client['name']}, Ciudad: {client['city']}, Email: {client['email']}")

if __name__ == "__main__":
    asyncio.run(main()) 