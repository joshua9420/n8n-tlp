"""
Database connection and query utilities for PostgreSQL
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import sys
import os
import time
from typing import List, Dict, Any, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings


@contextmanager
def get_connection(max_retries=3, retry_delay=2):
    """
    Context manager for PostgreSQL database connections.
    Automatically handles connection cleanup and retries.
    
    Args:
        max_retries: Maximum number of connection attempts
        retry_delay: Seconds to wait between retries
    
    Usage:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM table")
    """
    conn = None
    last_error = None
    
    for attempt in range(max_retries):
        try:
            # Debug info (will appear in container logs)
            if attempt > 0:
                print(f"[DB] Retry attempt {attempt + 1}/{max_retries}")
            
            conn = psycopg2.connect(
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                database=settings.POSTGRES_DB,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                connect_timeout=10
            )
            yield conn
            conn.commit()
            return
        except psycopg2.OperationalError as e:
            last_error = e
            if conn:
                try:
                    conn.rollback()
                    conn.close()
                except:
                    pass
            
            if attempt < max_retries - 1:
                print(f"[DB] Connection failed: {str(e)}. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                # Last attempt failed
                error_msg = f"Database connection failed after {max_retries} attempts: {str(e)}"
                print(f"[DB] {error_msg}")
                raise Exception(error_msg)
        except psycopg2.Error as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise Exception(f"Database error: {str(e)}")
        finally:
            if conn and attempt == max_retries - 1:
                try:
                    conn.close()
                except:
                    pass


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
        print(f"[DB] Testing connection to {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                print("[DB] Connection test successful!")
                return True
    except Exception as e:
        print(f"[DB] Connection test failed: {str(e)}")
        return False
