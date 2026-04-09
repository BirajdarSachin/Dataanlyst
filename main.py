from etl.extract import extract_data as extract
from etl.transform import clean_data , create_dim_tables, create_fact_tables
from etl.load import Load
from etl.validation import validate
from etl.logger import get_logger
import pyodbc
from sqlalchemy import create_engine
# from config.db_config import DB_CONFIG   
logger = get_logger()
def run():
    # try:
    logger.info("Starting ETL...")
    df = extract("data/IPL1.csv")
    df = extract("data/IPL.csv")
    df = clean_data(df)
    print(df.shape)
    validate(df)
    dim_team, dim_player, dim_venue, dim_date,dim_umpires, dim_wickets,dim_stage    = create_dim_tables(df)

    # fact_deliveries, fact_matches = create_fact_tables(df, dim_team, dim_player, dim_venue, dim_date,dim_umpires,dim_wickets)

        # Load data to database
        # Note: Update connection_string with your actual database connection
    connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=DESKTOP-AKHSPQL\\MS_SQL_2019;"
    "DATABASE=IPL_DW;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

    # conn=pyodbc.connect(connection_string)
    # print("Connection to database established successfully.", conn)

    
    # connection_string = DB_CONFIG[connection_string]

    with Load(connection_string=connection_string) as loader:
        loader.load_dimension_tables(dim_team, dim_player, dim_venue, dim_date, dim_umpires, dim_wickets)
        #     loader.load_fact_tables(fact_deliveries, fact_matches)

    logger.info("ETL completed successfully.")
    # except Exception as e:
        # logger.error(f"ETL failed: {e}")


if __name__ == "__main__":
    run()