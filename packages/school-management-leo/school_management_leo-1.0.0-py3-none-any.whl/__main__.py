from typing import List

from src.course import Course
from src.department import Department
from src.student import Student
from src.teacher import Teacher

courses: List[Course] = []

alex = Teacher(1, "Alex", "alex@gmail.com", "001")
anna = Teacher(2, "Anna", "anna@gmail.com", "002")

john = Student(1, "John", "john@gmail.com")
elise = Student(2, "Elise", "elise@gmail.com")


math = Course(1, "Math", "001", 8)
literature = Course(2, "Literature", "002", 9)

department1 = Department(1, "001", "HN")
department2 = Department(2, "002", "HN")

courses.append(math)
courses.append(literature)

department1.add_course(math)
department2.add_course(literature)

john.enroll(math)
elise.enroll(literature)

print(courses)
print(department1)
print(department2)
print(john)
print(elise)
