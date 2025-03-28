from typing import List

from src.course import Course


class Department:
    def __init__(self, department_id: int, department_name: str, location: str) -> None:
        self.department_id = department_id
        self.department_name = department_name
        self.location = location
        self.courses: List[Course] = []

    def add_course(self, course: Course) -> None:
        self.courses.append(course)

    def remove_course(self, course_id: int) -> str:
        for course in self.courses:
            if course_id == course.course_id:
                self.courses.remove(course)
                return f"Course ID: {course_id} removed"
        return f"Course not found"

    def __repr__(self):
        return f"Department(department_id={self.department_id!r}, department_name={self.department_name!r})"
