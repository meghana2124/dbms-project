-- ----------------------------------------------------
-- Test Script for student_skill_portfolio
-- ----------------------------------------------------
USE student_skill_portfolio;
SET SQL_SAFE_UPDATES = 0;

-- ----------------------------------------------------
-- Part 1: Testing Triggers
-- ----------------------------------------------------
SELECT '-- 1. TESTING TRIGGERS...' AS 'Test Section';

-- Test Trigger 1: before_student_insert (Validate age)
SELECT '-- Testing Trigger 1: before_student_insert (Age Validation)' AS 'Test';
-- This should FAIL (age < 16)
INSERT INTO Student (first_name, last_name, dob) 
VALUES ('Too', 'Young', '2015-01-01');

-- This should FAIL (age > 35)
INSERT INTO Student (first_name, last_name, dob) 
VALUES ('Too', 'Old', '1980-01-01');

-- This should SUCCEED
INSERT INTO Student (first_name, last_name, dob) 
VALUES ('Just', 'Right', '2004-01-01');
SELECT * FROM Student WHERE first_name = 'Just';

-- Test Trigger 2: before_student_cgpa_update (Validate CGPA)
SELECT '-- Testing Trigger 2: before_student_cgpa_update (CGPA Validation)' AS 'Test';
-- This should FAIL (CGPA > 10)
UPDATE Student SET cgpa = 11.0 WHERE student_id = 1;

-- This should FAIL (CGPA < 0)
UPDATE Student SET cgpa = -1.0 WHERE student_id = 1;

-- This should SUCCEED
UPDATE Student SET cgpa = 8.6 WHERE student_id = 1;
SELECT student_id, first_name, cgpa FROM Student WHERE student_id = 1;
-- (Resetting for consistency in other tests)
UPDATE Student SET cgpa = 8.5 WHERE student_id = 1; 

-- Test Trigger 3: before_application_insert (Prevent duplicates)
SELECT '-- Testing Trigger 3: before_application_insert (Duplicate Application)' AS 'Test';
-- Student 1 already applied to Job 1 (Status: Accepted).
-- This should FAIL (Duplicate application)
INSERT INTO application (app_date, status, student_id, job_id) 
VALUES (CURDATE(), 'Pending', 1, 1);

-- Student 3 applied to Job 1 (Status: Rejected).
-- This should SUCCEED (Can re-apply if rejected)
INSERT INTO application (app_date, status, student_id, job_id) 
VALUES (CURDATE(), 'Pending', 3, 1);
SELECT * FROM application WHERE student_id = 3;


-- Test Trigger 4: after_application_status_update (Audit Log)
SELECT '-- Testing Trigger 4: after_application_status_update (Audit Log)' AS 'Test';
SELECT 'Before update:' AS 'Info';
SELECT * FROM application WHERE app_id = 2;
SELECT * FROM application_audit;

-- Update status to fire trigger
UPDATE application SET status = 'Rejected' WHERE app_id = 2; -- Was 'Under Review'

SELECT 'After update:' AS 'Info';
SELECT * FROM application WHERE app_id = 2;
-- Check the audit table
SELECT * FROM application_audit WHERE app_id = 2;

-- Test Triggers 5 & 6: Activity Log (Skills & Courses)
SELECT '-- Testing Triggers 5 & 6: student_activity_log (Skills & Courses)' AS 'Test';
SELECT 'Before inserts:' AS 'Info';
SELECT * FROM student_activity_log WHERE student_id IN (1, 2);

-- Fire Trigger 5 (Skill Added)
INSERT INTO student_skill (student_id, skill_id) VALUES (1, 5); -- Student 1 adds 'Communication'

-- Fire Trigger 6 (Course Completed)
INSERT INTO student_course (student_id, course_id) VALUES (2, 4); -- Student 2 adds 'Cloud Computing'

SELECT 'After inserts:' AS 'Info';
SELECT * FROM student_activity_log WHERE student_id IN (1, 2);

-- Test Trigger 7: after_application_update_stats (Placement Stats)
SELECT '-- Testing Trigger 7: after_application_update_stats (Placement Stats)' AS 'Test';
-- Note: This table is empty after DML, it only populates on UPDATE
SELECT 'Before update:' AS 'Info';
SELECT * FROM placement_statistics;

-- Job 3 (app_id 3) is for Company 2. Status 'Pending' -> 'Accepted'
UPDATE application SET status = 'Accepted' WHERE app_id = 3; 

-- Job 2 (app_id 2) is for Company 3. We changed it to 'Rejected'
-- Let's update it again to test. Status 'Rejected' -> 'Under Review'
UPDATE application SET status = 'Under Review' WHERE app_id = 2;

-- Job 1 (app_id 1) is for Company 1. Status 'Accepted' -> 'Accepted' (no change, but should still run)
UPDATE application SET status = 'Accepted' WHERE app_id = 1; 

SELECT 'After updates:' AS 'Info';
-- Should show stats for Companies 1, 2, and 3
SELECT * FROM placement_statistics;


