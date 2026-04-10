from etl.extract import extract_data as extract
from etl.transform import clean_data , create_dim_tables, create_fact_tables
from etl.load import Load
from etl.validation import validate
from etl.logger import get_logger
from config.db_config import PYODBC_CONN_STR_WINDOWS  
logger = get_logger()
def run():
    try:
        logger.info("Starting ETL...")
        df = extract("data/IPL.csv")
        df = clean_data(df)
        print(df.shape)
        validate(df)
        dim_team, dim_player, dim_venue, dim_date,dim_umpires, dim_wickets,dim_stage ,dim_seasons = create_dim_tables(df)

        fact_deliveries, fact_matches, fact_batting, fact_bowling = create_fact_tables(df, dim_team, dim_player, dim_venue, dim_date,dim_umpires,dim_wickets, dim_stage, dim_seasons)

        with Load(connection_string=PYODBC_CONN_STR_WINDOWS ) as loader:
            loader.load_dimension_tables(dim_team, dim_player, dim_venue, dim_date, dim_umpires, dim_wickets, dim_stage,dim_seasons)
            loader.load_fact_tables(fact_deliveries, fact_matches, fact_batting, fact_bowling)

        logger.info("ETL completed successfully.")
    except Exception as e:
        logger.error(f"ETL failed: {e}")


if __name__ == "__main__":
    run()