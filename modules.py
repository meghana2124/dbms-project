# --- modules.py ---
import customtkinter as ctk
from tkinter import ttk, messagebox
import sys
import mysql.connector

# Import functions from utils and db_connector
try:
    # utils.py must be in the same directory
    from utils import fetch_table_data 
except ImportError as e:
    print(f"FATAL ERROR in modules.py: Missing dependency import: {e}")
    sys.exit()

# --------------------------------------------------------------------------------
# --- Reusable Component: DataTableFrame (Handles Treeview and Read/View) ---
# --------------------------------------------------------------------------------
# --- ADD to modules.py (after imports, before DataTableFrame) ---
# --- COMPLETE RecordForm CLASS (Handles INSERT and UPDATE) ---

class RecordForm(ctk.CTkToplevel):
    # Modified signature to accept optional data for update operations
    def __init__(self, master, conn, table_name, schema, record_data=None, pk_data=None):
        super().__init__(master)
        self.conn = conn
        self.table_name = table_name
        self.schema = schema
        self.record_data = record_data  # Existing data (dict: col_name -> value)
        self.pk_data = pk_data          # PK info for UPDATE WHERE clause ({'columns': [...], 'values': [...]})
        self.entries = {}
        
        # Adjust title and button text based on action
        action = "Update Existing" if record_data else "Add New"
        submit_text = "Save Changes" if record_data else "Submit Record"
        
        self.title(f"{action} Record in {table_name}")
        self.geometry("450x600")
        self.grab_set() 
        
        # Scrollable Frame for Form Inputs
        self.main_frame = ctk.CTkScrollableFrame(self, label_text=f"Fields for {table_name}", 
                                                 fg_color="#3A465A", label_fg_color="#2B3649")
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self._build_form()
        
        # Submit Button
        ctk.CTkButton(self, text=submit_text, command=self._submit_record, 
                      fg_color="#4CAF50" if not record_data else "#FFA726", 
                      hover_color="#388E3C" if not record_data else "#FB8C00").pack(pady=10)

    def _build_form(self):
        row_num = 0
        input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(padx=10, pady=10, fill='x')
        input_frame.columnconfigure(1, weight=1)
        
        for col in self.schema:
            # Skip Auto-Incrementing Primary Keys (handled by DB on INSERT)
            if col['is_auto']:
                continue 
            
            col_name = col['name']
            
            # Label
            label_text = col_name + (" (*)" if not col['nullable'] else "")
            ctk.CTkLabel(input_frame, text=label_text, anchor="w", 
                         text_color="#00AEEF" if col['is_pk'] else "white").grid(row=row_num, column=0, padx=10, pady=5, sticky='w')
            
            entry = ctk.CTkEntry(input_frame, width=250)
            entry.grid(row=row_num, column=1, padx=10, pady=5, sticky='ew')
            
            # --- PRE-FILLING LOGIC for UPDATE ---
            if self.record_data and col_name in self.record_data and self.record_data[col_name] is not None:
                # Format non-string types for display if necessary (e.g., date objects)
                value_str = str(self.record_data[col_name])
                entry.insert(0, value_str)
            
            # Disable primary key fields in UPDATE mode to maintain data integrity
            if self.pk_data and col['is_pk'] and col_name in self.pk_data['columns']:
                 entry.configure(state='disabled')
            
            self.entries[col_name] = entry
            row_num += 1

    def _submit_record(self):
        """Executes INSERT or UPDATE based on whether self.pk_data is present."""
        columns = []
        values = []
        placeholders = []
        
        # 1. Collect Data & Validate
        for col_name, entry_widget in self.entries.items():
            # If the entry is disabled (PK on update), use the original value
            if entry_widget.cget("state") == 'disabled':
                value = entry_widget.get().strip()
            else:
                value = entry_widget.get().strip()

            col_schema = next(col for col in self.schema if col['name'] == col_name)
            if not col_schema['nullable'] and not value:
                messagebox.showerror("Validation Error", f"Field '{col_name}' cannot be empty.")
                return

            columns.append(col_name)
            values.append(value if value != "" else None)
            placeholders.append("%s")
        
        if not columns:
            return

        cursor = self.conn.cursor()
        
        if self.pk_data:
            # --- UPDATE QUERY CONSTRUCTION ---
            set_clauses = [f"{col} = %s" for col in columns]
            where_clauses = [f"{pk_col} = %s" for pk_col in self.pk_data['columns']]
            
            sql = f"UPDATE {self.table_name} SET {', '.join(set_clauses)} WHERE {' AND '.join(where_clauses)}"
            
            # Values: [column_values] + [pk_values]
            update_values = values + self.pk_data['values']
            action_msg = "updated"
            
        else:
            # --- INSERT QUERY CONSTRUCTION ---
            cols_str = ", ".join(columns)
            placeholders_str = ", ".join(placeholders)
            sql = f"INSERT INTO {self.table_name} ({cols_str}) VALUES ({placeholders_str})"
            update_values = values
            action_msg = "added"
        
        try:
            # 3. Execute Query
            cursor.execute(sql, tuple(update_values))
            self.conn.commit()
            messagebox.showinfo("Success", f"Record successfully {action_msg} in {self.table_name}.")
            
            # Refresh the parent Treeview
            if hasattr(self.master, 'read_data'):
                self.master.read_data() 
            self.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to {action_msg} record: {err}")
            self.conn.rollback()
        finally:
            cursor.close()

