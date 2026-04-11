IPL Data Warehouse Project
📌 Objective

The objective of this project is to build a scalable Data Warehouse for IPL cricket data using a Star Schema architecture.
It transforms raw ball-by-ball data into structured tables to enable:

Match analysis
Player performance insights
Team comparison
Advanced analytics using BI tools
📖 Project Abstract

This project presents the design and implementation of a Data Warehouse for IPL cricket analytics using a Star Schema architecture and a Python-based ETL pipeline.

The dataset contains multi-granular information, including match-level and ball-level events. To address this, separate fact tables were designed—fact_matches for match-level data and fact_deliveries for ball-level data—ensuring accurate aggregation and efficient query performance.

The ETL process extracts data from CSV files, cleans and transforms it, and loads it into SQL Server. Surrogate keys are used to maintain referential integrity.

This warehouse enables analysis of player performance, team strategies, and match outcomes, demonstrating real-world data engineering practices.

🧱 Architecture
Kaggle CSV → Python ETL (Pandas) → SQL Server (Data Warehouse) → Tableau Dashboard


📊 Data Source

IPL Dataset (2008–2025)

Ball-by-ball match data
Player statistics
Match outcomes
Over 60+ attributes

⭐ Data Model (Star Schema)
🔹 Fact Tables
Table	Grain	Description
fact_matches	1 row per match	Match-level data
fact_deliveries	1 row per ball	Ball-level data
fact_batting	1 row per player	Batting stats
fact_bowling	1 row per player	Bowling stats


🔹 Dimension Tables
dim_date
dim_team
dim_player
dim_venue
dim_wickets
dim_umpires
dim_stage
dim_seasons


🔗 ER Diagram (Concept)
                           dim_date
                             |
                         fact_matches -------- dim_stage
                             |
                         fact_deliveries -------- dim_wickets
                        /               \
               fact_batting         fact_bowling

dim_team   dim_player   dim_venue   dim_seasons   dim_umpires


🔗 Relationships
1 Match → Many Deliveries
1 Player → Many Deliveries
1 Team → Many Matches
1 Player → 1 Batting Record
1 Player → 1 Bowling Record

🛠️ Database Schema
Fully normalized Star Schema
Primary Keys for uniqueness
Foreign Keys for relationships
Multi-fact design


🔄 ETL Process
1. Extract
Load CSV using Python (Pandas)

2. Transform
Remove duplicates
Handle null values
Standardize columns
Merge duplicate fields
Generate surrogate keys

3. Load
Load into SQL Server using SQLAlchemy and pyodbc
📊 Logging & Monitoring
🔹 Features
Tracks ETL stages
Logs success & failure
Captures errors
🔹 Log File
logs/etl.log
🔹 Example
INFO - ETL Job Started
INFO - Data Extracted
INFO - Data Loaded


📁 Project Structure
IPL-Data-Warehouse/
│
├── data/
│   └── IPL.csv
│
├── sql/
│   └── schema.sql
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── validation.py
│   ├── logger.py
│
├── ipl_dw_sql_server/
│   ├── Data_warehouse diagrams/
│   │   └── IPL_data_warehouse_Database_Diagrams.pdf
│   └── DB_Backup/
│       └── IPL_DW.bak
│
├── config/
│   └── db_config.py
│
├── main.py
├── requirements.txt
├── README.md
└── logs/
    └── etl.log

🔧 Steps to Rebuild This Project
1. Clone Repo
git clone <repo-url>
cd IPL-Data-Warehouse
2. Setup Environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
3. Add Dataset
data/IPL.csv
4. Configure DB

Update:

config/db_config.py
5. Create Tables

Run:

sql/schema.sql
6. Run ETL
python main.py
7. Validate Data
SELECT COUNT(*) FROM fact_matches;
SELECT COUNT(*) FROM fact_deliveries;
8. Use Tableau
Connect to SQL Server
Build dashboards

📊 Tableau Dashboard
Match analysis
Player performance
Team comparison
Venue insights


🚀 Features
Star Schema design
Multi-grain modeling
Python ETL pipeline
Logging system
Data validation
Scalable architecture
Database backup included

📚 Learnings
Data Warehouse design
ETL pipeline development
Data cleaning techniques
Handling multi-grain datasets
SQL optimization
Real-world project structuring


📦 References Included
Database Diagram (PDF)
Database Backup (.bak)
Dataset (CSV)

🔥 Key Notes
Ensure SQL Server is running
Do not change grain of fact tables
Validate data after load
Update DB credentials

👤 Author

Sachin Birajdar

🚀 One-Line Summary

Built an end-to-end IPL Data Warehouse using Python ETL, SQL Server, and Tableau for analytics.

⭐ Future Improvements
Add incremental load
Add Airflow scheduling
Add more dashboards

