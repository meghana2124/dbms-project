# --- student_mod.py ---
import customtkinter as ctk
# Import the reusable component
from modules import DataTableFrame 

class StudentModule(ctk.CTkFrame):
    def __init__(self, master, conn):
        super().__init__(master, fg_color="#2B3649")
        self.conn = conn
        
        # Title
        ctk.CTkLabel(self, text="Student Management (Core Data)", 
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#00AEEF").pack(pady=(20, 10), padx=20)

        self.managed_tables = ['Student', 'studentEmail', 'student_skill', 'student_course']
        
        # --- Control Bar (Table Selection) ---
        control_frame = ctk.CTkFrame(self, fg_color="#3A465A")
        control_frame.pack(pady=10, padx=20, fill='x')

        ctk.CTkLabel(control_frame, text="Select Table:").pack(side=ctk.LEFT, padx=10, pady=5)
        
        self.table_var = ctk.StringVar(value=self.managed_tables[0])
        
        sub_table_selector = ctk.CTkComboBox(control_frame, variable=self.table_var, values=self.managed_tables, 
                                            state="readonly", width=250)
        sub_table_selector.pack(side=ctk.LEFT, padx=10, pady=5)
        
        # --- Data Display Area (Uses the reusable component) ---
        self.data_area = DataTableFrame(self, self.conn, self.table_var)
        self.data_area.pack(fill='both', expand=True, padx=20, pady=(0, 20))