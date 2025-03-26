import psycopg2
import psycopg2.extras
from typing import Dict, Any, List

from gru.agents.tools.core.sql_runner.base import (
    BaseSQLRunner,
    DatabaseConnectionConfig,
    SQLExecutionResult
)


class PostgreSQLRunner(BaseSQLRunner):
    """PostgreSQL implementation of SQL runner"""
    
    def __init__(self, connection_config: DatabaseConnectionConfig):
        """
        Initialize PostgreSQL runner
        
        Args:
            connection_config: PostgreSQL connection configuration
        """
        self.config = connection_config
        self.connection = None
        self.cursor = None
        self.keep_alive = connection_config.keep_alive
        
        self.connect()
    
    def connect(self) -> None:
        """Establish connection to the PostgreSQL database."""
        try:
            if self.connection is None or self._is_connection_closed():
                conn_params = self._get_enhanced_connection_params()
                self.connection = psycopg2.connect(**conn_params)
                self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except Exception as e:
            raise e
    
    def close(self) -> None:
        """Close connection to the PostgreSQL database."""
        if not self.keep_alive:
            self._close_resources()
    
    def is_connection_closed(self) -> bool:
        """Check if PostgreSQL connection is closed."""
        return self._is_connection_closed()
    
    def is_connection_alive(self) -> bool:
        """Check if the PostgreSQL connection is still alive and not timed out."""
        if self.connection is None or self._is_connection_closed():
            return False
            
        return self._test_connection()
    
    def execute_query(self, query: str) -> SQLExecutionResult:
        """
        Execute a SQL query and return the results.
        
        Args:
            query: SQL query to execute
            
        Returns:
            SQLExecutionResult containing query results or error information
        """
        try:
            if not self.is_connection_alive():
                self.connect()
            
            self.cursor.execute(query)
            
            return self._handle_query_result(query)
                
        except Exception as e:
            return self._handle_execution_error(e)
        finally:
            if not self.keep_alive:
                self.close()
    
    def fetch_results(self) -> List[Dict[str, Any]]:
        """Fetch and format query results from PostgreSQL."""
        results = self.cursor.fetchall()
        return [dict(row) for row in results]
    
    def commit(self) -> None:
        """Commit the PostgreSQL transaction."""
        self.connection.commit()
    
    def rollback(self) -> None:
        """Rollback the PostgreSQL transaction."""
        self.connection.rollback()
        
    def __del__(self):
        """Destructor to ensure connection is closed when object is garbage collected."""
        try:
            self.close()
        except:
            pass
    
    def _is_connection_closed(self) -> bool:
        """Check if the database connection is closed."""
        return self.connection.closed if self.connection else True
    
    def _get_enhanced_connection_params(self) -> Dict[str, Any]:
        """
        Get connection parameters with keepalive settings.
        This uses PostgreSQL's built-in keepalive mechanism instead of 
        custom timeout tracking.
        """
        base_params = self.config.get_connection_params()
        
        keepalive_params = {
            "keepalives": 1,
            "keepalives_idle": 30,   
            "keepalives_interval": 10,
            "keepalives_count": 5
        }
        
        return {**base_params, **keepalive_params}
    
    def _test_connection(self) -> bool:
        """Test if the connection is still valid by executing a simple query."""
        try:
            test_cursor = self.connection.cursor()
            test_cursor.execute("SELECT 1")
            test_cursor.close()
            return True
        except Exception:
            self._close_resources()
            return False
    
    def _close_resources(self) -> None:
        """Close database cursor and connection resources."""
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def _handle_query_result(self, query: str) -> SQLExecutionResult:
        """Process the query result based on query type."""
        if query.strip().upper().startswith("SELECT"):
            results = self.fetch_results()
            return SQLExecutionResult(
                success=True,
                data=results
            )
        else:
            self.commit()
            return SQLExecutionResult(
                success=True,
                message="Query executed successfully",
                rows_affected=self.cursor.rowcount
            )
    
    def _handle_execution_error(self, error: Exception) -> SQLExecutionResult:
        """Handle exceptions that occur during query execution."""
        if self.connection:
            self.rollback()

        if "connection" in str(error).lower() or "terminated" in str(error).lower():
            self._close_resources()
            
        return SQLExecutionResult(
            success=False,
            error=str(error)
        )