# --- END OF COMPLETE RecordForm CLASS ---

class DataTableFrame(ctk.CTkFrame):
    """
    A reusable frame containing the styled Treeview and basic CRUD buttons 
    for any single table view within the main modules.
    """
    def __init__(self, master, conn, table_name_var):
        super().__init__(master, fg_color="#3A465A") # Inner frame color
        self.conn = conn
        self.table_name_var = table_name_var
        
        # --- CRUD Control Bar ---
        crud_frame = ctk.CTkFrame(self, fg_color="transparent")
        crud_frame.pack(pady=10, padx=10, fill='x')

        # View Data Button (Reads/Refreshes data)
        ctk.CTkButton(crud_frame, text="View/Refresh Data", command=self.read_data, 
                      fg_color="#00AEEF", hover_color="#0080B0").pack(side=ctk.LEFT, padx=10)
        
        # CRUD Buttons (Currently Stubs, logic needs implementation)
        ctk.CTkButton(crud_frame, text="Add New Record", command=self.create_record,
                      fg_color="#4CAF50", hover_color="#388E3C").pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(crud_frame, text="Edit Selected", command=self.update_record, 
                      fg_color="#FFA726", hover_color="#FB8C00").pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(crud_frame, text="Delete Selected", command=self.delete_record,
                      fg_color="#A33A3A", hover_color="#802A2A").pack(side=ctk.LEFT, padx=5)

        # --- Treeview Setup ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#3A465A", foreground="white", rowheight=35, fieldbackground="#3A465A",font=('Arial', 11))
        style.map('Treeview', background=[('selected', '#00AEEF')])
        style.configure("Treeview.Heading", font=('Arial', 20, 'bold'), background="#4A566A", foreground="white")
        
        self.tree = ttk.Treeview(self)
        self.tree.pack(padx=10, pady=(0, 10), fill='both', expand=True)

        # Initial load and auto-refresh setup
        self.read_data()
        self.table_name_var.trace_add("write", lambda *args: self.read_data())

    # --- CRUD STUB METHODS (Require implementation) ---
# --- REVISED DataTableFrame.read_data in modules.py ---
    def read_data(self):
        """Fetches and displays all data, adding calculated columns for Student table."""
        table_name = self.table_name_var.get()
        
        # --- FIX 1: Prevents 'Invalid table name' error on module switch ---
        if not table_name:
            return 
        
        # Clear previous data
        self.tree.delete(*self.tree.get_children())
        self.tree.configure(columns=()) 
        
        # Ensure utilities are available
        try:
            from utils import fetch_table_data
        except ImportError:
            messagebox.showerror("Error", "Missing utils.py dependency.")
            return

        headers, data = [], []

        if table_name == 'Student':
            # --- FIX 2: Corrected SQL Function Names ---
            # This query now logically integrates all 4 of your SQL functions
            sql_query = f"""
                SELECT 
                    s.student_id, 
                    s.first_name, 
                    s.last_name, 
                    s.branch, 
                    s.cgpa,
                    CalculateAge(s.dob) AS Age, 
                    GetStudentProjectCount(s.student_id) AS Total_Projects,
                    GetStudentSkillCount(s.student_id) AS Total_Skills,
                    GetStudentSuccessRate(s.student_id) AS Success_Rate,
                    s.s_phone,
                    s.degree,
                    s.resume_link,
                    s.dob
                FROM Student s
                ORDER BY s.student_id
            """
            headers, data = self._fetch_special_query(sql_query)
            
        else:
            # --- Path for ALL OTHER Tables (Generic Fetch) ---
            headers, data = fetch_table_data(self.conn, table_name)


        if not headers:
            # Fallback error display
            self.tree["columns"] = ("Message",)
            self.tree.heading("Message", text=f"Could not load data for {table_name}. (Check console for DB error.)")
            self.tree.column("Message", width=400, anchor='center')
            return

        # --- Configuration and Population (Unchanged) ---
        self.tree["columns"] = headers
        self.tree["show"] = "headings"
        for col in headers:
            self.tree.heading(col, text=col)
            # Auto-size columns
            width = max(len(col) * 10, 100) # Base width on header
            self.tree.column(col, width=width, stretch=True, anchor='w') 

        for row in data:
            self.tree.insert("", ctk.END, values=row)

    # def create_record(self):
    #     messagebox.showinfo("Action Required", f"Implementation needed: Open form to INSERT into {self.table_name_var.get()}.")
    # --- REPLACE create_record in DataTableFrame in modules.py ---

    def create_record(self):
        """Opens a dynamic form to add a new record to the currently selected table."""
        table_name = self.table_name_var.get()
        
        # 1. Get Schema
        # Note: utils.py must be imported correctly for this to work
        try:
            from utils import get_table_schema 
        except ImportError:
            messagebox.showerror("Error", "Cannot import get_table_schema from utils.py")
            return
            
        schema = get_table_schema(self.conn, table_name)
        
        if schema:
            # 2. Open Form Window
            # Note: self.master is the main Module (e.g., StudentModule), which needs the conn object.
            RecordForm(self, self.conn, table_name, schema)
        else:
            messagebox.showwarning("Error", f"Could not retrieve schema for {table_name}. Cannot open form.")
            
    # --- END of REPLACE ---
    # def update_record(self):
    #     messagebox.showinfo("Action Required", f"Implementation needed: Open form to UPDATE record in {self.table_name_var.get()}.")
    # def delete_record(self):
    #     messagebox.showinfo("Action Required", f"Implementation needed: Execute DELETE query for selected record in {self.table_name_var.get()}.")

