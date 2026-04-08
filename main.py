from etl.extract import extract_data as extract
from etl.transform import clean_data , create_dim_tables, create_fact_tables
#from etl.load import load
from etl.validation import validate
from etl.logger import get_logger
logger = get_logger()
def run():
    logger.info("Starting ETL...")

    df = extract("data/IPL.csv")
    df = clean_data(df)
    print(df.shape)
    # validate(df)
    # dim_team, dim_player, dim_venue, dim_date = create_dim_tables(df)

    # fact_deliveries, fact_matches = create_fact_tables(df, dim_team, dim_player, dim_venue, dim_date)


    logger.info("ETL completed successfully.")


if __name__ == "__main__":
    run()