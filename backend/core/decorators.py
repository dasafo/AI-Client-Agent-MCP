"""
Database decorators for service functions.

This module provides decorators to simplify database connection handling in service functions.
"""

import functools
from backend.core.logging import get_logger
from typing import Callable, Optional, Any, TypeVar
import asyncpg
from backend.core.database import database

logger = get_logger(__name__)

# Type variables for better type hints
T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])

def with_db_connection(func: F) -> F:
    """
    Decorator that automatically handles database connection acquisition and release.
    
    If a connection is provided as a parameter (conn), it uses that connection.
    If no connection is provided, it creates a new one and releases it after execution.
    
    Args:
        func: The async function to decorate
        
    Returns:
        The decorated function
        
    Example:
        @with_db_connection
        async def get_user(user_id, conn=None):
            # No need to acquire or release connection manually
            return await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Check if a connection was provided
        conn_provided = 'conn' in kwargs and kwargs['conn'] is not None
        conn = kwargs.get('conn')
        
        if not conn_provided:
            # If no connection provided, create a new one
            try:
                # Use the database utility to get a connection
                async with database.connection() as new_conn:
                    # Update kwargs with the new connection
                    kwargs['conn'] = new_conn
                    # Call the wrapped function with the new connection
                    return await func(*args, **kwargs)
            except asyncpg.PostgresError as e:
                logger.error(f"PostgreSQL error in {func.__name__}: {e}", exc_info=True)
                raise
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
                raise
        else:
            # If a connection was provided, just use it
            try:
                return await func(*args, **kwargs)
            except asyncpg.PostgresError as e:
                logger.error(f"PostgreSQL error in {func.__name__}: {e}", exc_info=True)
                raise
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
                raise
    
    return wrapper


def db_transaction(func: F) -> F:
    """
    Decorator that wraps a function in a database transaction.
    
    If a connection is provided, it starts a transaction on that connection.
    If no connection is provided, it creates a new connection and transaction.
    
    Args:
        func: The async function to decorate
        
    Returns:
        The decorated function
        
    Example:
        @db_transaction
        async def transfer_funds(from_account, to_account, amount, conn=None):
            # This will be executed in a transaction
            await conn.execute("UPDATE accounts SET balance = balance - $1 WHERE id = $2", amount, from_account)
            await conn.execute("UPDATE accounts SET balance = balance + $1 WHERE id = $2", amount, to_account)
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Check if a connection was provided
        conn_provided = 'conn' in kwargs and kwargs['conn'] is not None
        conn = kwargs.get('conn')
        
        if not conn_provided:
            # If no connection provided, create a new one
            try:
                pool = await database.connect()
                conn = await pool.acquire()
                
                # Start a transaction
                async with conn.transaction():
                    kwargs['conn'] = conn
                    result = await func(*args, **kwargs)
                
                return result
            except asyncpg.PostgresError as e:
                logger.error(f"PostgreSQL transaction error in {func.__name__}: {e}", exc_info=True)
                raise
            except Exception as e:
                logger.error(f"Unexpected transaction error in {func.__name__}: {e}", exc_info=True)
                raise
            finally:
                # Release the connection
                if conn and pool:
                    await pool.release(conn)
        else:
            # If a connection was provided, start a transaction on it
            async with conn.transaction():
                try:
                    return await func(*args, **kwargs)
                except asyncpg.PostgresError as e:
                    logger.error(f"PostgreSQL transaction error in {func.__name__}: {e}", exc_info=True)
                    raise
                except Exception as e:
                    logger.error(f"Unexpected transaction error in {func.__name__}: {e}", exc_info=True)
                    raise
    
    return wrapper 