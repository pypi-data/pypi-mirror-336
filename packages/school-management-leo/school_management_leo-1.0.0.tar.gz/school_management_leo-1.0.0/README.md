
```markdown
+----------------+         +----------------+        +----------------+
|    Student     |         |    Teacher     |        |     Course     |
+----------------+         +----------------+        +----------------+
| - studentID    |         | - teacherID    |        | - courseID     |
| - name         |         | - name         |        | - courseName   |
| - dob          |         | - dob          |        | - department   |
| - address      |         | - email        |        | - creditHours  |
| - email        |         | - department   |        +----------------+
+----------------+         +----------------+        | + addStudent() |
| + enroll()     |         | + assignGrade()|        | + removeStudent()|
| + dropCourse() |         | + createCourse()|       +----------------+
| + viewGrades() |         +----------------+
+----------------+         +----------------+
        |                       | 1..*  
        |                       | 
        |1                      | 
        |                       | 
        V                       V
  +----------------+     +------------------+
  |   Department  |     |   Classroom      |
  +----------------+     +------------------+
  | - departmentID |     | - roomNumber     |
  | - departmentName|     | - capacity       |
  | - location     |     +------------------+
  +----------------+     | + assignCourse() |
  | + addCourse()  |     | + removeCourse() |
  | + removeCourse()|     +------------------+
  +----------------+      
```