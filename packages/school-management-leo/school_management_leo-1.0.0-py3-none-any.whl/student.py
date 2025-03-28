from typing import List

from src.person import Person


class Student(Person):
    def __init__(self, student_id: int, name: str, email: str):
        super().__init__(name, email)
        self.student_id = student_id
        self.courses: List = []

    def enroll(self, course) -> None:
        self.courses.append(course)

    def drop_course(self, course_id: int) -> str:
        for course in self.courses:
            if course_id == course.course_id:
                self.courses.remove(course)
                return f"Course ID: {course_id} removed"
        return f"Course not found"

    def view_grades(self) -> None:
        for course in self.courses:
            print(f"{course.course_name}: {course.grade}")

    def get_info(self) -> str:
        return f"Student ID: {self.student_id}---Student name: {self.name}"

    def __repr__(self):
        return f"Student(student_id={self.student_id!r}, name={self.name})"
