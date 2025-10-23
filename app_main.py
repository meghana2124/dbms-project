import customtkinter as ctk
import sys

# Import components from other files
try:
    from db_connector import create_db_connection
    # from modules import StudentModule, PlacementModule 
    # # Placeholder imports for future modules
    # from modules import ProjectSkillModule, ApplicationModule
    from student_mod import StudentModule
    from placement_mod import PlacementModule
    from project_skill_mod import ProjectSkillModule
    from application_mod import ApplicationModule
except ImportError as e:
    print(f"Error importing modules: {e}. Check if db_connector.py and modules.py exist.")
    sys.exit()

# --------------------------------------------------------------------------------
# --- Main Application Class (Structure and Navigation) ---
# --------------------------------------------------------------------------------

class PortfolioManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- Theme Setup (Matching the Dark/Cyan UI Kit) ---
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue") 
        
        self.title("Student Portfolio Manager - Dark Theme")
        self.geometry("1200x750")
        self.minsize(1000, 600)

        # Database Connection
        self.conn = create_db_connection()
        if not self.conn:
            sys.exit() # Exit if database connection fails

        # Dictionary to hold module classes for easy switching
        self.modules = {
            "Student Management": StudentModule,
            "Placement & Hiring": PlacementModule,
            "Project & Skill Catalog": ProjectSkillModule,
            "Application Tracking": ApplicationModule
        }
        self.current_frame = None
        self.nav_buttons = {} 

        # --- Grid Configuration ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- A. Sidebar (Navigation) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1F2837")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(len(self.modules) + 2, weight=1)

        # App Logo/Title
        ctk.CTkLabel(self.sidebar_frame, text="🎓 PORTFOLIO MANAGER", 
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#00AEEF").pack(pady=(20, 10))
        ctk.CTkLabel(self.sidebar_frame, text="Database CRUD & Analytics", 
                     font=ctk.CTkFont(size=12),
                     text_color="gray").pack(pady=(0, 20))
        
        # Navigation Buttons
        for i, (title, module) in enumerate(self.modules.items()):
            button = ctk.CTkButton(self.sidebar_frame, 
                                   text=title,
                                   command=lambda t=title: self.switch_module(t),
                                   fg_color="transparent",
                                   hover_color="#3A465A",
                                   text_color="white",
                                   anchor="w")
            button.pack(fill='x', padx=15, pady=5)
            self.nav_buttons[title] = button 

        # Exit Button
        ctk.CTkButton(self.sidebar_frame, 
                      text="Exit Application", 
                      command=self.on_closing,
                      fg_color="#A33A3A",
                      hover_color="#802A2A").pack(fill='x', padx=15, pady=(20, 15), ipady=5)


        # --- C. Main Content Area ---
        self.main_area = ctk.CTkFrame(self, fg_color="#212834")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Load the initial module
        self.switch_module("Student Management")

    def switch_module(self, title):
        """Destroys the current frame and loads the selected module."""
        
        if self.current_frame:
            self.current_frame.destroy()
        
        # Visual Feedback
        for name, button in self.nav_buttons.items():
            if name == title:
                button.configure(fg_color="#00AEEF", hover_color="#00AEEF", text_color="black")
            else:
                button.configure(fg_color="transparent", hover_color="#3A465A", text_color="white")
        
        # Instantiate and Pack the new frame
        ModuleClass = self.modules[title]
        self.current_frame = ModuleClass(self.main_area, self.conn)
        self.current_frame.pack(fill='both', expand=True)

    def on_closing(self):
        """Handle closing the application and database connection."""
        if self.conn and self.conn.is_connected():
            self.conn.close()
        self.destroy() # Use destroy() instead of quit() in CTk

if __name__ == "__main__":
    app = PortfolioManagerApp()
    app.mainloop()