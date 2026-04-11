"""
Data transformation module for IPL Data Warehouse.

This module contains functions to clean, transform, and create dimension
and fact tables from the extracted IPL cricket data.
"""

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


        dim_venue_1 = df[["venue", "city"]].drop_duplicates()
        dim_venue = dim_venue_1['venue']+" - "+dim_venue_1['city']
        dim_venue = pd.DataFrame({"venue": dim_venue})
        dim_venue["venue_id"] = range(1, len(dim_venue)+1)
        logger.info("Dimension table for venues created successfully.")

        dim_umpires = pd.DataFrame({"umpire_name":df['umpire'].dropna().drop_duplicates().sort_values()})
        dim_umpires['umpire_id'] = range(1, len(dim_umpires) + 1)
        logger.info("Dimension table for umpires created successfully.")

        dim_wickets=pd.DataFrame({"wiket_type":df['wicket_kind'].dropna().drop_duplicates().sort_values()})
        dim_wickets['wicket_id'] = range(1, len(dim_wickets) + 1)
        logger.info("Dimension table for wickets created successfully.")

        dim_date = df[["date", "day", "month", "year", "season"]].drop_duplicates()
        dim_date["date_id"] = range(1, len(dim_date)+1)
        logger.info("Dimension table for dates created successfully.")

        dim_stage = pd.DataFrame({"stage":df['stage'].dropna().drop_duplicates().sort_values()})
        dim_stage['stage_id']=range(1, len(dim_stage) + 1)
        logger.info("Dimension table for stage created successfully.")

        dim_seasons = pd.DataFrame({"season_name":df['season'].astype(str).dropna().drop_duplicates().sort_values()})
        dim_seasons['season_id'] = range(1, len(dim_seasons) + 1)
        logger.info("Dimension table for seasons created successfully.")    

        logger.info("Dimension tables created successfully.")

        return dim_team, dim_player, dim_venue, dim_date, dim_umpires, dim_wickets,dim_stage, dim_seasons

    except Exception as e:
        logger.error(f"An error occurred while creating dimension tables: {e}")
        return None, None, None, None, None, None, None, None

    

