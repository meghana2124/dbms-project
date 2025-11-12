-- Create Database
CREATE DATABASE IF NOT EXISTS student_skill_portfolio;
USE student_skill_portfolio;

-- Table: Student
CREATE TABLE Student (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    s_phone VARCHAR(15),
    degree VARCHAR(100),
    branch VARCHAR(100),
    cgpa DECIMAL(3, 2) CHECK (cgpa >= 0.00 AND cgpa <= 10.00),
    resume_link VARCHAR(255),
    dob DATE
);

-- Table: studentEmail
CREATE TABLE studentEmail (
    student_id INT,
    s_email VARCHAR(100),
    PRIMARY KEY (student_id, s_email),
    FOREIGN KEY (student_id) REFERENCES Student(student_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Table: Skill
CREATE TABLE Skill (
    skill_id INT PRIMARY KEY AUTO_INCREMENT,
    skill_name VARCHAR(100) NOT NULL UNIQUE,
    skill_type VARCHAR(50) NOT NULL
);

-- Table: Course
CREATE TABLE Course (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(150) NOT NULL,
    provider VARCHAR(100),
    certification_link VARCHAR(255)
);


CREATE TABLE Project (
    project_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completion_date DATE,
    github_link VARCHAR(255),
    student_id INT NOT NULL,
     -- Composite Primary Key (PK of Student + Discriminator)
    PRIMARY KEY (student_id, project_id), 
    FOREIGN KEY (student_id) REFERENCES Student(student_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Table: Company
CREATE TABLE Company (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(150) NOT NULL UNIQUE,
    industry VARCHAR(100),
    location VARCHAR(150)
);

-- Table: PlacementOfficer
CREATE TABLE PlacementOfficer (
    officer_id INT PRIMARY KEY AUTO_INCREMENT,
    p_name VARCHAR(100) NOT NULL,
    p_phone VARCHAR(15)
);

-- Table: placementOfficerEmail
CREATE TABLE placementOfficerEmail (
    officer_id INT,
    p_email VARCHAR(100),
    PRIMARY KEY (officer_id, p_email),
    FOREIGN KEY (officer_id) REFERENCES PlacementOfficer(officer_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Table: Recruiter
CREATE TABLE Recruiter (
    recruiter_id INT PRIMARY KEY AUTO_INCREMENT,
    r_name VARCHAR(100) NOT NULL,
    designation VARCHAR(100),
    company_id INT,
    FOREIGN KEY (company_id) REFERENCES Company(company_id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE
);

-- Table: recruiterEmail
CREATE TABLE recruiterEmail (
    recruiter_id INT,
    r_email VARCHAR(100),
    PRIMARY KEY (recruiter_id, r_email),
    FOREIGN KEY (recruiter_id) REFERENCES Recruiter(recruiter_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Table: JobRole (recruiter_id FK already handles 1:m from Recruiter)
CREATE TABLE JobRole (
    job_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    eligibility_criteria TEXT,
    company_id INT,
    officer_id INT,
    recruiter_id INT,
    FOREIGN KEY (company_id) REFERENCES Company(company_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (officer_id) REFERENCES PlacementOfficer(officer_id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    FOREIGN KEY (recruiter_id) REFERENCES Recruiter(recruiter_id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE
);

-- Table: application
CREATE TABLE application (
    app_id INT PRIMARY KEY AUTO_INCREMENT,
    app_date DATE NOT NULL,
    status VARCHAR(50) CHECK (status IN ('Pending', 'Accepted', 'Rejected', 'Under Review')),
    student_id INT,
    job_id INT,
    FOREIGN KEY (student_id) REFERENCES Student(student_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (job_id) REFERENCES JobRole(job_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Relationship Table: student-skill (Many-to-Many)
CREATE TABLE student_skill (
    student_id INT,
    skill_id INT,
    PRIMARY KEY (student_id, skill_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES Skill(skill_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Relationship Table: student-course (Many-to-Many)
CREATE TABLE student_course (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Course(course_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Relationship Table: jobrole-skill (Many-to-Many)
CREATE TABLE jobrole_skill (
    job_id INT,
    skill_id INT,
    PRIMARY KEY (job_id, skill_id),
    FOREIGN KEY (job_id) REFERENCES JobRole(job_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES Skill(skill_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);
