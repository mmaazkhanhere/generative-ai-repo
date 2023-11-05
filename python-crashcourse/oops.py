from typing import overload, Union
from typing import Type


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


# Multiple Inheritance


class A:
    def method_A(self) -> None:
        print("Method from class A")


class B:
    def method_B(self) -> None:
        print("Method from class B")


class C(A, B):
    def method_C(self) -> None:
        print("Method from class C")


# Creating an object of class C
obj_c = C()

# Accessing methods from each parent class
obj_c.method_A()  # Calls method from class A
obj_c.method_B()  # Calls method from class B
obj_c.method_C()  # Calls method from class C


class Mother:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.eye_color: str = "Blue"

    def speaking(self, words: str) -> str:
        return f"Mother Speaking function"


class Father:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.height: str = "6 Feet"


class Child(Mother, Father):
    def __init__(self, mother_name: str, father_name: str, child_name: str) -> None:
        Mother.__init__(self, mother_name)
        Father.__init__(self, father_name)
        self.child_name: str = child_name


qasim: Child = Child("Naseem Bano", "Muhammed Aslam", "Muhammed Qasum")
print(f"Object height : {qasim.height}")
print(f"Eye color : {qasim.eye_color}")


# function overloading


@overload
def add(x: int, y: int) -> int:
    ...


@overload
def add(x: float, y: float) -> float:
    ...


@overload
def add(x: str, y: str) -> str:
    ...


def add(x: Union[int, float, str], y: Union[int, float, str]) -> Union[int, float, str]:
    if isinstance(x, int) and isinstance(y, int):
        return x + y
    elif isinstance(x, float) and isinstance(y, float):
        return x + y
    elif isinstance(x, str) and isinstance(y, str):
        return x + y
    else:
        raise TypeError("Invalid Argument Types")


result1 = add(1, 2)
print(result1)
result2 = add(1.5, 2.5)
print(result2)
result3 = add("Hello", "World")
print(result3)


# Static Method
class MyClass:
    static_var: int = 10  # Class variable (static variable)

    @staticmethod
    def static_method() -> str:
        return "This is a static method"


# Accessing the static method and static variable
print(MyClass.static_method())  # Output: "This is a static method"
print(MyClass.static_var)  # Output: 10


# Overriding


class Animal:
    def sound(self) -> str:
        return "Generic animal sound"


class Dog(Animal):
    def sound(self) -> str:
        return "Woof!"


class Cat(Animal):
    def sound(self) -> str:
        return "Meow!"


def make_sound(animal: Type[Animal]) -> None:
    print(animal().sound())


# Using the overridden methods
make_sound(Animal)  # Output: "Generic animal sound"
make_sound(Dog)  # Output: "Woof!"
make_sound(Cat)  # Output: "Meow!"


# Callable Function


class Square:
    def __init__(self, exponent=2):
        self.exponent = exponent

    def __call__(self, value):
        return value**self.exponent


num: Square = Square()
print(f"Exponent Value: {num.exponent}")
print(f"{3} power exponent {num.exponent} is {num(3)}")


class CumulativeAverage:
    def __init__(self):
        self.data = []

    def __call__(self, new_value):
        self.data.append(new_value)
        print(self.data)
        return sum(self.data) / len(self.data)


stream_average = CumulativeAverage()
stream_average(12)
stream_average(13)
stream_average(14)

# Access Modifier


class Piaic:
    def __init__(self) -> None:
        self.piaic_helpline: str = "0800"  # public
        self._total_expense: int = 600000  # protected (you can identify protected variable if it starts with _ just like _total_expense)
        self.__test_announcement: str = "5 Nov 2023"  # private (you can identifiy private variable if it starts with __ (dunder) just like here)


maaz: Piaic = Piaic()
print(f"Public Variable {maaz.piaic_helpline}")
maaz.piaic_helpline = "85263"
print(f"Public variable after value changed {maaz.piaic_helpline}")

# maaz.__test_announcement #cannot access it because private
maaz._Piaic__test_announcement  # can access private variable like this because python is not pure oops


# Abstract Class


from abc import ABC, abstractmethod


class Vehicle(ABC):
    @abstractmethod  # necessary to include
    def drive(self) -> None:
        pass


class Car(Vehicle):
    def drive(self) -> None:
        print("Car is being driven")


class Bike(Vehicle):
    def drive(self) -> None:
        print("Bike is being ridden")


# Trying to instantiate the abstract class (will raise an error)
try:
    vehicle = Vehicle()  # This will raise an error
except TypeError as e:
    print(f"TypeError: {e}")

car = Car()
car.drive()  # Output: Car is being driven

bike = Bike()
bike.drive()  # Output: Bike is being ridden
