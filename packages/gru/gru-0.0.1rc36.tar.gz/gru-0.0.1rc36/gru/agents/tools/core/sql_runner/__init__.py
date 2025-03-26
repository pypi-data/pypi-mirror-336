from gru.agents.tools.core.sql_runner.base import DatabaseConnectionConfig, SQLRunnerToolInput, SQLExecutionResult, BaseSQLRunner
from gru.agents.tools.core.sql_runner.postgresql import PostgreSQLRunner


def get_sql_runner(db_type: str, connection_config: DatabaseConnectionConfig) -> BaseSQLRunner:
    """
    Factory function to get the appropriate SQL runner based on database type.
    
    Args:
        db_type: Database type (e.g., "postgresql")
        connection_config: DatabaseConnectionConfig instance with connection parameters
        
    Returns:
        An instance of the appropriate SQL runner
    """
    runners = {
        "postgresql": PostgreSQLRunner,
    }

    runner_class = runners.get(db_type.lower())
    if not runner_class:
        raise ValueError(f"Unsupported database type: {db_type}")

    return runner_class(connection_config)
