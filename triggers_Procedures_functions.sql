
USE student_skill_portfolio;
-- Insert Students
INSERT INTO Student (first_name, last_name, s_phone, degree, branch, cgpa, resume_link, dob) 
VALUES 
    ('Rahul', 'Sharma', '9876543210', 'B.Tech', 'Computer Science', 8.5, 'https://resume.com/rahul', '2003-05-15'),
    ('Priya', 'Singh', '9876543211', 'B.Tech', 'Electronics', 8.2, 'https://resume.com/priya', '2003-08-22'),
    ('Amit', 'Kumar', '9876543212', 'B.Tech', 'Mechanical', 7.8, 'https://resume.com/amit', '2003-11-10'),
    ('Sneha', 'Verma', '9876543213', 'B.Tech', 'Computer Science', 9.0, 'https://resume.com/sneha', '2003-02-28');
select * from student;
desc student;
-- Insert Student Emails
INSERT INTO studentEmail (student_id, s_email) 
VALUES 
    (1, 'rahul.sharma@college.edu'),
    (1, 'rahul@gmail.com'),
    (2, 'priya.singh@college.edu'),
    (3, 'amit.kumar@college.edu'),
    (4, 'sneha.verma@college.edu');
select * from studentEmail;
-- Insert Skills
INSERT INTO Skill (skill_name, skill_type) 
VALUES 
    ('Python', 'Programming'),
    ('Machine Learning', 'Technical'),
    ('Java', 'Programming'),
    ('SQL', 'Database'),
    ('Communication', 'Soft Skill'),
    ('Leadership', 'Soft Skill'),
    ('Data Structures', 'Technical'),
    ('Web Development', 'Technical');
select * from skill;

-- Insert Courses
INSERT INTO Course (course_name, provider, certification_link) 
VALUES 
    ('Machine Learning Specialization', 'Coursera', 'https://coursera.org/ml-cert'),
    ('Full Stack Development', 'Udemy', 'https://udemy.com/fullstack-cert'),
    ('Data Science Bootcamp', 'edX', 'https://edx.org/datascience-cert'),
    ('Cloud Computing Fundamentals', 'AWS', 'https://aws.amazon.com/cert');
select * from course;

-- Insert Projects (Modified - now includes student_id)
INSERT INTO Project (project_id, title, description, completion_date, github_link, student_id)
VALUES
    (1, 'CRISPR AI Tool', 'AI-powered tool for predicting safe gene edit locations', '2025-08-15', 'https://github.com/user/crispr-ai', 1),
    (2, 'Sustainability Scoring System', 'Product sustainability scoring using LCA databases', '2025-10-01', 'https://github.com/user/sustainability', 1),
    (3, 'E-commerce Web App', 'Full-stack e-commerce platform with payment integration', '2025-06-20', 'https://github.com/user/ecommerce', 2),
    (4, 'Cognitive Load Monitor', 'Webcam-based cognitive load monitoring system', '2025-09-30', 'https://github.com/user/cognitive-load', 4),
    (5, 'LeetCode Solutions Repository', 'Collection of optimized solutions to coding problems', '2025-07-10', 'https://github.com/user/leetcode', 1),
    (6, 'Mobile Banking App', 'Secure mobile banking application with biometric authentication', '2025-05-15', 'https://github.com/user/banking', 4);
select * from Project;

-- Insert Companies
INSERT INTO Company (company_name, industry, location) 
VALUES 
    ('Tech Solutions Inc', 'IT Services', 'Bangalore'),
    ('Innovation Labs', 'Software Development', 'Hyderabad'),
    ('Data Analytics Corp', 'Data Science', 'Pune'),
    ('Cloud Systems Ltd', 'Cloud Computing', 'Mumbai');
select * from Company;

-- Insert Placement Officers
INSERT INTO PlacementOfficer (p_name, p_phone) 
VALUES 
    ('Dr. Anil Gupta', '9876501234'),
    ('Ms. Meera Reddy', '9876501235');
select * from PlacementOfficer;

-- Insert Placement Officer Emails
INSERT INTO placementOfficerEmail (officer_id, p_email) 
VALUES 
    (1, 'anil.gupta@college.edu'),
    (2, 'meera.reddy@college.edu');
