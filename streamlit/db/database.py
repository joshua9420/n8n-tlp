"""
Database connection and query utilities for PostgreSQL
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import sys
import os
from typing import List, Dict, Any, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings


@contextmanager
def get_connection():
    """
    Context manager for PostgreSQL database connections.
    Automatically handles connection cleanup.
    
    Usage:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM table")
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD
        )
        yield conn
        conn.commit()
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        raise Exception(f"Database error: {str(e)}")
    finally:
        if conn:
            conn.close()


def execute_query(query: str, params: Optional[tuple] = None) -> None:
    """
    Execute a query without returning results (INSERT, UPDATE, DELETE).
    
    Args:
        query: SQL query string
        params: Optional tuple of parameters for parameterized queries
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)


def fetch_data(query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """
    Execute a SELECT query and return results as list of dictionaries.
    
    Args:
        query: SQL query string
        params: Optional tuple of parameters for parameterized queries
        
    Returns:
        List of dictionaries where keys are column names
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            results = cur.fetchall()
            # Convert RealDictRow objects to regular dicts
            return [dict(row) for row in results]


def fetch_one(query: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
    """
    Execute a SELECT query and return a single row as a dictionary.
    
    Args:
        query: SQL query string
        params: Optional tuple of parameters for parameterized queries
        
    Returns:
        Dictionary with column names as keys, or None if no results
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            result = cur.fetchone()
            return dict(result) if result else None


def test_connection() -> bool:
    """
    Test database connection.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                return True
    except Exception as e:
        print(f"Connection test failed: {str(e)}")
        return False