# --- REPLACE delete_record in DataTableFrame in modules.py ---

    def delete_record(self):
        """Deletes the currently selected record using its Primary Key."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return

        table_name = self.table_name_var.get()
        
        try:
            # 1. Get Primary Key Info
            from utils import get_table_primary_key
            pk_columns = get_table_primary_key(self.conn, table_name)
            
            if not pk_columns:
                messagebox.showwarning("Error", f"Could not identify Primary Key for {table_name}.")
                return
                
            # 2. Retrieve Data for the selected row
            selected_data = self.tree.item(selected_item, 'values')
            
            # 3. Get column headers to map data index to PK column name
            headers = self.tree["columns"]
            
            # Build the WHERE clause (handles both single and composite keys)
            where_clauses = []
            pk_values = []
            
            for pk_col in pk_columns:
                try:
                    col_index = headers.index(pk_col)
                    pk_value = selected_data[col_index]
                    where_clauses.append(f"{pk_col} = %s")
                    pk_values.append(pk_value)
                except ValueError:
                    messagebox.showerror("Error", f"Primary Key column '{pk_col}' not found in display data.")
                    return

            # 4. Confirmation
            pk_display = ", ".join([f"{c}={v}" for c, v in zip(pk_columns, pk_values)])
            confirm = messagebox.askyesno(
                "Confirm Deletion", 
                f"Are you sure you want to delete the following record from {table_name}?\n\nKey: {pk_display}"
            )

            if confirm:
                cursor = self.conn.cursor()
                sql = f"DELETE FROM {table_name} WHERE {' AND '.join(where_clauses)}"
                
                # 5. Execute Delete
                cursor.execute(sql, tuple(pk_values))
                self.conn.commit()
                messagebox.showinfo("Success", "Record deleted successfully.")
                self.read_data() # Refresh table view
                
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to delete record. Check foreign key constraints: {err}")
            self.conn.rollback()
        except Exception as e:
            messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()

    # --- END of REPLACE delete_record ---
    


    # --- REPLACE update_record in DataTableFrame in modules.py ---

    def update_record(self):
        """Opens a form pre-filled with the selected record's data for update."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to update.")
            return
            
        table_name = self.table_name_var.get()
        
        try:
            from utils import get_table_schema, get_table_primary_key
            
            # 1. Get Schema and PK Info
            schema = get_table_schema(self.conn, table_name)
            pk_columns = get_table_primary_key(self.conn, table_name)
            if not schema or not pk_columns:
                messagebox.showwarning("Error", f"Could not retrieve schema or PK for {table_name}.")
                return
                
            # 2. Get Selected Data
            selected_data_tuple = self.tree.item(selected_item, 'values')
            headers = self.tree["columns"]
            
            # Map tuple data to column names (dictionary for easy lookup)
            record_data = dict(zip(headers, selected_data_tuple))
            
            # 3. Prepare PK Data
            pk_values = [record_data[col] for col in pk_columns]
            pk_data = {'columns': pk_columns, 'values': pk_values}
            
            # 4. Open Form Window
            RecordForm(self, self.conn, table_name, schema, record_data=record_data, pk_data=pk_data)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to prepare update form: {e}")
            
    # --- END of REPLACE update_record ---



    # --- ADD this method INSIDE the DataTableFrame class in modules.py ---

    def _fetch_special_query(self, sql_query):
        """Helper function to fetch data for calculated columns using a specific SQL query."""
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_query)
            headers = [i[0] for i in cursor.description]
            data = cursor.fetchall()
            return headers, data
        except mysql.connector.Error as err:
            messagebox.showerror("Function Error", f"Failed to fetch data using functions: {err}")
            return [], []
        finally:
            if cursor:
                cursor.close()