-- ----------------------------------------------------
-- Part 2: Testing Stored Procedures
-- ----------------------------------------------------
SELECT '-- 2. TESTING STORED PROCEDURES...' AS 'Test Section';

-- Test Procedure 1: GetStudentProfile
SELECT '-- Testing Procedure 1: GetStudentProfile(1)' AS 'Test';
CALL GetStudentProfile(1); -- Rahul Sharma

SELECT '-- Testing Procedure 1: GetStudentProfile(4)' AS 'Test';
CALL GetStudentProfile(4); -- Sneha Verma

-- Test Procedure 2: CalculateSkillMatch
SELECT '-- Testing Procedure 2: CalculateSkillMatch' AS 'Test';
-- Student 1 (Skills: 1,2,4,7) for Job 2 (Skills: 1,2,4) -> 3/3 = 100%
CALL CalculateSkillMatch(1, 2, @match_pct_1);
SELECT @match_pct_1 AS 'Student 1 / Job 2 Match (Should be 100.00)';

-- Student 3 (Skills: 3,5) for Job 1 (Skills: 1,3,7) -> 1/3 = 33.33%
CALL CalculateSkillMatch(3, 1, @match_pct_2);
SELECT @match_pct_2 AS 'Student 3 / Job 1 Match (Should be 33.33)';

-- Test Procedure 3: RecommendJobs
SELECT '-- Testing Procedure 3: RecommendJobs(1)' AS 'Test';
CALL RecommendJobs(1); -- For Rahul

SELECT '-- Testing Procedure 3: RecommendJobs(3)' AS 'Test';
CALL RecommendJobs(3); -- For Amit

-- Test Procedure 4: GetPlacementAnalytics
SELECT '-- Testing Procedure 4: GetPlacementAnalytics' AS 'Test';
CALL GetPlacementAnalytics('2025-01-01', '2025-12-31');

-- Test Procedure 5: FindEligibleStudents
SELECT '-- Testing Procedure 5: FindEligibleStudents(2)' AS 'Test';
CALL FindEligibleStudents(2); -- For 'Data Scientist'

SELECT '-- Testing Procedure 5: FindEligibleStudents(5)' AS 'Test';
CALL FindEligibleStudents(5); -- For 'Backend Developer'


-- ----------------------------------------------------
-- Part 3: Testing Functions
-- ----------------------------------------------------
SELECT '-- 3. TESTING FUNCTIONS...' AS 'Test Section';

-- Test Function 1: CalculateAge
SELECT '-- Testing Function 1: CalculateAge' AS 'Test';
SELECT dob, CalculateAge(dob) AS age FROM Student WHERE student_id = 1; -- Rahul (2003-05-15)

-- Test Function 2: GetStudentSkillCount
SELECT '-- Testing Function 2: GetStudentSkillCount' AS 'Test';
-- Student 1 (Rahul) has 4 skills + 1 we added = 5
SELECT GetStudentSkillCount(1) AS 'Rahul Skill Count (Should be 5)';
-- Student 2 (Priya) has 2 skills
SELECT GetStudentSkillCount(2) AS 'Priya Skill Count (Should be 2)';

-- Test Function 3: GetStudentProjectCount
SELECT '-- Testing Function 3: GetStudentProjectCount' AS 'Test';
SELECT GetStudentProjectCount(1) AS 'Rahul Project Count (Should be 3)';
SELECT GetStudentProjectCount(4) AS 'Sneha Project Count (Should be 2)';

-- Test Function 4: CheckCGPAEligibility
SELECT '-- Testing Function 4: CheckCGPAEligibility' AS 'Test';
-- Rahul (8.5) vs Min 8.0 -> 1 (TRUE)
SELECT CheckCGPAEligibility(1, 8.0) AS 'Rahul vs 8.0 (Should be 1)';
-- Amit (7.8) vs Min 8.0 -> 0 (FALSE)
SELECT CheckCGPAEligibility(3, 8.0) AS 'Amit vs 8.0 (Should be 0)';

-- Test Function 5: GetStudentSuccessRate
SELECT '-- Testing Function 5: GetStudentSuccessRate' AS 'Test';
-- Student 1: Apps: Job 1 (Accepted), Job 2 (Under Review). 1/2 = 50.00
SELECT GetStudentSuccessRate(1) AS 'Rahul Success Rate (Should be 50.00)';
-- Student 4: Apps: Job 2 (Accepted). 1/1 = 100.00
SELECT GetStudentSuccessRate(4) AS 'Sneha Success Rate (Should be 100.00)';
-- Student 3: Apps: Job 1 (Rejected), Job 1 (Pending). 0/2 = 0.00
SELECT GetStudentSuccessRate(3) AS 'Amit Success Rate (Should be 0.00)';

-- Test Function 6: GetMostDemandedSkill
SELECT '-- Testing Function 6: GetMostDemandedSkill' AS 'Test';
-- Python (ID 1) is required by 5 jobs
SELECT GetMostDemandedSkill() AS 'Most Demanded Skill (Should be Python)';

SELECT '-- ALL TESTS COMPLETE --' AS 'Status';

SET SQL_SAFE_UPDATES = 1;