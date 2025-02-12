import pyodbc

# Database connection
server = "appmapping.database.windows.net"
database = "appmapping"
username = "appmappingadmin"
password = "Abcd123abcd123!"
driver = "{ODBC Driver 17 for SQL Server}"

conn_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
conn = pyodbc.connect(conn_string)
cursor = conn.cursor()

# Test Query
try:
    cursor.execute("SELECT * FROM ApplicationDatabaseMapping")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print("✅ Database connection and query successful!")
except Exception as e:
    print("❌ Error:", e)