select * from placementOfficerEmail;

-- Insert Recruiters
INSERT INTO Recruiter (r_name, designation, company_id) 
VALUES 
    ('Vikram Malhotra', 'HR Manager', 1),
    ('Anita Desai', 'Technical Recruiter', 2),
    ('Rajesh Patel', 'Talent Acquisition Lead', 3);
select * from Recruiter;

-- Insert Recruiter Emails
INSERT INTO recruiterEmail (recruiter_id, r_email) 
VALUES 
    (1, 'vikram@techsolutions.com'),
    (2, 'anita@innovationlabs.com'),
    (3, 'rajesh@dataanalytics.com');
select * from RecruiterEmail;

-- Insert Job Roles (recruiter_id FK handles 1:m relationship)
INSERT INTO JobRole (title, description, eligibility_criteria, company_id, officer_id, recruiter_id) 
VALUES 
    ('Software Engineer', 'Develop and maintain software applications', 'CGPA > 7.5, Knowledge of Python/Java', 1, 1, 1),
    ('Data Scientist', 'Analyze data and build ML models', 'CGPA > 8.0, ML and Python skills required', 3, 1, 3),
    ('Full Stack Developer', 'Build complete web applications', 'Web development experience required', 2, 2, 2),
    ('Cloud Engineer', 'Design and maintain cloud infrastructure', 'Cloud computing knowledge required', 4, 1, NULL),
    ('Backend Developer', 'Build scalable backend systems', 'CGPA > 7.0, Java/Python expertise', 1, 1, 1);
select * from jobRole;

-- Link Students with Skills
INSERT INTO student_skill (student_id, skill_id) 
VALUES 
    (1, 1), (1, 2), (1, 4), (1, 7),
    (2, 1), (2, 8),
    (3, 3), (3, 5),
    (4, 1), (4, 2), (4, 7), (4, 8);
select * from student_skill;

-- Link Students with Courses
INSERT INTO student_course (student_id, course_id) 
VALUES 
    (1, 1), (1, 3),
    (2, 2),
    (4, 1), (4, 2);
select * from student_course;

-- Link Job Roles with Skills
INSERT INTO jobrole_skill (job_id, skill_id) 
VALUES 
    (1, 1), (1, 3), (1, 7),
    (2, 1), (2, 2), (2, 4),
    (3, 8), (3, 1),
    (4, 1),
    (5, 1), (5, 3);
select * from jobrole_skill;



-- Insert Applications
INSERT INTO application (app_date, status, student_id, job_id) 
VALUES 
    ('2025-09-01', 'Accepted', 1, 1),
    ('2025-09-05', 'Under Review', 1, 2),
    ('2025-09-10', 'Pending', 2, 3),
    ('2025-09-15', 'Accepted', 4, 2),
    ('2025-09-20', 'Rejected', 3, 1);
select * from application;

show tables;

-- Triggers
-- Data Integrity and Validation
-- Trigger 1: Validate student age before insertion
DELIMITER //
CREATE TRIGGER before_student_insert
BEFORE INSERT ON Student
FOR EACH ROW
BEGIN
    DECLARE student_age INT;
    SET student_age = TIMESTAMPDIFF(YEAR, NEW.dob, CURDATE());
    
    IF student_age < 16 OR student_age > 35 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Student age must be between 16 and 35 years';
    END IF;
END//
DELIMITER ;

-- Trigger 2: Validate CGPA on update
DELIMITER //
CREATE TRIGGER before_student_cgpa_update
BEFORE UPDATE ON Student
FOR EACH ROW
BEGIN
    IF NEW.cgpa < 0 OR NEW.cgpa > 10 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'CGPA must be between 0 and 10';
    END IF;
END//
DELIMITER ;

-- Trigger 3: Prevent duplicate applications
DELIMITER //
CREATE TRIGGER before_application_insert
BEFORE INSERT ON application
FOR EACH ROW
BEGIN
    DECLARE app_count INT;
    
    SELECT COUNT(*) INTO app_count
    FROM application
    WHERE student_id = NEW.student_id 
    AND job_id = NEW.job_id
    AND status != 'Rejected';
    
    IF app_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Student has already applied for this job';
    END IF;
