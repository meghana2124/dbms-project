# import mysql.connector
# from tkinter import messagebox

# # Ensure db_connector.py is in the same directory to access DB_CONFIG
# try:
#     from db_connector import create_db_connection
# except ImportError:
#     # Fallback or error handling if db_connector is missing
#     pass


# def fetch_table_data(conn, table_name):
#     """Fetches all rows and headers from a specified table."""
#     cursor = None
#     try:
#         # Simple check to prevent basic SQL injection risk on table name
#         # if not table_name.isalnum() and "_" not in table_name:
#         #      raise ValueError("Invalid table name.")
        
#         # Robust check to ensure table name is valid (alphanumeric + underscore)
#         if not table_name or not all(char.isalnum() or char == '_' for char in table_name):
#             raise ValueError("Invalid table name.")  
         
#         cursor = conn.cursor()
#         query = f"SELECT * FROM {table_name}"
#         cursor.execute(query)
        
#         headers = [i[0] for i in cursor.description]
#         data = cursor.fetchall()
        
#         return headers, data
#     except mysql.connector.Error as err:
#         messagebox.showerror("Query Error", f"Failed to fetch data from {table_name}: {err}")
#         return [], []
#     except ValueError as e:
#         messagebox.showerror("Security Error", str(e))
#         return [], []
#     finally:
#         if cursor:
#             cursor.close()



# # --- ADD to utils.py (after fetch_table_data) ---

# def get_table_schema(conn, table_name):
#     """Retrieves column names, types, and primary key status for a given table."""
#     cursor = None
#     schema = []
    
#     # Map of Primary Keys for complex tables (manual lookup required as a simple DESCRIBE doesn't always suffice)
#     PK_MAP = {
#         'Student': 'student_id',
#         'Skill': 'skill_id',
#         'Course': 'course_id',
#         'Company': 'company_id',
#         'PlacementOfficer': 'officer_id',
#         'Recruiter': 'recruiter_id',
#         'JobRole': 'job_id',
#         'application': 'app_id'
#         # Composite keys (like student_skill) will be handled separately in the form logic
#     }
    
#     try:
#         cursor = conn.cursor()
#         # Using DESCRIBE to get basic column info
#         cursor.execute(f"DESCRIBE {table_name}")
#         results = cursor.fetchall()
        
#         # Determine the Primary Key column name
#         pk_column = PK_MAP.get(table_name)
        
#         for col_info in results:
#             col_name = col_info[0]
#             col_type = col_info[1].split('(')[0] # e.g., 'int(11)' -> 'int'
#             is_nullable = col_info[2] == 'YES'
#             is_auto_increment = col_info[5] == 'auto_increment'
#             is_pk = col_name == pk_column or col_info[3] == 'PRI'
            
#             schema.append({
#                 'name': col_name,
#                 'type': col_type,
#                 'is_pk': is_pk,
#                 'is_auto': is_auto_increment,
#                 'nullable': is_nullable
#             })
            
#         return schema
    
#     except mysql.connector.Error as err:
#         messagebox.showerror("Schema Error", f"Failed to retrieve schema for {table_name}: {err}")
#         return None
#     finally:
#         if cursor:
#             cursor.close()

# # --- END of ADD to utils.py ---



# # --- ADD to utils.py (after get_table_schema) ---

# def get_table_primary_key(conn, table_name):
#     """Dynamically retrieves the Primary Key column name(s) for a given table."""
#     cursor = None
    
#     # NOTE: Manually defining composite keys is often necessary for simplicity in Python apps.
#     COMPOSITE_KEYS = {
#         'studentEmail': ['student_id', 's_email'],
#         'placementOfficerEmail': ['officer_id', 'p_email'],
#         'recruiterEmail': ['recruiter_id', 'r_email'],
#         'student_skill': ['student_id', 'skill_id'],
#         'student_course': ['student_id', 'course_id'],
#         'jobrole_skill': ['job_id', 'skill_id'],
#         # Project uses (student_id, project_number) - we will assume project_id is the unique identifier for now
#         # based on your DML (project_id) and DDL (student_id, project_number)
#         # We will prioritize the singular ID if it exists (e.g., job_id, student_id, etc.)
#         'Project': ['project_id'] # NOTE: This assumes project_id is functional despite DDL confusion
#     }
    
#     # Handle composite keys first
#     if table_name in COMPOSITE_KEYS:
#         return COMPOSITE_KEYS[table_name]

#     try:
#         cursor = conn.cursor()
#         # Query MySQL's information schema to find the PK column
#         query = f"""
#             SELECT COLUMN_NAME
#             FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
#             WHERE TABLE_NAME = %s
#             AND CONSTRAINT_NAME = 'PRIMARY';
#         """
#         cursor.execute(query, (table_name,))
        
