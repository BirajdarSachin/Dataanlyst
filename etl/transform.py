import pandas as pd
from etl.logger import get_logger
logger = get_logger()


def clean_data(df):
    """
    Clean the extracted data by handling missing values and ensuring correct data types.

    Parameters:
    df (pd.DataFrame): The DataFrame to be cleaned.

    Returns:
    pd.DataFrame: A cleaned DataFrame.
    Note: The cleaning steps are examples and should be adjusted based on the actual data and requirements.
    """
    try:
        # Example cleaning steps (these can be modified based on actual data)
        df = df.drop(columns=["Unnamed: 0"], errors='ignore') # Remove unnecessary columns if they exist
        logger.info("Removed unnecessary columns if they existed.")

        df = df.drop_duplicates() # Remove rows with  duplicates values
        logger.info(" Duplicates handled by dropping rows.")
        
        df.columns = df.columns.str.lower().str.strip() # Standardize column names
        logger.info("Standardized column names to lowercase and stripped whitespace.")
        
        df["date"] = pd.to_datetime(df["date"]) # Convert 'date' column to datetime format
        logger.info("Converted 'date' column to datetime.")
        
        logger.info("Data cleaning completed successfully.")
        return df
    
    except Exception as e:
        logger.error(f"An error occurred during data cleaning: {e}")
        return None


def create_dim_tables(df):
    try:
        # Corrected: Apply .unique() to the Series before creating DataFrame
        dim_team =pd.DataFrame({"team_name": pd.concat([
        df["batting_team"], df["bowling_team"], df["toss_winner"]
        ]).dropna().unique()})
        dim_team["team_id"] = range(1, len(dim_team)+1) # Add this line to create 'team_id'
        logger.info("Dimension table for teams created successfully.")

        dim_player = pd.DataFrame({"player_name": pd.concat([
            df["batter"], df["bowler"], df["non_striker"], df["player_of_match"], df["player_out"]
        ]).dropna().unique()})
        dim_player["player_id"] = range(1, len(dim_player)+1)
        logger.info("Dimension table for players created successfully.")


        dim_venue = df[["venue", "city"]].drop_duplicates()
        dim_venue["venue_id"] = range(1, len(dim_venue)+1)
        logger.info("Dimension table for venues created successfully.")

        dim_date = df[["date", "day", "month", "year", "season"]].drop_duplicates()
        dim_date["date_id"] = range(1, len(dim_date)+1)
        logger.info("Dimension table for dates created successfully.")
        logger.info("Dimension tables created successfully.")

        return dim_team, dim_player, dim_venue, dim_date

    except Exception as e:
        logger.error(f"An error occurred while creating dimension tables: {e}")
        return None, None, None, None
    

    

def create_fact_tables(df, dim_team, dim_player, dim_venue, dim_date):
    try:
        logger.info("Creating mapping dictionaries for dimension tables.")
        team_map = dict(zip(dim_team.team_name, dim_team.team_id))
        player_map = dict(zip(dim_player.player_name, dim_player.player_id))
        venue_map = dict(zip(dim_venue.venue, dim_venue.venue_id))
        date_map = dict(zip(dim_date.date, dim_date.date_id))

        logger.info("Mapping dictionaries for dimension tables created successfully.")

        # FACT DELIVERIES
        fact_deliveries = df.copy()

        fact_deliveries["batting_team_id"] = fact_deliveries["batting_team"].map(team_map)
        fact_deliveries["bowling_team_id"] = fact_deliveries["bowling_team"].map(team_map)
        logger.info("Mapped team names to team IDs in fact deliveries.")
        fact_deliveries["striker_id"] = fact_deliveries["batter"].map(player_map)
        fact_deliveries["bowler_id"] = fact_deliveries["bowler"].map(player_map)
        fact_deliveries["non_striker_id"] = fact_deliveries["non_striker"].map(player_map)
        logger.info("Mapped player names to player IDs in fact deliveries.")

        fact_deliveries["venue_id"] = fact_deliveries["venue"].map(venue_map)
        fact_deliveries["date_id"] = fact_deliveries["date"].map(date_map)
        logger.info("Mapped venue names to venue IDs and dates to date IDs in fact deliveries.")

        fact_deliveries["is_wicket"] = fact_deliveries["wicket_kind"].notnull().astype(int)
        logger.info("Fact deliveries table created successfully.")

        # FACT MATCHES
        fact_matches = df.groupby("match_id").agg({
            "date": "first",
            "venue": "first",
            "toss_winner": "first",
            "match_won_by": "first",
            "team_runs": "max",
            "team_wicket": "max"
        }).reset_index()

        logger.info("Aggregated match-level data for fact matches.")

        fact_matches["date_id"] = fact_matches["date"].map(date_map)
        fact_matches["venue_id"] = fact_matches["venue"].map(venue_map)
        fact_matches["toss_winner_id"] = fact_matches["toss_winner"].map(team_map)
        fact_matches["winner_team_id"] = fact_matches["match_won_by"].map(team_map)

        logger.info("Fact tables created successfully.")

        return fact_deliveries, fact_matches  
        
    except Exception as e:
        logger.error(f"An error occurred while creating fact tables: {e}")
        return None, None