END//
DELIMITER ;

-- Audit and Logging
-- Create audit table for application status changes
CREATE TABLE application_audit (
    audit_id INT PRIMARY KEY AUTO_INCREMENT,
    app_id INT,
    student_id INT,
    job_id INT,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (app_id) REFERENCES application(app_id) ON DELETE CASCADE
);

-- Trigger 4: Log application status changes
DELIMITER //
CREATE TRIGGER after_application_status_update
AFTER UPDATE ON application
FOR EACH ROW
BEGIN
    IF OLD.status != NEW.status THEN
        INSERT INTO application_audit (app_id, student_id, job_id, old_status, new_status)
        VALUES (NEW.app_id, NEW.student_id, NEW.job_id, OLD.status, NEW.status);
    END IF;
END//
DELIMITER ;

-- Create student activity log
CREATE TABLE student_activity_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    activity_type VARCHAR(50),
    activity_description TEXT,
    activity_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE
);

-- Trigger 5: Log when students add new skills
DELIMITER //
CREATE TRIGGER after_student_skill_insert
AFTER INSERT ON student_skill
FOR EACH ROW
BEGIN
    DECLARE skill_name_val VARCHAR(100);
    
    SELECT skill_name INTO skill_name_val
    FROM Skill
    WHERE skill_id = NEW.skill_id;
    
    INSERT INTO student_activity_log (student_id, activity_type, activity_description)
    VALUES (NEW.student_id, 'Skill Added', CONCAT('Added skill: ', skill_name_val));
END//
DELIMITER ;

-- Trigger 6: Log when students complete courses
DELIMITER //
CREATE TRIGGER after_student_course_insert
AFTER INSERT ON student_course
FOR EACH ROW
BEGIN
    DECLARE course_name_val VARCHAR(150);
    
    SELECT course_name INTO course_name_val
    FROM Course
    WHERE course_id = NEW.course_id;
    
    INSERT INTO student_activity_log (student_id, activity_type, activity_description)
    VALUES (NEW.student_id, 'Course Completed', CONCAT('Completed course: ', course_name_val));
END//
DELIMITER ;

-- Automatic Calculations
-- Create placement statistics table
CREATE TABLE placement_statistics (
    stat_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    total_applications INT DEFAULT 0,
    accepted_applications INT DEFAULT 0,
    rejected_applications INT DEFAULT 0,
    pending_applications INT DEFAULT 0,
    acceptance_rate DECIMAL(5,2) DEFAULT 0.00,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES Company(company_id) ON DELETE CASCADE
);

-- Trigger 7: Update placement statistics when application status changes
DELIMITER //
CREATE TRIGGER after_application_update_stats
AFTER UPDATE ON application
FOR EACH ROW
BEGIN
    DECLARE comp_id INT;
    
    SELECT company_id INTO comp_id
    FROM JobRole
    WHERE job_id = NEW.job_id;
    
    -- Insert or update statistics
    INSERT INTO placement_statistics (company_id, total_applications)
    VALUES (comp_id, 1)
    ON DUPLICATE KEY UPDATE
        total_applications = (
            SELECT COUNT(*) FROM application a
            JOIN JobRole jr ON a.job_id = jr.job_id
            WHERE jr.company_id = comp_id
        ),
        accepted_applications = (
            SELECT COUNT(*) FROM application a
            JOIN JobRole jr ON a.job_id = jr.job_id
            WHERE jr.company_id = comp_id AND a.status = 'Accepted'
        ),
        rejected_applications = (
            SELECT COUNT(*) FROM application a
            JOIN JobRole jr ON a.job_id = jr.job_id
            WHERE jr.company_id = comp_id AND a.status = 'Rejected'
        ),
        pending_applications = (
            SELECT COUNT(*) FROM application a
            JOIN JobRole jr ON a.job_id = jr.job_id
            WHERE jr.company_id = comp_id AND a.status IN ('Pending', 'Under Review')
        ),
        acceptance_rate = (
            SELECT CASE 
                WHEN COUNT(*) > 0 THEN (SUM(CASE WHEN a.status = 'Accepted' THEN 1 ELSE 0 END) / COUNT(*)) * 100
                ELSE 0
            END
            FROM application a
            JOIN JobRole jr ON a.job_id = jr.job_id
            WHERE jr.company_id = comp_id
        );
