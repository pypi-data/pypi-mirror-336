import json
from typing import Optional
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from gru.agents.tools.core.sql_runner import (
    SQLRunnerToolInput,
    SQLExecutionResult,
    DatabaseConnectionConfig,
    get_sql_runner,
)


class SQLNativeRunnerTool(BaseTool):
    """
    A direct implementation of the SQL Runner Tool that executes queries natively
    without submitting to the task server. Supports PostgreSQL by default.
    """

    name: str = "run_sql_query"
    description: str = "Used to run SQL queries on the database"
    args_schema: type[BaseModel] = SQLRunnerToolInput
    return_direct: bool = True

    db_type: str = Field(default="postgresql", description="Database type")
    db_host: str = Field(description="Database host")
    db_port: int = Field(description="Database port")
    db_username: str = Field(description="Database username")
    db_password: str = Field(description="Database password")
    db_name: str = Field(description="Database name")
    keep_alive: bool = Field(
        default=True, description="Keep connection alive between queries"
    )
    connection_timeout: int = Field(
        default=3600, description="Connection timeout in seconds (used by some DB types)"
    )

    def __init__(
        self,
        db_host: str,
        db_port: int,
        db_username: str,
        db_password: str,
        db_name: str,
        db_type: str = "postgresql",
        keep_alive: bool = True,
        connection_timeout: int = 3600,
        **kwargs,
    ):
        """
        Initialize SQL Native Runner Tool.

        Args:
            db_host: Database host
            db_port: Database port
            db_username: Database username
            db_password: Database password
            db_name: Database name
            db_type: Database type
            keep_alive: Keep connection alive between queries
            connection_timeout: Connection timeout in seconds (used by some DB types)
        """
        super().__init__(
            db_host=db_host,
            db_port=db_port,
            db_username=db_username,
            db_password=db_password,
            db_name=db_name,
            db_type=db_type,
            keep_alive=keep_alive,
            connection_timeout=connection_timeout,
            **kwargs,
        )

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """
        Execute the SQL query directly and return the results.

        Args:
            query: SQL query to execute
            run_manager: Optional callback manager for the tool run

        Returns:
            Query results as a JSON string
        """
        try:
            connection_config = DatabaseConnectionConfig(
                db_host=self.db_host,
                db_port=self.db_port,
                db_username=self.db_username,
                db_password=self.db_password,
                db_name=self.db_name,
                keep_alive=self.keep_alive,
                connection_timeout=self.connection_timeout,
            )

            runner = get_sql_runner(self.db_type, connection_config)

            result = runner.execute_query(query)

            if isinstance(result, SQLExecutionResult):
                return json.dumps(result.model_dump(), default=str)
            else:
                return json.dumps({"results": result}, default=str)

        except Exception as e:
            error_result = {
                "success": False,
                "error": f"Error executing SQL query: {str(e)}",
            }
            return json.dumps(error_result)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """
        Asynchronous version of _run.
        """
        return self._run(query, run_manager)