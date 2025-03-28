from typing import List

from src.student import Student


class Course:
    def __init__(
        self, course_id: int, course_name: str, department: str, credit_hours: int
    ) -> None:
        self.course_id = course_id
        self.course_name = course_name
        self.department = department
        self.credit_hours = credit_hours
        self._grade: int
        self.students: List = []

    @property
    def grade(self) -> int:
        return self._grade

    @grade.setter
    def grade(self, value: int) -> None:
        if isinstance(value, int):
            raise ValueError("Grade must be integer")
        if value < 0 or value > 10:
            raise ValueError("Grade must be between 0 and 10")
        self._grade = value

    def add_student(self, student: Student) -> None:
        self.students.append(student)

    def remove_student(self, student_id: int) -> str:
        for student in self.students:
            if student_id == student.student_id:
                self.students.remove(student)
                return f"Student ID: {student_id} removed"
        return f"Student not found"

    def __repr__(self) -> str:
        return f"Course(course_id={self.course_id!r}, course_name={self.course_name!r})"