END//
DELIMITER ;
-- Stored Procedures
-- Student Management
-- Procedure 1: Get student complete profile with skills and courses
DELIMITER //
CREATE PROCEDURE GetStudentProfile(IN p_student_id INT)
BEGIN
    -- Basic student info
    SELECT s.*, GROUP_CONCAT(DISTINCT se.s_email) as emails
    FROM Student s
    LEFT JOIN studentEmail se ON s.student_id = se.student_id
    WHERE s.student_id = p_student_id
    GROUP BY s.student_id;
    
    -- Student skills
    SELECT sk.skill_name, sk.skill_type
    FROM student_skill ss
    JOIN Skill sk ON ss.skill_id = sk.skill_id
    WHERE ss.student_id = p_student_id;
    
    -- Student courses
    SELECT c.course_name, c.provider, c.certification_link
    FROM student_course sc
    JOIN Course c ON sc.course_id = c.course_id
    WHERE sc.student_id = p_student_id;
    
    -- Student projects
    SELECT title, description, completion_date, github_link
    FROM Project
    WHERE student_id = p_student_id;
    
    -- Application history
    SELECT jr.title, c.company_name, a.app_date, a.status
    FROM application a
    JOIN JobRole jr ON a.job_id = jr.job_id
    JOIN Company c ON jr.company_id = c.company_id
    WHERE a.student_id = p_student_id
    ORDER BY a.app_date DESC;
END//
DELIMITER ;

-- Procedure 2: Calculate student skill match percentage for a job
DELIMITER //
CREATE PROCEDURE CalculateSkillMatch(
    IN p_student_id INT,
    IN p_job_id INT,
    OUT match_percentage DECIMAL(5,2)
)
BEGIN
    DECLARE total_required_skills INT;
    DECLARE matched_skills INT;
    
    -- Count total required skills for job
    SELECT COUNT(*) INTO total_required_skills
    FROM jobrole_skill
    WHERE job_id = p_job_id;
    
    -- Count how many the student has
    SELECT COUNT(*) INTO matched_skills
    FROM jobrole_skill jrs
    JOIN student_skill ss ON jrs.skill_id = ss.skill_id
    WHERE jrs.job_id = p_job_id AND ss.student_id = p_student_id;
    
    -- Calculate percentage
    IF total_required_skills > 0 THEN
        SET match_percentage = (matched_skills / total_required_skills) * 100;
    ELSE
        SET match_percentage = 0;
    END IF;
END//
DELIMITER ;

-- Job Recommendation and Placement Analytics
-- Procedure 3: Recommend jobs based on student skills and eligibility
DELIMITER //
CREATE PROCEDURE RecommendJobs(IN p_student_id INT)
BEGIN
    DECLARE student_cgpa DECIMAL(3,2);
    
    SELECT cgpa INTO student_cgpa
    FROM Student
    WHERE student_id = p_student_id;
    
    SELECT 
        jr.job_id,
        jr.title,
        c.company_name,
        c.industry,
        jr.eligibility_criteria,
        COUNT(DISTINCT jrs.skill_id) as total_skills_required,
        COUNT(DISTINCT ss.skill_id) as matching_skills,
        ROUND((COUNT(DISTINCT ss.skill_id) / COUNT(DISTINCT jrs.skill_id)) * 100, 2) as skill_match_percentage
    FROM JobRole jr
    JOIN Company c ON jr.company_id = c.company_id
    LEFT JOIN jobrole_skill jrs ON jr.job_id = jrs.job_id
    LEFT JOIN student_skill ss ON jrs.skill_id = ss.skill_id AND ss.student_id = p_student_id
    WHERE jr.job_id NOT IN (
        SELECT job_id FROM application 
        WHERE student_id = p_student_id AND status != 'Rejected'
    )
    GROUP BY jr.job_id, jr.title, c.company_name, c.industry, jr.eligibility_criteria
    HAVING skill_match_percentage >= 50
    ORDER BY skill_match_percentage DESC, total_skills_required ASC;
