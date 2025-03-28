from typing import List

from course import Course


class Classroom:
    def __init__(self, room_number: int, capacity: int) -> None:
        self.room_number = room_number
        self.capacity = capacity
        self.courses: List[Course] = []

    def assign_course(self, course: Course) -> None:
        self.courses.append(course)

    def remove_course(self, course_id: int) -> str:
        for course in self.courses:
            if course_id == course.course_id:
                return f"Course ID: {course_id} removed"
        return f"Course not found"
