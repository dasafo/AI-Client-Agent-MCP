# backend/services/client_service.py
from backend.core.database import database


async def get_all_clients(conn=None):
    was_conn_provided = conn is not None
    pool = None
    try:
        if not was_conn_provided:
            pool = await database.connect()
            conn = await pool.acquire()
        
        rows = await conn.fetch(
            "SELECT id, name, city, email, created_at FROM clients ORDER BY id"
        )
        return [dict(row) for row in rows]
    finally:
        if not was_conn_provided and conn:
            if pool:
                await pool.release(conn)

async def get_client_by_id(client_id, conn=None):
    was_conn_provided = conn is not None
    pool = None
    try:
        if not was_conn_provided:
            pool = await database.connect()
            conn = await pool.acquire()

        row = await conn.fetchrow(
            "SELECT id, name, city, email, created_at FROM clients WHERE id = $1",
            client_id
        )
        return dict(row) if row else None
    finally:
        if not was_conn_provided and conn:
            if pool:
                await pool.release(conn)

async def create_client(name, city, email, conn=None):
    was_conn_provided = conn is not None
    pool = None
    try:
        if not was_conn_provided:
            pool = await database.connect()
            conn = await pool.acquire()

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
        if not was_conn_provided and conn:
            if pool:
                await pool.release(conn)

async def update_client(client_id, name=None, city=None, email=None, conn=None):
    was_conn_provided = conn is not None
    pool = None
    acquired_conn_internally = False

    try:
        if not was_conn_provided:
            pool = await database.connect()
            conn_for_read = await pool.acquire()
            acquired_conn_internally = True # Marcar que la conexión fue adquirida aquí
        else:
            conn_for_read = conn # Usar la conexión proporcionada para la lectura inicial

        # Primero obtenemos el cliente actual usando la conexión determinada (conn_for_read)
        # Nota: get_client_by_id también necesita ser refactorizado o llamado con la conexión correcta
        # Para este refactor, asumimos que get_client_by_id se llamará con la 'conn_for_read'
        # o que internamente se adaptará si es None.
        # Por simplicidad, si get_client_by_id es refactorizado, pasamos conn_for_read:
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

        # Actualizamos solo los campos proporcionados
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
        if acquired_conn_internally and conn: # Si la conexión principal fue adquirida internamente
            if pool:
                await pool.release(conn)
        # Si se proporcionó conn externamente (was_conn_provided = True), no se libera aquí.

async def delete_client(client_id, conn=None):
    was_conn_provided = conn is not None
    pool = None
    acquired_conn_internally = False

    try:
        if not was_conn_provided:
            pool = await database.connect()
            conn_for_read_and_delete = await pool.acquire()
            acquired_conn_internally = True
        else:
            conn_for_read_and_delete = conn

        # Primero verificamos que el cliente existe
        # Pasamos la conexión que estamos usando (sea provista o adquirida)
        client = await get_client_by_id(client_id, conn=conn_for_read_and_delete)
        if not client:
            return False # O podrías devolver un dict con success: False, message: "..."
        
        # Eliminamos el cliente usando la misma conexión
        result = await conn_for_read_and_delete.execute(
            "DELETE FROM clients WHERE id = $1",
            client_id
        )
        return result == "DELETE 1"
    finally:
        if acquired_conn_internally and conn_for_read_and_delete:
            if pool:
                await pool.release(conn_for_read_and_delete)
        # Si se proporcionó conn externamente, no se libera aquí.
