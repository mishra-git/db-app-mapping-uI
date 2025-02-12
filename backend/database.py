import pyodbc
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Database connection details
server = "appmapping.database.windows.net"
database = "appmapping"
username = "appmappingadmin"
password = "Abcd123abcd123!"
driver = "{ODBC Driver 17 for SQL Server}"

try:
    conn_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    conn = pyodbc.connect(conn_string, autocommit=True)
    cursor = conn.cursor()
    logging.info("✅ Successfully connected to the database.")
except Exception as e:
    logging.error("❌ Database connection failed:", exc_info=True)

# ✅ Fetch all mappings
def get_all_mappings():
    try:
        cursor.execute("SELECT id, application_name, database_name ,instance_name ,database_type, team_name,environment,server_owner,database_owner,application_contacts,created_at, updated_at from db_application_tracking")
        rows = cursor.fetchall()
        return [{
            "id": row.id,
            "application_name": row.application_name,
            "database_name": row.database_name,
            "instance_name": row.instance_name,
            "database_type": row.database_type,
            "team_name": row.team_name,
            "environment": row.environment,
            "server_owner": row.server_owner,
            "database_owner": row.database_owner,
            "application_contacts": row.application_contacts,
            "created_at": row.created_at,
            "updated_at": row.updated_at
        } for row in rows]
    except Exception as e:
        logging.error("❌ Error fetching data:", exc_info=True)
        return {"error": str(e)}

# ✅ Add a new mapping
def add_mapping(application_name, database_name, instance_name, database_type, team_name, environment, server_owner, database_owner, application_contacts):
    try:
        cursor.execute("""
            INSERT INTO db_application_tracking 
            (application_name, database_name, instance_name, database_type, team_name, environment, server_owner, database_owner, application_contacts) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (application_name, database_name, instance_name, database_type, team_name, environment, server_owner, database_owner, application_contacts))
        return {"message": "Mapping added successfully"}
    except Exception as e:
        logging.error("❌ Error inserting data:", exc_info=True)
        return {"error": str(e)}

# ✅ Update a mapping
def update_mapping(mapping_id, application_name, database_name, instance_name, database_type, team_name, environment, server_owner, database_owner, application_contacts):
    try:
        cursor.execute("""
            UPDATE db_application_tracking 
            SET application_name=?, database_name=?, instance_name=?, database_type=?, team_name=?, environment=?, server_owner=?, database_owner=?, application_contacts=?, updated_at=SYSUTCDATETIME()
            WHERE id=?
        """, (application_name, database_name, instance_name, database_type, team_name, environment, server_owner, database_owner, application_contacts, mapping_id))
        return {"message": f"Mapping with ID {mapping_id} updated successfully"}
    except Exception as e:
        logging.error("❌ Error updating data:", exc_info=True)
        return {"error": str(e)}

# ✅ Delete a mapping
def delete_mapping(mapping_id):
    try:
        cursor.execute("DELETE FROM db_application_tracking WHERE id=?", (mapping_id,))
        return {"message": f"Mapping with ID {mapping_id} deleted successfully"}
    except Exception as e:
        logging.error("❌ Error deleting data:", exc_info=True)
        return {"error": str(e)}