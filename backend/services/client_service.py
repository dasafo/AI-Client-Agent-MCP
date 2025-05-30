# backend/services/client_service.py
from backend.core.database import database

# Servicios para la gestión de clientes
# Estas funciones implementan la lógica de negocio y el acceso a la base de datos para los clientes

async def get_all_clients(conn=None):
    """
    Obtiene todos los clientes ordenados por ID.
    
    Args:
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
        
    Returns:
        Lista de diccionarios con los datos de todos los clientes.
    """
    was_conn_provided = conn is not None
    pool = None
    try:
        if not was_conn_provided:
            # Si no se proporcionó una conexión, obtenemos una nueva del pool
            pool = await database.connect()
            conn = await pool.acquire()
        
        # Consulta todos los clientes ordenados por ID
        rows = await conn.fetch(
            "SELECT id, name, city, email, created_at FROM clients ORDER BY id"
        )
        return [dict(row) for row in rows]
    finally:
        # Solo liberamos la conexión si la creamos internamente
        if not was_conn_provided and conn:
            if pool:
                await pool.release(conn)

async def get_client_by_id(client_id, conn=None):
    """
    Obtiene un cliente específico por su ID.
    
    Args:
        client_id: ID del cliente a buscar.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
        
    Returns:
        Diccionario con los datos del cliente o None si no se encuentra.
    """
    was_conn_provided = conn is not None
    pool = None
    try:
        if not was_conn_provided:
            # Si no se proporcionó una conexión, obtenemos una nueva del pool
            pool = await database.connect()
            conn = await pool.acquire()

        # Consulta el cliente por ID
        row = await conn.fetchrow(
            "SELECT id, name, city, email, created_at FROM clients WHERE id = $1",
            client_id
        )
        return dict(row) if row else None
    finally:
        # Solo liberamos la conexión si la creamos internamente
        if not was_conn_provided and conn:
            if pool:
                await pool.release(conn)

async def create_client(name, city, email, conn=None):
    """
    Crea un nuevo cliente en la base de datos.
    
    Args:
        name: Nombre del cliente (obligatorio).
        city: Ciudad del cliente (opcional).
        email: Email del cliente (opcional).
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
        
    Returns:
        Diccionario con los datos del cliente creado.
    """
    was_conn_provided = conn is not None
    pool = None
    try:
        if not was_conn_provided:
            # Si no se proporcionó una conexión, obtenemos una nueva del pool
            pool = await database.connect()
            conn = await pool.acquire()

        # Inserta el nuevo cliente y devuelve sus datos
        row = await conn.fetchrow(
            """
            INSERT INTO clients (name, city, email) 
            VALUES ($1, $2, $3) 
            RETURNING id, name, city, email, created_at
            """,
            name, city, email
        )
        return dict(row)
    finally:
        # Solo liberamos la conexión si la creamos internamente
        if not was_conn_provided and conn:
            if pool:
                await pool.release(conn)

async def update_client(client_id, name=None, city=None, email=None, conn=None):
    """
    Actualiza los datos de un cliente existente.
    
    Args:
        client_id: ID del cliente a actualizar.
        name: Nuevo nombre del cliente (opcional).
        city: Nueva ciudad del cliente (opcional).
        email: Nuevo email del cliente (opcional).
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
        
    Returns:
        Diccionario con los datos actualizados del cliente o None si no se encuentra.
    """
    was_conn_provided = conn is not None
    pool = None
    acquired_conn_internally = False

    try:
        if not was_conn_provided:
            # Si no se proporcionó una conexión, obtenemos una nueva del pool
            pool = await database.connect()
            conn_for_read = await pool.acquire()
            acquired_conn_internally = True # Marcar que la conexión fue adquirida aquí
        else:
            conn_for_read = conn # Usar la conexión proporcionada para la lectura inicial

        # Primero obtenemos el cliente actual para verificar que existe
        # y para mantener los campos no actualizados
        client = await get_client_by_id(client_id, conn=conn_for_read) 
        if not client:
            return None
        
        # Si adquirimos la conexión internamente para la lectura, la liberamos antes de la escritura si no es la misma que usaremos para escribir.
        # Sin embargo, es más simple usar la misma conexión si la obtuvimos del pool.
        if acquired_conn_internally and conn_for_read != conn: # Este caso es complejo y mejor evitarlo
             # Si la conexión para leer fue interna y diferente a la provista (conn), liberar la interna.
             # Esto solo sería relevante si conn_for_read es diferente de conn cuando conn es provisto.
             # Normalmente, si conn es provisto, conn_for_read será el mismo conn.
             # Si conn no es provisto, conn_for_read se adquiere del pool.
             # La lógica de liberación al final manejará la conexión adquirida internamente.
             pass # La conexión principal (conn) es la que se usa para la escritura.

        # Actualizamos solo los campos proporcionados, manteniendo los valores existentes para los no proporcionados
        updated_name = name if name is not None else client['name']
        updated_city = city if city is not None else client['city']
        updated_email = email if email is not None else client['email']
        
        # Usamos la conexión 'conn' (ya sea la provista o la adquirida del pool) para la escritura
        # Si no se proveyó conn y no se adquirió antes (lo cual no debería pasar por la lógica de arriba), se adquiere ahora.
        # Pero la lógica actual ya define 'conn' si no fue provista.
        if not conn: # Esto es una doble verificación, conn ya debería estar definido si no se proveyó.
            if not pool: pool = await database.connect()
            conn = await pool.acquire()
            was_conn_provided = False # Se marca que fue adquirida internamente
            acquired_conn_internally = True # Aunque ya debería estar marcado.

        # Ejecuta la actualización del cliente
        row = await conn.fetchrow(
            """
            UPDATE clients 
            SET name = $1, city = $2, email = $3 
            WHERE id = $4
            RETURNING id, name, city, email, created_at
            """,
            updated_name, updated_city, updated_email, client_id
        )
        return dict(row) if row else None
    finally:
        # Solo liberamos la conexión si la creamos internamente
        if acquired_conn_internally and conn: # Si la conexión principal fue adquirida internamente
            if pool:
                await pool.release(conn)
        # Si se proporcionó conn externamente (was_conn_provided = True), no se libera aquí.

async def delete_client(client_id, conn=None):
    """
    Elimina un cliente de la base de datos.
    
    Args:
        client_id: ID del cliente a eliminar.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
        
    Returns:
        Boolean indicando si la eliminación fue exitosa.
    """
    was_conn_provided = conn is not None
    pool = None
    acquired_conn_internally = False

    try:
        if not was_conn_provided:
            # Si no se proporcionó una conexión, obtenemos una nueva del pool
            pool = await database.connect()
            conn_for_read_and_delete = await pool.acquire()
            acquired_conn_internally = True
        else:
            conn_for_read_and_delete = conn

        # Primero verificamos que el cliente existe
        client = await get_client_by_id(client_id, conn=conn_for_read_and_delete)
        if not client:
            return False # El cliente no existe, no se puede eliminar
        
        # Eliminamos el cliente usando la misma conexión
        result = await conn_for_read_and_delete.execute(
            "DELETE FROM clients WHERE id = $1",
            client_id
        )
        return result == "DELETE 1" # Retorna True si se eliminó exactamente un registro
    finally:
        # Solo liberamos la conexión si la creamos internamente
        if acquired_conn_internally and conn_for_read_and_delete:
            if pool:
                await pool.release(conn_for_read_and_delete)
        # Si se proporcionó conn externamente, no se libera aquí.
