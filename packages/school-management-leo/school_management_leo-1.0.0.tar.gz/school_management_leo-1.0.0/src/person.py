from abc import ABC, abstractmethod


class Person:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email

    @abstractmethod
    def get_info(self) -> str:
        pass