END//
DELIMITER ;

-- Procedure 4: Get placement analytics for a specific period
DELIMITER //
CREATE PROCEDURE GetPlacementAnalytics(
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    -- Overall statistics
    SELECT 
        COUNT(DISTINCT a.student_id) as total_students_applied,
        COUNT(DISTINCT CASE WHEN a.status = 'Accepted' THEN a.student_id END) as students_placed,
        COUNT(a.app_id) as total_applications,
        SUM(CASE WHEN a.status = 'Accepted' THEN 1 ELSE 0 END) as accepted_applications,
        SUM(CASE WHEN a.status = 'Rejected' THEN 1 ELSE 0 END) as rejected_applications,
        SUM(CASE WHEN a.status IN ('Pending', 'Under Review') THEN 1 ELSE 0 END) as pending_applications,
        ROUND(AVG(CASE WHEN a.status = 'Accepted' THEN s.cgpa END), 2) as avg_cgpa_placed_students
    FROM application a
    JOIN Student s ON a.student_id = s.student_id
    WHERE a.app_date BETWEEN start_date AND end_date;
    
    -- Company-wise breakdown
    SELECT 
        c.company_name,
        c.industry,
        COUNT(a.app_id) as total_applications,
        SUM(CASE WHEN a.status = 'Accepted' THEN 1 ELSE 0 END) as placements,
        ROUND((SUM(CASE WHEN a.status = 'Accepted' THEN 1 ELSE 0 END) / COUNT(a.app_id)) * 100, 2) as success_rate
    FROM application a
    JOIN JobRole jr ON a.job_id = jr.job_id
    JOIN Company c ON jr.company_id = c.company_id
    WHERE a.app_date BETWEEN start_date AND end_date
    GROUP BY c.company_id, c.company_name, c.industry
    ORDER BY placements DESC;
    
    -- Branch-wise placement statistics
    SELECT 
        s.branch,
        COUNT(DISTINCT a.student_id) as students_applied,
        COUNT(DISTINCT CASE WHEN a.status = 'Accepted' THEN a.student_id END) as students_placed,
        ROUND((COUNT(DISTINCT CASE WHEN a.status = 'Accepted' THEN a.student_id END) / 
               COUNT(DISTINCT a.student_id)) * 100, 2) as placement_percentage
    FROM application a
    JOIN Student s ON a.student_id = s.student_id
    WHERE a.app_date BETWEEN start_date AND end_date
    GROUP BY s.branch
    ORDER BY placement_percentage DESC;
END//
DELIMITER ;

-- Procedure 5: Find students eligible for a job


-- Functions
-- Function 1: Calculate student age
DELIMITER //
CREATE FUNCTION CalculateAge(birth_date DATE)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN TIMESTAMPDIFF(YEAR, birth_date, CURDATE());
END//
DELIMITER ;

-- Function 2: Get total skills count for a student
DELIMITER //
CREATE FUNCTION GetStudentSkillCount(p_student_id INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE skill_count INT;
    
    SELECT COUNT(*) INTO skill_count
    FROM student_skill
    WHERE student_id = p_student_id;
    
    RETURN skill_count;
END//
DELIMITER ;

-- Function 3: Get total projects count for a student
DELIMITER //
CREATE FUNCTION GetStudentProjectCount(p_student_id INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE project_count INT;
    
    SELECT COUNT(*) INTO project_count
    FROM Project
    WHERE student_id = p_student_id;
    
    RETURN project_count;
END//
DELIMITER ;

-- Function 4: Check if student meets job eligibility based on CGPA
DELIMITER //
CREATE FUNCTION CheckCGPAEligibility(p_student_id INT, min_cgpa DECIMAL(3,2))
RETURNS BOOLEAN
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE student_cgpa DECIMAL(3,2);
    
    SELECT cgpa INTO student_cgpa
    FROM Student
    WHERE student_id = p_student_id;
    
    RETURN student_cgpa >= min_cgpa;
END//
DELIMITER ;

-- Function 5: Get application success rate for a student
DELIMITER //
CREATE FUNCTION GetStudentSuccessRate(p_student_id INT)
RETURNS DECIMAL(5,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total_apps INT;
    DECLARE accepted_apps INT;
    DECLARE success_rate DECIMAL(5,2);
    
    SELECT COUNT(*) INTO total_apps
    FROM application
    WHERE student_id = p_student_id;
    
    SELECT COUNT(*) INTO accepted_apps
    FROM application
    WHERE student_id = p_student_id AND status = 'Accepted';
    
    IF total_apps > 0 THEN
        SET success_rate = (accepted_apps / total_apps) * 100;
    ELSE
        SET success_rate = 0;
    END IF;
    
    RETURN success_rate;
END//
DELIMITER ;

-- Function 6: Get most in-demand skill
DELIMITER //
CREATE FUNCTION GetMostDemandedSkill()
RETURNS VARCHAR(100)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE skill_name_val VARCHAR(100);
    
    SELECT s.skill_name INTO skill_name_val
    FROM Skill s
    JOIN jobrole_skill jrs ON s.skill_id = jrs.skill_id
    GROUP BY s.skill_id, s.skill_name
    ORDER BY COUNT(jrs.job_id) DESC
    LIMIT 1;
    
    RETURN skill_name_val;
END//
DELIMITER ;



DROP PROCEDURE IF EXISTS FindEligibleStudents; -- Drop old one first
DELIMITER //
CREATE PROCEDURE FindEligibleStudents(IN p_job_id INT)
BEGIN
    DECLARE total_required_skills INT;

    -- Get the total required skills for the job ONCE
    SELECT COUNT(*) INTO total_required_skills
    FROM jobrole_skill 
    WHERE job_id = p_job_id;

    SELECT 
        s.student_id,
        s.first_name,
        s.last_name,
        s.branch,
        s.cgpa,
        
        -- THE FIX IS HERE:
        -- Count jrs.skill_id, not ss.skill_id.
        -- jrs.skill_id will only be NOT NULL when a student's skill
        -- matches a required job skill, thanks to the LEFT JOIN.
        COUNT(DISTINCT jrs.skill_id) as matching_skills,
        
        total_required_skills as required_skills,
        
        ROUND((COUNT(DISTINCT jrs.skill_id) / 
               total_required_skills) * 100, 2) as skill_match_percentage
               
    FROM Student s
    LEFT JOIN student_skill ss ON s.student_id = ss.student_id
    LEFT JOIN jobrole_skill jrs ON ss.skill_id = jrs.skill_id AND jrs.job_id = p_job_id
    WHERE 
        s.student_id NOT IN (
            SELECT student_id FROM application 
            WHERE job_id = p_job_id AND status != 'Rejected'
        )
        AND total_required_skills > 0 -- Don't divide by zero
    GROUP BY s.student_id, s.first_name, s.last_name, s.branch, s.cgpa
    HAVING skill_match_percentage >= 40
    ORDER BY skill_match_percentage DESC, s.cgpa DESC;
END//

DELIMITER ;


-- ---
-- 1. Procedure to get a specific officer's "inbox" of pending applications
-- ---
DELIMITER //
CREATE PROCEDURE GetOfficerPendingApplications(IN p_officer_id INT)
BEGIN
    SELECT 
        a.app_id,
        s.first_name,
        s.last_name,
        jr.title AS job_title,
        a.app_date,
        a.status
    FROM application a
    JOIN Student s ON a.student_id = s.student_id
    JOIN JobRole jr ON a.job_id = jr.job_id
    WHERE 
        jr.officer_id = p_officer_id 
        AND a.status IN ('Pending', 'Under Review')
    ORDER BY a.app_date ASC;
END//
DELIMITER ;

-- ---
-- 2. Procedure to securely update an application's status
-- ---
DELIMITER //
CREATE PROCEDURE UpdateApplicationStatus(
    IN p_app_id INT,
    IN p_new_status VARCHAR(50)
)
BEGIN
    -- Check if the status is a valid one to set
    IF p_new_status NOT IN ('Accepted', 'Rejected', 'Under Review') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid status. Must be "Accepted", "Rejected", or "Under Review".';
    ELSE
        UPDATE application
        SET status = p_new_status
        WHERE app_id = p_app_id;
    END IF;
END//
DELIMITER ;

