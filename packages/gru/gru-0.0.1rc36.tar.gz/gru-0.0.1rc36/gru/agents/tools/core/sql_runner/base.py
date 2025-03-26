from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_serializer
from datetime import date, datetime, time, timedelta
import json


class DatabaseConnectionConfig(BaseModel):
    """Base configuration for database connections"""

    db_host: str
    db_port: int
    db_username: str
    db_password: str
    db_name: str
    keep_alive: bool = True
    connection_timeout: int = 3600

    class Config:
        extra = "allow"

    def get_connection_params(self) -> Dict[str, Any]:
        """
        Get connection parameters in a format suitable for database connectors.
        Can be overridden by subclasses to customize parameter mapping.

        Returns:
            Dictionary of connection parameters
        """
        params = self.model_dump()
        return {
            "host": params["db_host"],
            "port": params["db_port"],
            "user": params["db_username"],
            "password": params["db_password"],
            "dbname": params["db_name"],
        }


class SQLExecutionResult(BaseModel):
    """Model for SQL execution results"""

    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    message: Optional[str] = None
    error: Optional[str] = None
    rows_affected: Optional[int] = None

    @field_serializer("data")
    def serialize_data(self, data: Optional[List[Dict[str, Any]]]):
        """Custom serializer for data field to handle non-serializable objects"""
        if data is None:
            return None
        
        serialized_data = []
        for row in data:
            serialized_row = {}
            for k, v in row.items():
                if isinstance(v, (str, int, float, bool, type(None), list, dict)):
                    serialized_row[k] = v
                elif isinstance(v, (date, datetime, time)):
                    serialized_row[k] = v.isoformat()
                elif isinstance(v, timedelta):
                    serialized_row[k] = str(v)
                elif hasattr(v, '__json__') or hasattr(v, 'to_json'):
                    try:
                        if hasattr(v, '__json__'):
                            serialized_row[k] = v.__json__()
                        else:
                            serialized_row[k] = v.to_json()
                    except:
                        serialized_row[k] = str(v)
                else:
                    try:
                        json_str = json.dumps(v)
                        serialized_row[k] = v
                    except:
                        serialized_row[k] = str(v)
            
            serialized_data.append(serialized_row)
        
        return serialized_data


class SQLRunnerToolInput(BaseModel):
    """Input schema for SQL runner tools"""

    query: str = Field(description="SQL query to execute")


class BaseSQLRunner(ABC):
    """
    Abstract base class for SQL query runners.
    Defines the interface for SQL runners without implementation details.
    """

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the database."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close connection to the database."""
        pass

    @abstractmethod
    def is_connection_alive(self) -> bool:
        """Check if the database connection is still alive."""
        pass

    @abstractmethod
    def execute_query(self, query: str) -> SQLExecutionResult:
        """
        Execute a SQL query and return the results.

        Args:
            query: SQL query to execute

        Returns:
            SQLExecutionResult containing query results or error information
        """
        pass