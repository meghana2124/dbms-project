# --- analytics_mod.py ---
import customtkinter as ctk
from tkinter import messagebox, ttk
import mysql.connector

# We'll use the generic fetcher from utils to populate our comboboxes
from utils import fetch_table_data 

class AnalyticsModule(ctk.CTkFrame):
    def __init__(self, master, conn):
        super().__init__(master, fg_color="#2B3649")
        self.conn = conn
        
        # --- 1. KPI Header (for GetMostDemandedSkill function) ---
        kpi_frame = ctk.CTkFrame(self, fg_color="#3A465A")
        kpi_frame.pack(pady=(20, 10), padx=20, fill='x')
        
        self.kpi_label = ctk.CTkLabel(kpi_frame, text="Most In-Demand Skill: Loading...", 
                                      font=ctk.CTkFont(size=16, weight="bold"),
                                      text_color="#00AEEF")
        self.kpi_label.pack(pady=10)
        self._run_kpi_function()

        # --- 2. Tab View for all Procedures ---
        self.tab_view = ctk.CTkTabview(self, fg_color="#3A465A", segmented_button_selected_color="#00AEEF")
        self.tab_view.pack(padx=20, pady=(0, 20), fill="both", expand=True)

        # Create a tab for each logical procedure
        self.tab_view.add("Find Candidates")      # FindEligibleStudents
        self.tab_view.add("Recommend Jobs")       # RecommendJobs
        self.tab_view.add("Student Profile")      # GetStudentProfile
        self.tab_view.add("Skill Match %")        # CalculateSkillMatch
        self.tab_view.add("Placement Analytics")  # GetPlacementAnalytics
        
        # Dictionaries to store student/job data for comboboxes
        self.student_map = {}
        self.job_map = {}
        
        # Setup each tab
        self._setup_find_candidates_tab(self.tab_view.tab("Find Candidates"))
        self._setup_recommend_jobs_tab(self.tab_view.tab("Recommend Jobs"))
        self._setup_student_profile_tab(self.tab_view.tab("Student Profile"))
        self._setup_skill_match_tab(self.tab_view.tab("Skill Match %"))
        self._setup_placement_analytics_tab(self.tab_view.tab("Placement Analytics"))
        
    # --- Data Fetching Helpers ---
    
    def _fetch_students(self):
        """Fetches 'id' and 'name' for student comboboxes."""
        _, data = fetch_table_data(self.conn, 'Student')
        self.student_map = {f"{row[1]} {row[2]} (ID: {row[0]})": row[0] for row in data}
        return list(self.student_map.keys())

    def _fetch_jobs(self):
        """Fetches 'id' and 'title' for job comboboxes."""
        _, data = fetch_table_data(self.conn, 'JobRole')
        self.job_map = {f"{row[1]} (ID: {row[0]})": row[0] for row in data}
        return list(self.job_map.keys())

    def _setup_treeview(self, parent_tab):
        """Creates a standardized, styled Treeview for results."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#3A465A", foreground="white", rowheight=25, fieldbackground="#3A465A")
        style.map('Treeview', background=[('selected', '#00AEEF')])
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#4A566A", foreground="white")
        
        tree = ttk.Treeview(parent_tab)
        tree.pack(padx=10, pady=(0, 10), fill='both', expand=True)
        return tree

    def _populate_treeview(self, tree, headers, data):
        """Helper to dynamically populate any treeview."""
        tree.delete(*tree.get_children())
        
        if not data or not headers:
            tree["columns"] = ("Message",)
            tree.heading("Message", text="No results found for this query.")
            tree.column("Message", anchor='center')
            return

        tree["columns"] = headers
        tree["show"] = "headings"
        for col in headers:
            tree.heading(col, text=col)
            tree.column(col, width=max(100, len(col) * 12), stretch=True) 
        
        for row in data:
            tree.insert("", ctk.END, values=row)

    def _run_procedure_to_tree(self, proc_name, params, tree_widget):
        """Generic handler for procedures that return one result set."""
        cursor = self.conn.cursor()
        try:
            cursor.callproc(proc_name, params)
            
            result_data = None
            headers = []
            for result in cursor.stored_results():
                result_data = result.fetchall()
                headers = [i[0] for i in result.description]
                break
                
            self._populate_treeview(tree_widget, headers, result_data)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error running procedure {proc_name}: {err}")
        finally:
            cursor.close()

    # --- Tab 1: Find Candidates (FindEligibleStudents) ---
    def _setup_find_candidates_tab(self, tab):
        control_frame = ctk.CTkFrame(tab, fg_color="transparent")
        control_frame.pack(pady=10, padx=10, fill='x')

        ctk.CTkLabel(control_frame, text="Select Job Role:").pack(side=ctk.LEFT, padx=10)
        
        job_names = self._fetch_jobs()
        job_var = ctk.StringVar(value=job_names[0] if job_names else "")
        
        job_selector = ctk.CTkComboBox(control_frame, variable=job_var, values=job_names, state="readonly", width=300)
        job_selector.pack(side=ctk.LEFT, padx=10)
        
        tree = self._setup_treeview(tab)

        ctk.CTkButton(control_frame, text="Find Candidates", 
                      command=lambda: self._run_find_candidates(job_var, tree),
                      fg_color="#00AEEF", hover_color="#0080B0").pack(side=ctk.LEFT, padx=10)

    def _run_find_candidates(self, job_var, tree):
        job_name = job_var.get()
        if not job_name:
            messagebox.showwarning("Input Error", "Please select a job.")
            return
        
        job_id = self.job_map.get(job_name)
        self._run_procedure_to_tree('FindEligibleStudents', (job_id,), tree)


    # --- Tab 2: Recommend Jobs (RecommendJobs) ---
    def _setup_recommend_jobs_tab(self, tab):
        control_frame = ctk.CTkFrame(tab, fg_color="transparent")
        control_frame.pack(pady=10, padx=10, fill='x')

        ctk.CTkLabel(control_frame, text="Select Student:").pack(side=ctk.LEFT, padx=10)
        
        student_names = self._fetch_students()
        student_var = ctk.StringVar(value=student_names[0] if student_names else "")
        
        student_selector = ctk.CTkComboBox(control_frame, variable=student_var, values=student_names, state="readonly", width=300)
        student_selector.pack(side=ctk.LEFT, padx=10)
        
        tree = self._setup_treeview(tab)

        ctk.CTkButton(control_frame, text="Recommend Jobs", 
                      command=lambda: self._run_recommend_jobs(student_var, tree),
                      fg_color="#00AEEF", hover_color="#0080B0").pack(side=ctk.LEFT, padx=10)

    def _run_recommend_jobs(self, student_var, tree):
        student_name = student_var.get()
        if not student_name:
            messagebox.showwarning("Input Error", "Please select a student.")
            return
        
        student_id = self.student_map.get(student_name)
        self._run_procedure_to_tree('RecommendJobs', (student_id,), tree)


    # --- Tab 3: Student Profile (GetStudentProfile) ---
    def _setup_student_profile_tab(self, tab):
        control_frame = ctk.CTkFrame(tab, fg_color="transparent")
        control_frame.pack(pady=10, padx=10, fill='x')

        ctk.CTkLabel(control_frame, text="Select Student:").pack(side=ctk.LEFT, padx=10)
        
        student_names = self._fetch_students()
        student_var = ctk.StringVar(value=student_names[0] if student_names else "")
        
        student_selector = ctk.CTkComboBox(control_frame, variable=student_var, values=student_names, state="readonly", width=300)
        student_selector.pack(side=ctk.LEFT, padx=10)
        
        # Using a Textbox for this report, as it has 5 parts
        self.profile_text = ctk.CTkTextbox(tab, font=("Consolas", 12), wrap="word")
        self.profile_text.pack(padx=10, pady=(0, 10), fill='both', expand=True)

        ctk.CTkButton(control_frame, text="Get Full Profile", 
                      command=lambda: self._run_student_profile(student_var),
                      fg_color="#00AEEF", hover_color="#0080B0").pack(side=ctk.LEFT, padx=10)

    def _run_student_profile(self, student_var):
        student_name = student_var.get()
        if not student_name:
            messagebox.showwarning("Input Error", "Please select a student.")
            return
        
        student_id = self.student_map.get(student_name)
        self.profile_text.delete("1.0", ctk.END)
        report = f"--- STUDENT PROFILE REPORT (ID: {student_id}) ---\n\n"
        
        cursor = self.conn.cursor()
        try:
            cursor.callproc('GetStudentProfile', (student_id,))
            
            result_titles = ["1. Basic Info", "2. Skills", "3. Courses", "4. Projects", "5. Application History"]
            
            for i, result in enumerate(cursor.stored_results()):
                title = result_titles[i]
                report += f"--- {title} ---\n"
                
                headers = [desc[0] for desc in result.description]
                data = result.fetchall()
                
                if not data:
                    report += " (No data found)\n\n"
                    continue
                
                # Format as a simple table
                report += f"{' | '.join(headers)}\n"
                report += "-" * (sum(len(h) for h in headers) + 3*len(headers)) + "\n"
                for row in data:
                    report += f"{' | '.join(str(item) for item in row)}\n"
                report += "\n"
            
            self.profile_text.insert("1.0", report)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error running procedure GetStudentProfile: {err}")
        finally:
            cursor.close()


    # --- Tab 4: Skill Match % (CalculateSkillMatch) ---
    def _setup_skill_match_tab(self, tab):
        control_frame = ctk.CTkFrame(tab, fg_color="transparent")
        control_frame.pack(pady=10, padx=10, fill='x')

        # Student Selector
        ctk.CTkLabel(control_frame, text="Student:").pack(side=ctk.LEFT, padx=(10,0))
        student_names = self._fetch_students()
        student_var = ctk.StringVar(value=student_names[0] if student_names else "")
        student_selector = ctk.CTkComboBox(control_frame, variable=student_var, values=student_names, state="readonly", width=250)
        student_selector.pack(side=ctk.LEFT, padx=(5,10))

        # Job Selector
        ctk.CTkLabel(control_frame, text="Job:").pack(side=ctk.LEFT, padx=(10,0))
        job_names = self._fetch_jobs()
        job_var = ctk.StringVar(value=job_names[0] if job_names else "")
        job_selector = ctk.CTkComboBox(control_frame, variable=job_var, values=job_names, state="readonly", width=250)
        job_selector.pack(side=ctk.LEFT, padx=(5,10))
        
        # Result Display
        result_label = ctk.CTkLabel(tab, text="Match Percentage: --%", font=ctk.CTkFont(size=20, weight="bold"))
        result_label.pack(pady=20, padx=20)
        
        ctk.CTkButton(control_frame, text="Calculate Match", 
                      command=lambda: self._run_skill_match(student_var, job_var, result_label),
                      fg_color="#00AEEF", hover_color="#0080B0").pack(side=ctk.LEFT, padx=10)

    def _run_skill_match(self, student_var, job_var, result_label):
            student_name = student_var.get()
            job_name = job_var.get()
            
            if not student_name or not job_name:
                messagebox.showwarning("Input Error", "Please select both a student and a job.")
                return

            student_id = self.student_map.get(student_name)
            job_id = self.job_map.get(job_name)
            
            cursor = self.conn.cursor()
            try:
                # --- THIS IS THE NEW, MORE ROBUST METHOD ---

                # 1. Call the procedure, assigning the OUT param to a session variable @p_match_pct
                #    We pass (student_id, job_id) as args to cursor.execute
                cursor.execute("CALL CalculateSkillMatch(%s, %s, @p_match_pct)", (student_id, job_id))
                
                # 2. Commit the call (ensures the procedure executes)
                self.conn.commit()

                # 3. Select the value from the session variable
                cursor.execute("SELECT @p_match_pct")
                
                # 4. Fetch the result
                result = cursor.fetchone()
                
                if result:
                    match_pct = result[0]
                    result_label.configure(text=f"Match Percentage: {match_pct}%")
                else:
                    result_label.configure(text="Match Percentage: Error")
                # --- END OF NEW METHOD ---

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error running procedure CalculateSkillMatch: {err}")
                self.conn.rollback() # Rollback on error
            finally:
                cursor.close()

    # --- Tab 5: Placement Analytics (GetPlacementAnalytics) ---
    def _setup_placement_analytics_tab(self, tab):
        control_frame = ctk.CTkFrame(tab, fg_color="transparent")
        control_frame.pack(pady=10, padx=10, fill='x')

        ctk.CTkLabel(control_frame, text="Start Date (YYYY-MM-DD):").pack(side=ctk.LEFT, padx=(10,0))
        start_date_entry = ctk.CTkEntry(control_frame, placeholder_text="2025-01-01")
        start_date_entry.pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkLabel(control_frame, text="End Date (YYYY-MM-DD):").pack(side=ctk.LEFT, padx=(10,0))
        end_date_entry = ctk.CTkEntry(control_frame, placeholder_text="2025-12-31")
        end_date_entry.pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(control_frame, text="Run Analytics", 
                      command=lambda: self._run_placement_analytics(start_date_entry, end_date_entry),
                      fg_color="#00AEEF", hover_color="#0080B0").pack(side=ctk.LEFT, padx=10)
        
        # This report has 3 parts, so we need 3 treeviews
        ctk.CTkLabel(tab, text="Overall Statistics", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10,0))
        self.tree_overall = self._setup_treeview(tab)
        
        ctk.CTkLabel(tab, text="Company Breakdown", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10,0))
        self.tree_company = self._setup_treeview(tab)
        
        ctk.CTkLabel(tab, text="Branch Breakdown", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10,0))
        self.tree_branch = self._setup_treeview(tab)

    def _run_placement_analytics(self, start_date_entry, end_date_entry):
        start_date = start_date_entry.get() or "2000-01-01"
        end_date = end_date_entry.get() or "2099-12-31"
        
        cursor = self.conn.cursor()
        try:
            cursor.callproc('GetPlacementAnalytics', (start_date, end_date))
            
            result_trees = [self.tree_overall, self.tree_company, self.tree_branch]
            
            for i, result in enumerate(cursor.stored_results()):
                headers = [desc[0] for desc in result.description]
                data = result.fetchall()
                if i < len(result_trees):
                    self._populate_treeview(result_trees[i], headers, data)
                    
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error running procedure GetPlacementAnalytics: {err}")
        finally:
            cursor.close()

    # --- KPI Function (GetMostDemandedSkill) ---
    def _run_kpi_function(self):
        """Executes the GetMostDemandedSkill function."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT GetMostDemandedSkill()")
            result = cursor.fetchone()
            if result and result[0]:
                self.kpi_label.configure(text=f"Most In-Demand Skill: {result[0]}")
            else:
                self.kpi_label.configure(text="Most In-Demand Skill: Not Found")
        except mysql.connector.Error as err:
            self.kpi_label.configure(text="Most In-Demand Skill: Error")
            print(f"Error running KPI function: {err}")
        finally:
            cursor.close()