import pyodbc
import pandas as pd
from sqlalchemy import create_engine, text
from etl.logger import get_logger

logger = get_logger()
class Load:
    """
    Load class for handling data loading operations to SQL Server database.
    """

    def __init__(self, connection_string=None, engine_url=None):
        """
        Initialize the Load class with database connection details.

        Parameters:
        connection_string (str): PyODBC connection string for SQL Server
        engine_url (str): SQLAlchemy engine URL (alternative to connection_string)
        """
        self.connection_string = connection_string
        self.engine_url = engine_url
        self.engine = None
        self.conn = None
        self.cursor = None

        if engine_url:
            self.engine = create_engine(engine_url)
            logger.info("SQLAlchemy engine created successfully.")
        elif connection_string:
            logger.info("Using PyODBC connection string.")

    def connect(self):
        """
        Establish database connection.
        """
        try:
            if self.engine:
                self.conn = self.engine.connect()
                logger.info("Database connection established using SQLAlchemy.")
            else:
                self.conn = pyodbc.connect(self.connection_string)
                self.cursor = self.conn.cursor()
                logger.info("Database connection established using PyODBC.")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def disconnect(self):
        """
        Close database connection.
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            logger.info("Database connection closed successfully.")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")

    def create_table_if_not_exists(self, table_name, df):
        """
        Create table if it doesn't exist based on DataFrame columns.

        Parameters:
        table_name (str): Name of the table to create
        df (pd.DataFrame): DataFrame to infer schema from
        """
        try:
            # Infer column types from DataFrame
            columns = []
            for col in df.columns:
                dtype = df[col].dtype
                if dtype == 'int64':
                    sql_type = 'INT'
                elif dtype == 'float64':
                    sql_type = 'FLOAT'
                elif dtype == 'bool':
                    sql_type = 'BIT'
                elif 'datetime' in str(dtype):
                    sql_type = 'DATETIME'
                else:
                    # Check if column contains dates
                    if col.lower() in ['date', 'created_at', 'updated_at']:
                        sql_type = 'DATETIME'
                    else:
                        sql_type = 'VARCHAR(255)'

                columns.append(f"[{col}] {sql_type}")

            columns_str = ", ".join(columns)
            create_query = f"""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')
            CREATE TABLE {table_name} ({columns_str})
            """

            if self.engine:
                with self.engine.connect() as conn:
                    conn.execute(text(create_query))
                    conn.commit()
            else:
                self.cursor.execute(create_query)
                self.conn.commit()

            logger.info(f"Table '{table_name}' created or already exists.")

        except Exception as e:
            logger.error(f"Error creating table '{table_name}': {e}")
            raise

    def load_dataframe(self, df, table_name, if_exists='append'):
        """
        Load DataFrame to database table.

        Parameters:
        df (pd.DataFrame): DataFrame to load
        table_name (str): Target table name
        if_exists (str): What to do if table exists ('append', 'replace', 'fail')
        """
        try:
            if self.engine:
                df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
                logger.info(f"Data loaded successfully to table '{table_name}' using SQLAlchemy.")
            else:
                # Create table if not exists
                self.create_table_if_not_exists(table_name, df)

                # Insert data
                for index, row in df.iterrows():
                    placeholders = ", ".join(["?" for _ in row])
                    columns = ", ".join([f"[{col}]" for col in df.columns])
                    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

                    # Convert row to list and handle None values
                    values = [None if pd.isna(val) else val for val in row]
                    self.cursor.execute(insert_query, values)

                self.conn.commit()
                logger.info(f"Data loaded successfully to table '{table_name}' using PyODBC.")

        except Exception as e:
            logger.error(f"Error loading data to table '{table_name}': {e}")
            raise

    def load_dimension_tables(self, dim_team, dim_player, dim_venue, dim_date, dim_umpires, dim_wickets):
        """
        Load all dimension tables to database.

        Parameters:
        dim_team, dim_player, dim_venue, dim_date, dim_umpires, dim_wickets: DataFrames for dimension tables
        """
        try:
            logger.info("Starting to load dimension tables...")

            self.load_dataframe(dim_team, 'dim_team', if_exists='replace')
            self.load_dataframe(dim_player, 'dim_player', if_exists='replace')
            self.load_dataframe(dim_venue, 'dim_venue', if_exists='replace')
            self.load_dataframe(dim_date, 'dim_date', if_exists='replace')
            self.load_dataframe(dim_umpires, 'dim_umpires', if_exists='replace')
            self.load_dataframe(dim_wickets, 'dim_wickets', if_exists='replace')

            logger.info("All dimension tables loaded successfully.")

        except Exception as e:
            logger.error(f"Error loading dimension tables: {e}")
            raise

    def load_fact_tables(self, fact_deliveries, fact_matches):
        """
        Load all fact tables to database.

        Parameters:
        fact_deliveries, fact_matches: DataFrames for fact tables
        """
        try:
            logger.info("Starting to load fact tables...")

            self.load_dataframe(fact_deliveries, 'fact_deliveries', if_exists='replace')
            self.load_dataframe(fact_matches, 'fact_matches', if_exists='replace')

            logger.info("All fact tables loaded successfully.")

        except Exception as e:
            logger.error(f"Error loading fact tables: {e}")
            raise

    def execute_query(self, query):
        """
        Execute a custom SQL query.

        Parameters:
        query (str): SQL query to execute
        """
        try:
            if self.engine:
                with self.engine.connect() as conn:
                    result = conn.execute(text(query))
                    conn.commit()
                    logger.info("Query executed successfully.")
                    return result
            else:
                self.cursor.execute(query)
                self.conn.commit()
                logger.info("Query executed successfully.")
                return self.cursor

        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise

    def get_table_count(self, table_name):
        """
        Get row count of a table.

        Parameters:
        table_name (str): Name of the table

        Returns:
        int: Row count
        """
        try:
            query = f"SELECT COUNT(*) FROM {table_name}"
            if self.engine:
                with self.engine.connect() as conn:
                    result = conn.execute(text(query))
                    count = result.fetchone()[0]
            else:
                self.cursor.execute(query)
                count = self.cursor.fetchone()[0]

            logger.info(f"Table '{table_name}' has {count} rows.")
            return count

        except Exception as e:
            logger.error(f"Error getting count for table '{table_name}': {e}")
            return 0

    def __enter__(self):
        """
        Context manager entry.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit.
        """
        self.disconnect()