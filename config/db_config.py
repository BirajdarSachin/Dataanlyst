# Database Configuration
# SQL Server connection parameters

DB_CONFIG = {
    'server': 'DESKTOP-AKHSPQL\MS_SQL_2019',  # Change to your SQL Server instance
    'database': 'IPL_DW',   # Database name
    'username': 'sa',       # SQL Server username
    'password': 'your_password',  # SQL Server password
    'driver': 'ODBC Driver 17 for SQL Server',  # ODBC driver
    'trusted_connection': 'yes',  # Use 'yes' for Windows Authentication
    'port': 1433  # Default SQL Server port
}

# SQLAlchemy engine URL
SQLALCHEMY_DATABASE_URL = (
    f"mssql+pyodbc://{DB_CONFIG['username']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['server']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?"
    f"driver={DB_CONFIG['driver'].replace(' ', '+')}&"
    f"Trusted_Connection={DB_CONFIG['trusted_connection']}"
)

# PyODBC connection string
PYODBC_CONNECTION_STRING = (
    f"DRIVER={{{DB_CONFIG['driver']}}};"
    f"SERVER={DB_CONFIG['server']},{DB_CONFIG['port']};"
    f"DATABASE={DB_CONFIG['database']};"
    f"UID={DB_CONFIG['username']};"
    f"PWD={DB_CONFIG['password']};"
    f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
)
