  DROP TABLE IF EXISTS dim_date ;
  DROP TABLE IF EXISTS dim_player;
  DROP TABLE IF EXISTS dim_venue;
  DROP TABLE IF EXISTS dim_wickets;
  DROP TABLE IF EXISTS dim_umpires;
  DROP TABLE IF EXISTS dim_team;
  DROP TABLE IF EXISTS dim_stage;



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

