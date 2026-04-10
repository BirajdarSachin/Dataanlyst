  DROP TABLE IF EXISTS dim_date ;
  DROP TABLE IF EXISTS dim_player;
  DROP TABLE IF EXISTS dim_venue;
  DROP TABLE IF EXISTS dim_wickets;
  DROP TABLE IF EXISTS dim_umpires;
  DROP TABLE IF EXISTS dim_team;
  DROP TABLE IF EXISTS dim_stage;
  DROP TABLE IF EXISTS dim_seasons;
  DROP TABLE IF EXISTS fact_batting;
  DROP TABLE IF EXISTS fact_bowling;
  DROP TABLE IF EXISTS fact_matches;
  DROP TABLE IF EXISTS fact_deliveries;

	 create table dim_date(date_id int primary key
	  ,date date
      ,day varchar(225)
      ,month varchar(225)
      ,year varchar(225)
      ,season varchar(225)
      );

	create table dim_team( team_id int primary key,
	  team_name varchar(225));

	create table [dim_player]( [player_id] int primary key,
	  [player_name] varchar(225));

	  
	create table [dim_umpires]( [umpire_id] int primary key,
	  [umpire_name] varchar(225));

	 create table [dim_venue]( [venue_id] int primary key,
	  [venue] varchar(225));

	  create table [dim_wickets]( [wicket_id] int primary key,
	  [wiket_type] varchar(225));

	  create table dim_stage(stage_id int primary key,
	  stage varchar(225));

	  create table dim_seasons(season_id int primary key,
	  season_name varchar(225));

	CREATE TABLE fact_batting (
    batter_id INT PRIMARY KEY,
    total_runs INT,
    no_balls INT,
    no_fours INT,
    no_sixes INT,
    no_matches INT,
    SR FLOAT,
    Avg FLOAT,

    CONSTRAINT FK_fact_batting_player
    FOREIGN KEY (batter_id)
    REFERENCES dim_player(player_id)
);


CREATE TABLE fact_bowling (
    bowler_id INT PRIMARY KEY,
    no_wickets INT,
    no_runs INT,
    no_balls INT,
    no_matches INT,
    Eco FLOAT,
    SR FLOAT,
    Avg FLOAT,

    CONSTRAINT FK_fact_bowling_player
    FOREIGN KEY (bowler_id)
    REFERENCES dim_player(player_id)
);


CREATE TABLE fact_matches (
    match_id INT PRIMARY KEY,
    date_id INT,
    venue_id INT,
    season_id INT,
    stage_id INT,
    batting_team_id INT,
    bowling_team_id INT,
    umpire_id INT,
    toss_winner_id INT,
    winner_team_id INT,
    team_runs INT,
    team_wicket INT,
    team_balls INT,
    runs_target INT,

    -- Foreign Keys
    CONSTRAINT FK_fact_matches_date
        FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id),

    CONSTRAINT FK_fact_matches_venue
        FOREIGN KEY (venue_id)
        REFERENCES dim_venue(venue_id),

    CONSTRAINT FK_fact_matches_season
        FOREIGN KEY (season_id)
        REFERENCES dim_seasons(season_id),

    CONSTRAINT FK_fact_matches_stage
        FOREIGN KEY (stage_id)
        REFERENCES dim_stage(stage_id),

    CONSTRAINT FK_fact_matches_batting_team
        FOREIGN KEY (batting_team_id)
        REFERENCES dim_team(team_id),

    CONSTRAINT FK_fact_matches_bowling_team
        FOREIGN KEY (bowling_team_id)
        REFERENCES dim_team(team_id),

    CONSTRAINT FK_fact_matches_toss_winner
        FOREIGN KEY (toss_winner_id)
        REFERENCES dim_team(team_id),

    CONSTRAINT FK_fact_matches_winner
        FOREIGN KEY (winner_team_id)
        REFERENCES dim_team(team_id),

    CONSTRAINT FK_fact_matches_umpire
        FOREIGN KEY (umpire_id)
        REFERENCES dim_umpires(umpire_id)
);

CREATE TABLE fact_deliveries (
    delivery_id VARCHAR(50) PRIMARY KEY,
    match_id INT,
    date_id INT,
    venue_id INT,
    season_id INT,
    stage_id INT,
    batting_team_id INT,
    bowling_team_id INT,
    batter_id INT,
    non_striker_id INT,
    bowler_id INT,
    player_of_match_id INT,
    player_out_id INT,
    wicket_kind_id INT,
    toss_winner_id INT,
    match_won_by_id INT,
    umpire_id INT,
    innings INT,
    overs INT,
    ball FLOAT,
    ball_no INT,
    balls_per_over INT,
    runs_batter INT,
    runs_extras INT,
    runs_total INT,
    runs_not_boundary INT,
    valid_ball INT,
    runs_bowler INT,
    bowler_wicket INT,
    bat_pos INT,
    balls_faced INT,
    is_wicket INT,
    is_four INT,
    is_six INT,
    is_boundary INT,
    is_dot INT,

    -- Foreign Keys
    CONSTRAINT FK_fact_deliveries_match
        FOREIGN KEY (match_id)
        REFERENCES fact_matches(match_id),

    CONSTRAINT FK_fact_deliveries_date
        FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id),

    CONSTRAINT FK_fact_deliveries_venue
        FOREIGN KEY (venue_id)
        REFERENCES dim_venue(venue_id),

    CONSTRAINT FK_fact_deliveries_season
        FOREIGN KEY (season_id)
        REFERENCES dim_seasons(season_id),

    CONSTRAINT FK_fact_deliveries_stage
        FOREIGN KEY (stage_id)
        REFERENCES dim_stage(stage_id),

    CONSTRAINT FK_fact_deliveries_batting_team
        FOREIGN KEY (batting_team_id)
        REFERENCES dim_team(team_id),

    CONSTRAINT FK_fact_deliveries_bowling_team
        FOREIGN KEY (bowling_team_id)
        REFERENCES dim_team(team_id),

    CONSTRAINT FK_fact_deliveries_batter
        FOREIGN KEY (batter_id)
        REFERENCES dim_player(player_id),

    CONSTRAINT FK_fact_deliveries_non_striker
        FOREIGN KEY (non_striker_id)
        REFERENCES dim_player(player_id),

    CONSTRAINT FK_fact_deliveries_bowler
        FOREIGN KEY (bowler_id)
        REFERENCES dim_player(player_id),

    CONSTRAINT FK_fact_deliveries_player_of_match
        FOREIGN KEY (player_of_match_id)
        REFERENCES dim_player(player_id),

    CONSTRAINT FK_fact_deliveries_player_out
        FOREIGN KEY (player_out_id)
        REFERENCES dim_player(player_id),

    CONSTRAINT FK_fact_deliveries_wicket_kind
        FOREIGN KEY (wicket_kind_id)
        REFERENCES dim_wickets(wicket_id),

    CONSTRAINT FK_fact_deliveries_toss_winner
        FOREIGN KEY (toss_winner_id)
        REFERENCES dim_team(team_id),

    CONSTRAINT FK_fact_deliveries_match_won_by
        FOREIGN KEY (match_won_by_id)
        REFERENCES dim_team(team_id),

    CONSTRAINT FK_fact_deliveries_umpire
        FOREIGN KEY (umpire_id)
        REFERENCES dim_umpires(umpire_id)
);