def create_fact_tables(df, dim_team, dim_player, dim_venue, dim_date ,dim_umpires, dim_wickets, dim_stage, dim_seasons ):
    try:
        logger.info("Creating mapping dictionaries for dimension tables.")
        team_map = dict(zip(dim_team.team_name, dim_team.team_id))
        player_map = dict(zip(dim_player.player_name, dim_player.player_id))
        venue_map = dict(zip(dim_venue.venue, dim_venue.venue_id))
        date_map = dict(zip(dim_date.date, dim_date.date_id))
        stage_map = dict(zip(dim_stage.stage, dim_stage.stage_id))
        umpire_map = dict(zip(dim_umpires.umpire_name, dim_umpires.umpire_id))
        wicket_map = dict(zip(dim_wickets.wiket_type, dim_wickets.wicket_id))
        season_map = dict(zip(dim_seasons.season_name, dim_seasons.season_id))

         # frature engineering for fact tables
        df['is_four'] = (df['runs_total'] == 4) & (df['runs_extras'] == 0)
        df['is_six'] = (df['runs_total'] == 6) & (df['runs_extras'] == 0)
        df['is_boundary'] = df['is_four'] | df['is_six']
        df['is_dot'] = (df['runs_total'] == 0) & (df['valid_ball'] == 1)
        df['is_wicket'] = df['wicket_kind'].notna().astype(int)
        df["delivery_id"] = (
            df["match_id"].astype(str) + "_" +
            df["innings"].astype(str) + "_" +
            df["over"].astype(str) + "_" +
            df["ball"].astype(str)
        )
        # --fact_batters


        logger.info("Mapping dictionaries for dimension tables created successfully.")

        # FACT DELIVERIES
        fact_deliveries = df[[
            "delivery_id", "match_id", "innings", "over", "ball", "ball_no", "balls_per_over",
            "batting_team", "bowling_team", "batter", "non_striker", "bowler",
            "runs_batter", "runs_extras", "runs_total", "runs_not_boundary",
            "extra_type", "wicket_kind", "player_out", "fielders", "valid_ball",
            "runs_bowler", "bowler_wicket", "bat_pos", "balls_faced", "new_batter",
            "striker_out", "is_wicket", "stage", "season", "date", "venue",
            "toss_winner", "match_won_by", "player_of_match", "umpire"
        ]].copy()
        
        # Add engineered features
        fact_deliveries['is_four'] = df['is_four']
        fact_deliveries['is_six'] = df['is_six']
        fact_deliveries['is_boundary'] = df['is_boundary']
        fact_deliveries['is_dot'] = df['is_dot']
        
        # Map to dimension IDs
        fact_deliveries["batting_team_id"] = fact_deliveries["batting_team"].map(team_map)
        fact_deliveries["bowling_team_id"] = fact_deliveries["bowling_team"].map(team_map)
        fact_deliveries["batter_id"] = fact_deliveries["batter"].map(player_map)
        fact_deliveries["non_striker_id"] = fact_deliveries["non_striker"].map(player_map)
        fact_deliveries["bowler_id"] = fact_deliveries["bowler"].map(player_map)
        fact_deliveries["player_of_match_id"] = fact_deliveries["player_of_match"].map(player_map)
        fact_deliveries["player_out_id"] = fact_deliveries["player_out"].map(player_map)
        fact_deliveries["wicket_kind_id"] = fact_deliveries["wicket_kind"].map(wicket_map)
        fact_deliveries["stage_id"] = fact_deliveries["stage"].map(stage_map)
        fact_deliveries["season_id"] = fact_deliveries["season"].map(season_map)
        fact_deliveries["toss_winner_id"] = fact_deliveries["toss_winner"].map(team_map)
        fact_deliveries["match_won_by_id"] = fact_deliveries["match_won_by"].map(team_map)
        fact_deliveries["venue_id"] = fact_deliveries["venue"].map(venue_map)
        fact_deliveries["date_id"] = fact_deliveries["date"].map(date_map)
        fact_deliveries["umpire_id"] = fact_deliveries["umpire"].map(umpire_map)
        fact_deliveries["overs"] = fact_deliveries["over"]
        fact_deliveries.drop(columns=['over'], inplace=True)
        logger.info("Mapped dimension attributes to their respective IDs in fact deliveries.")
        
        # Reorder columns: IDs first, then measures and original columns
        id_columns = [
            "delivery_id", "match_id", "date_id", "venue_id", "season_id", "stage_id",
            "batting_team_id", "bowling_team_id", "batter_id", "non_striker_id", "bowler_id",
            "player_of_match_id", "player_out_id", "wicket_kind_id", "toss_winner_id",
            "match_won_by_id", "umpire_id"
        ]
        
        # Keep measure columns (numeric and engineered features)
        measure_columns = [
            "innings", "overs", "ball", "ball_no", "balls_per_over",
            "runs_batter", "runs_extras", "runs_total", "runs_not_boundary",
            "valid_ball", "runs_bowler", "bowler_wicket", "bat_pos", "balls_faced",
            "is_wicket", "is_four", "is_six", "is_boundary", "is_dot"
        ]
        
        # Select only ID and measure columns, drop dimension text columns
        fact_deliveries = fact_deliveries[id_columns + measure_columns]
        
        # Remove duplicate delivery records based on delivery_id (primary key)
        fact_deliveries = fact_deliveries.drop_duplicates(subset=['delivery_id'], keep='first')
        logger.info(f"Removed duplicate deliveries. Final count: {len(fact_deliveries)} records.")
        
        logger.info("Fact deliveries table created successfully.")

        # FACT MATCHES
        fact_matches =df.groupby("match_id").agg({
            "date": "first",
            "venue": "first",
            "season": "first",
            "stage": "first",
            "batting_team": "first",
            "bowling_team": "first",           
            'umpire': 'first',
            "toss_winner": "first",
            "match_won_by": "first",
            "team_runs": "max",
            "team_wicket": "max",
            "team_balls": "sum",
             "runs_target": "first"       
        }).reset_index()

        logger.info("Aggregated match-level data for fact matches.")

        fact_matches["date_id"] = fact_matches["date"].map(date_map)
        fact_matches["venue_id"] = fact_matches["venue"].map(venue_map)
        fact_matches["toss_winner_id"] = fact_matches["toss_winner"].map(team_map)
        fact_matches["winner_team_id"] = fact_matches["match_won_by"].map(team_map)
        fact_matches["umpire_id"] = fact_matches["umpire"].map(umpire_map)
        fact_matches["stage_id"] = fact_matches["stage"].map(stage_map)
        fact_matches["season_id"] = fact_matches["season"].map(season_map)
        fact_matches["batting_team_id"] = fact_matches["batting_team"].map(team_map)
        fact_matches["bowling_team_id"] = fact_matches["bowling_team"].map(team_map)

        logger.info("Mapped dimension attributes to their respective IDs in fact matches.")

        # Keep only ID and measure columns, drop dimension text columns
        fact_matches = fact_matches[[
            "match_id", "date_id", "venue_id", "season_id", "stage_id",
            "batting_team_id", "bowling_team_id", "umpire_id", "toss_winner_id",
            "winner_team_id", "team_runs", "team_wicket", "team_balls", "runs_target"
        ]]

        logger.info("Fact tables created successfully.")


       
    
        Fact_batting = df.groupby('batter').agg({
            'runs_batter': 'sum',
            'valid_ball': 'count',
            'is_four': 'sum',
            'is_six': 'sum',
            'match_id': 'nunique'
            }).reset_index()

        Fact_batting.columns = ['batter', 'total_runs', 'no_balls', 'no_fours', 'no_sixes', 'no_matches']
        Fact_batting['SR'] = (Fact_batting['total_runs'] / Fact_batting['no_balls'] * 100).round(2)
        Fact_batting['Avg'] = (Fact_batting['total_runs'] / Fact_batting['no_matches']).round(2)
        Fact_batting['batter_id'] = Fact_batting['batter'].map(player_map)
        
        # Keep only ID and measure columns, drop player name
        Fact_batting = Fact_batting[[
            'batter_id', 'total_runs', 'no_balls', 'no_fours', 'no_sixes', 'no_matches', 'SR', 'Avg'
        ]]
        
        logger.info("Fact table for batting created successfully.") 

        # Fact_bolwing 
        Fact_bowling = df.groupby('bowler').agg({
            'is_wicket': 'sum',
            'runs_bowler': 'sum',
            'valid_ball': 'count',
            'match_id': 'nunique'
        }).reset_index()

        Fact_bowling.columns = ['bowler', 'no_wickets', 'no_runs', 'no_balls', 'no_matches']
        Fact_bowling['Eco'] = (Fact_bowling['no_runs'] / Fact_bowling['no_balls'] * 6).round(2)
        Fact_bowling['SR'] = (Fact_bowling['no_balls'] / Fact_bowling['no_wickets'].replace(0, 1)).round(2)
        Fact_bowling['Avg'] = (Fact_bowling['no_runs'] / Fact_bowling['no_wickets'].replace(0, 1)).round(2)
        Fact_bowling['bowler_id'] = Fact_bowling['bowler'].map(player_map)
        
        # Keep only ID and measure columns, drop player name
        Fact_bowling = Fact_bowling[[
            'bowler_id', 'no_wickets', 'no_runs', 'no_balls', 'no_matches', 'Eco', 'SR', 'Avg'
        ]]
        
        logger.info("Fact table for bowling created successfully.")

        return fact_deliveries, fact_matches ,Fact_batting, Fact_bowling
        
    except Exception as e:
        logger.error(f"An error occurred while creating fact tables: {e}")
        return None, None, None, None