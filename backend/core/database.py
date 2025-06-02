# backend/core/database.py
import asyncpg
from backend.core.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DATABASE_URL
from backend.core.logging import get_logger
from contextlib import asynccontextmanager
from typing import Optional, Any

logger = get_logger(__name__)

class Database:
    """
    Database connection manager for PostgreSQL.
    Implements a singleton pattern for the connection pool.
    """
    def __init__(self):
        # Initialize connection pool as None
        self._pool = None
        self._connection_params = self._get_connection_params()

    def _get_connection_params(self) -> dict:
        """
        Get database connection parameters from environment variables.
        
        Returns:
            Dictionary with connection parameters or DSN string.
        """
        # If DATABASE_URL is provided, use it directly
        if DATABASE_URL:
            return {"dsn": DATABASE_URL}
        
        # Otherwise, construct from individual parameters
        if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
            logger.warning("Some database connection parameters are missing. Check your .env file.")
            
        return {
            "user": DB_USER,
            "password": DB_PASSWORD,
            "host": DB_HOST,
            "port": DB_PORT,
            "database": DB_NAME
        }

    async def connect(self):
        """
        Establishes a connection to the database if it doesn't exist.
        Creates a connection pool for efficient reuse.
        
        Returns:
            Database connection pool.
        """
        if not self._pool:
            try:
                # Create a new connection pool if it doesn't exist
                self._pool = await asyncpg.create_pool(
                    **self._connection_params,
                    min_size=1,
                    max_size=10
                )
                logger.info("Database connection pool created")
            except Exception as e:
                logger.error(f"Failed to create database connection pool: {e}")
                raise
        return self._pool

    async def disconnect(self):
        """
        Closes the database connection pool if active.
        """
        if self._pool:
            # Close all connections in the pool
            await self._pool.close()
            self._pool = None
            logger.info("Database connection pool closed")
    
    @asynccontextmanager
    async def connection(self):
        """
        Async context manager for database connections.
        Automatically acquires and releases connections from the pool.
        
        Usage:
            async with database.connection() as conn:
                result = await conn.fetch("SELECT * FROM table")
        
        Yields:
            Database connection from the pool.
        """
        pool = await self.connect()
        conn = None
        try:
            conn = await pool.acquire()
            yield conn
        finally:
            if conn:
                await pool.release(conn)

    async def execute(self, query: str, *args, **kwargs) -> str:
        """
        Executes a database query using a connection from the pool.
        
        Args:
            query: SQL query to execute
            *args, **kwargs: Parameters for the query
            
        Returns:
            Query result
        """
        async with self.connection() as conn:
            return await conn.execute(query, *args, **kwargs)
            
    async def fetch(self, query: str, *args, **kwargs) -> list:
        """
        Fetches multiple rows from the database.
        
        Args:
            query: SQL query to execute
            *args, **kwargs: Parameters for the query
            
        Returns:
            List of query results
        """
        async with self.connection() as conn:
            return await conn.fetch(query, *args, **kwargs)
            
    async def fetchrow(self, query: str, *args, **kwargs) -> Optional[dict]:
        """
        Fetches a single row from the database.
        
        Args:
            query: SQL query to execute
            *args, **kwargs: Parameters for the query
            
        Returns:
            Query result as a dictionary or None if no result
        """
        async with self.connection() as conn:
            row = await conn.fetchrow(query, *args, **kwargs)
            return dict(row) if row else None
            
    async def fetchval(self, query: str, *args, **kwargs) -> Any:
        """
        Fetches a single value from the database.
        
        Args:
            query: SQL query to execute
            *args, **kwargs: Parameters for the query
            
        Returns:
            Single value from query result
        """
        async with self.connection() as conn:
            return await conn.fetchval(query, *args, **kwargs)

# Singleton instance of Database class to be used throughout the application
database = Database()
