from src.course import Course
from src.person import Person


class Teacher(Person):
    def __init__(self, teacher_id: int, name: str, email: str, department: str):
        super().__init__(name, email)
        self.teacher_id = teacher_id
        self.department = department

    def get_info(self):
        return f"Teacher ID: {self.teacher_id}---Teacher name: {self.name}"
