import psycopg2
import psycopg2.extras
from psycopg2 import sql

import logging

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

class PGSQL:
    """Start a database Connection"""

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.connection = psycopg2
        self.builder = psycopg2.sql
        try:
            self.connection = psycopg2.connect(
                host=kwargs['host'],
                port=kwargs['port'],
                database=kwargs['database'],
                user=kwargs['user'],
                password=kwargs['password']
            )
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.OperationalError) as psql_error:
            logger.info(f"Error while connecting to {kwargs['host']}")
            logger.fatal(psql_error)
            exit(99)

    def commit(self):
        self.connection.commit()

    def close(self, commit=False):
        if commit is True:
            self.commit()
        self.connection.close()

    def copy(self, table, columns, data):

        """
        Copy payload from buffer to a postgres table
        Parameters
        ----------
        table : str
            Target table.
        columns: str
            Columns to be copied.
        data: io.StringIO()
            payload buffer
        """

        statement = f"COPY {table}({columns}) FROM STDIN WITH (FORMAT CSV, FORCE_NULL({columns}), HEADER);"
        try:
            data.seek(0)
            self.cursor.copy_expert(statement, data)
            logger.info(f"Data copied successfully to {table}")
        except (Exception, psycopg2.Error) as sql_error:
            logger.error(sql_error)
            exit(99)

    def exec(self, statement):
        """
        Execute an SQL statement.
        Parameters
        ----------
        statement : str
            Statement to be executed on Postgres.
        """

        try:
            self.cursor.execute(statement)
            logger.info("Executed successfully")
        except (Exception, psycopg2.Error) as sql_error:
            logger.error(sql_error)
            exit(99)

    def merge(self, columns, target_table, source_table, merge_keys):
        on_conflict_statement = columns.split(',')
        
        query = f"""WITH data AS (SELECT {columns} FROM {source_table})
                    INSERT INTO {target_table} ({columns})
                    SELECT {columns} from data
                    ON CONFLICT ({merge_keys}) DO UPDATE SET
                    __elt_last_updated_at = CURRENT_TIMESTAMP,
             """

        for i in range(0, len(on_conflict_statement)):
            query += on_conflict_statement[i] + ' = EXCLUDED.' + on_conflict_statement[i] + ','
        query = query[:-1]

        self.exec(query)



