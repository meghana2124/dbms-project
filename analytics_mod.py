# --- analytics_mod.py ---
import customtkinter as ctk
from tkinter import messagebox, ttk
from utils import fetch_table_data # Used to fetch list of skills

class AnalyticsModule(ctk.CTkFrame):
    def __init__(self, master, conn):
        super().__init__(master, fg_color="#2B3649")
        self.conn = conn
        
        ctk.CTkLabel(self, text="Database Analytics & Reports", 
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#00AEEF").pack(pady=(20, 10), padx=20)

        # Tab View to organize different reports
        self.tab_view = ctk.CTkTabview(self, fg_color="#3A465A", segmented_button_selected_color="#00AEEF")
        self.tab_view.pack(padx=20, pady=20, fill="both", expand=True)

        self.tab_view.add("Top Students by Skill")
        self.tab_view.add("Other Reports")
        
        self._setup_top_students_tab(self.tab_view.tab("Top Students by Skill"))
        self._setup_results_display(self.tab_view.tab("Top Students by Skill"))
        
    # --- Helper to Fetch List of Skills ---
    def _fetch_skills(self):
        """Fetches all skill names for the combobox."""
        headers, data = fetch_table_data(self.conn, 'Skill')
        return [row[1] for row in data] if data else ["No Skills Found"]

    # --- Setup Tab: GetTopStudentsBySkill Procedure ---
    def _setup_top_students_tab(self, tab):
        control_frame = ctk.CTkFrame(tab, fg_color="transparent")
        control_frame.pack(pady=10, padx=10, fill='x')

        ctk.CTkLabel(control_frame, text="Select Skill:").pack(side=ctk.LEFT, padx=10)
        
        self.skill_names = self._fetch_skills()
        self.skill_var = ctk.StringVar(value=self.skill_names[0])
        
        self.skill_selector = ctk.CTkComboBox(control_frame, variable=self.skill_var, values=self.skill_names, 
                                            state="readonly", width=250)
        self.skill_selector.pack(side=ctk.LEFT, padx=10)
        
        ctk.CTkButton(control_frame, text="Run Report", command=self._run_top_students_procedure,
                      fg_color="#00AEEF", hover_color="#0080B0").pack(side=ctk.LEFT, padx=10)

    # --- Setup Results Display ---
    def _setup_results_display(self, tab):
        # Styled Treeview for results (reusing style from modules.py)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#3A465A", foreground="white", rowheight=25, fieldbackground="#3A465A")
        style.map('Treeview', background=[('selected', '#00AEEF')])
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#4A566A", foreground="white")
        
        self.tree = ttk.Treeview(tab)
        self.tree.pack(padx=10, pady=(0, 10), fill='both', expand=True)

    # --- Execution: GetTopStudentsBySkill Procedure ---
    def _run_top_students_procedure(self):
        """Executes the GetTopStudentsBySkill stored procedure."""
        skill_name = self.skill_var.get()
        self.tree.delete(*self.tree.get_children())
        self.tree.configure(columns=()) 
        
        cursor = self.conn.cursor()
        try:
            # EXECUTE THE STORED PROCEDURE
            cursor.callproc('GetTopStudentsBySkill', (skill_name,))
            
            # Fetch the result set
            result_data = None
            headers = []
            for result in cursor.stored_results():
                result_data = result.fetchall()
                headers = [i[0] for i in result.description]
                break
                
            if result_data and headers:
                # Configure and populate the Treeview
                self.tree["columns"] = headers
                self.tree["show"] = "headings"
                for col in headers:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=120, stretch=True) 
                
                for row in result_data:
                    self.tree.insert("", ctk.END, values=row)
            else:
                messagebox.showinfo("Report", f"No students found with the skill: {skill_name}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error running procedure: {err}")
        finally:
            cursor.close()