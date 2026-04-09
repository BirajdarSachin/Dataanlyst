# Database Configuration
# SQL Server connection parameters

DB_CONFIG = {
    "server": "DESKTOP-AKHSPQL\\MS_SQL_2019",  # Change if needed
    "database": "IPL_DW",
    "driver": "ODBC Driver 18 for SQL Server",
}


# =========================================================
# OPTION 1: WINDOWS AUTHENTICATION (RECOMMENDED)
# =========================================================

PYODBC_CONN_STR_WINDOWS = (
    f"DRIVER={{{DB_CONFIG['driver']}}};"
    f"SERVER={DB_CONFIG['server']};"
    f"DATABASE={DB_CONFIG['database']};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)


SQLALCHEMY_URL_WINDOWS = (
    f"mssql+pyodbc://@{DB_CONFIG['server']}/{DB_CONFIG['database']}?"
    f"driver={DB_CONFIG['driver'].replace(' ', '+')}&"
    f"trusted_connection=yes&"
    f"TrustServerCertificate=yes"
)


# =========================================================
# OPTION 2: SQL AUTHENTICATION (USE ONLY IF ENABLED)
# =========================================================

DB_CONFIG_SQL_AUTH = {
    "server": "DESKTOP-AKHSPQL\\MS_SQL_2019",
    "database": "IPL_DW",
    "username": "sa",
    "password": "your_password",
    "driver": "ODBC Driver 18 for SQL Server",
}

PYODBC_CONN_STR_SQL = (
    f"DRIVER={{{DB_CONFIG_SQL_AUTH['driver']}}};"
    f"SERVER={DB_CONFIG_SQL_AUTH['server']};"
    f"DATABASE={DB_CONFIG_SQL_AUTH['database']};"
    f"UID={DB_CONFIG_SQL_AUTH['username']};"
    f"PWD={DB_CONFIG_SQL_AUTH['password']};"
    f"TrustServerCertificate=yes;"
)



SQLALCHEMY_URL_SQL = (
    f"mssql+pyodbc://{DB_CONFIG_SQL_AUTH['username']}:{DB_CONFIG_SQL_AUTH['password']}"
    f"@{DB_CONFIG_SQL_AUTH['server']}/{DB_CONFIG_SQL_AUTH['database']}?"
    f"driver={DB_CONFIG_SQL_AUTH['driver'].replace(' ', '+')}&"
    f"TrustServerCertificate=yes"
)


