class Teacher:
    counter: int = 0
    # class variable 1
    help_line_number: str = "0315-2968211"  # class variable 2

    def __init__(self, teacher_id: int, teacher_name: str) -> None:
        self.name: str = teacher_name
        self.teacher_id: int = teacher_id
        self.organisation_name: str = "PIAIC"
        Teacher.counter += 1  # with new object created, counter will be
        # incremented

    def speak(self, words: str) -> None:
        print(f"Teacher {self.name} is saying {words}")

    def teaching(self, subject: str) -> None:
        print(f"{self.name} is teaching {subject}")

    def details(self) -> None:
        information: str = f"""
                            Teacher name is {self.name}
                            Our helpline number is {self.help_line_number}
                            """
        print(information)


obj1: Teacher = Teacher(1, "Sir Zia Khan")
obj2: Teacher = Teacher(2, "Muhammed Qasim")
obj3: Teacher = Teacher(1, "Sir Zia Khan")
obj4: Teacher = Teacher(2, "Muhammed Qasim")

print(dir(obj1))
print(obj1.name)
obj1.speak("Hello")
print(obj1.counter)
print(obj2.help_line_number)
obj1.details()


class Employee:
    def __init__(self) -> None:
        self.name: str = ""
        self.education: str = ""
        self.department: str = ""


class Designer(Employee):
    def __init__(self, title: str) -> None:
        super().__init__()  # all attributes of the Employee class imported
        self.title: str = title


class Developer(Employee):
    def __init__(self, title) -> None:
        super().__init__()
        self.title: str = title
        self.programming_skills: list[str] = ["Python"]


designe1: Designer = Designer("Animation Artist")
dev1: Developer = Developer("GenAI Engineer")

print(designe1.department)
print(dev1.programming_skills)