#         result = cursor.fetchone()
#         if result:
#             return [result[0]] # Return the column name in a list
#         else:
#             return None
#     except mysql.connector.Error as err:
#         print(f"Error retrieving PK for {table_name}: {err}")
#         return None
#     finally:
#         if cursor:
#             cursor.close()

# # --- END of ADD to utils.py ---







import mysql.connector
from tkinter import messagebox

# Ensure db_connector.py is in the same directory to access DB_CONFIG
try:
    from db_connector import create_db_connection
except ImportError:
    # Fallback or error handling if db_connector is missing
    pass


def fetch_table_data(conn, table_name):
    """Fetches all rows and headers from a specified table."""
    cursor = None
    try:
        # Simple check to prevent basic SQL injection risk on table name
        # if not table_name.isalnum() and "_" not in table_name:
        #      raise ValueError("Invalid table name.")
        
        # Robust check to ensure table name is valid (alphanumeric + underscore)
        if not table_name or not all(char.isalnum() or char == '_' for char in table_name):
            raise ValueError("Invalid table name.")  
         
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        
        headers = [i[0] for i in cursor.description]
        data = cursor.fetchall()
        
        return headers, data
    except mysql.connector.Error as err:
        messagebox.showerror("Query Error", f"Failed to fetch data from {table_name}: {err}")
        return [], []
    except ValueError as e:
        messagebox.showerror("Security Error", str(e))
        return [], []
    finally:
        if cursor:
            cursor.close()



# --- ADD to utils.py (after fetch_table_data) ---

def get_table_schema(conn, table_name):
    """Retrieves column names, types, and primary key status for a given table."""
    cursor = None
    schema = []
    
    # Map of Primary Keys for complex tables (manual lookup required as a simple DESCRIBE doesn't always suffice)
    PK_MAP = {
        'Student': 'student_id',
        'Skill': 'skill_id',
        'Course': 'course_id',
        'Company': 'company_id',
        'PlacementOfficer': 'officer_id',
        'Recruiter': 'recruiter_id',
        'JobRole': 'job_id',
        'application': 'app_id'
        # Composite keys (like student_skill) will be handled separately in the form logic
    }
    
    try:
        cursor = conn.cursor()
        # Using DESCRIBE to get basic column info
        cursor.execute(f"DESCRIBE {table_name}")
        results = cursor.fetchall()
        
        # Determine the Primary Key column name
        pk_column = PK_MAP.get(table_name)
        
        for col_info in results:
            col_name = col_info[0]
            col_type = col_info[1].split('(')[0] # e.g., 'int(11)' -> 'int'
            is_nullable = col_info[2] == 'YES'
            is_auto_increment = col_info[5] == 'auto_increment'
            is_pk = col_name == pk_column or col_info[3] == 'PRI'
            
            schema.append({
                'name': col_name,
                'type': col_type,
                'is_pk': is_pk,
                'is_auto': is_auto_increment,
                'nullable': is_nullable
            })
            
        return schema
    
    except mysql.connector.Error as err:
        messagebox.showerror("Schema Error", f"Failed to retrieve schema for {table_name}: {err}")
        return None
    finally:
        if cursor:
            cursor.close()

# --- END of ADD to utils.py ---



# --- ADD to utils.py (after get_table_schema) ---

def get_table_primary_key(conn, table_name):
    """Dynamically retrieves the Primary Key column name(s) for a given table."""
    cursor = None
    
    # NOTE: Manually defining composite keys is often necessary for simplicity in Python apps.
    COMPOSITE_KEYS = {
        'studentEmail': ['student_id', 's_email'],
        'placementOfficerEmail': ['officer_id', 'p_email'],
        'recruiterEmail': ['recruiter_id', 'r_email'],
        'student_skill': ['student_id', 'skill_id'],
        'student_course': ['student_id', 'course_id'],
        'jobrole_skill': ['job_id', 'skill_id'],
        # Project uses (student_id, project_number) - we will assume project_id is the unique identifier for now
        # based on your DML (project_id) and DDL (student_id, project_number)
        # We will prioritize the singular ID if it exists (e.g., job_id, student_id, etc.)
        'Project': ['project_id'] # NOTE: This assumes project_id is functional despite DDL confusion
    }
    
    # Handle composite keys first
    if table_name in COMPOSITE_KEYS:
        return COMPOSITE_KEYS[table_name]

    try:
        cursor = conn.cursor()
        # Query MySQL's information schema to find the PK column
        query = f"""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = %s
            AND CONSTRAINT_NAME = 'PRIMARY';
        """
        cursor.execute(query, (table_name,))
        
        result = cursor.fetchone()
        if result:
            return [result[0]] # Return the column name in a list
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error retrieving PK for {table_name}: {err}")
        return None
    finally:
        if cursor:
            cursor.close()

# --- END of ADD to utils.py ---