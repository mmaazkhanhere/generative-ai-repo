def greeting_message()->None: #function declaration
    #function body
    print("Hello World");#function statement
greeting_message(); #function calling

def piaic()->None:
    print("PIAIC Generative Artifical Intelligence");

piaic();
piaic();

#Function with optional parameters

def add_two_numbers(num1: int, num2: int = 0) -> int:
    print(num1, num2);
    return num1 + num2;

add_two_numbers(7);
add_two_numbers(7,3);

#lambda function with typing

from typing import Callable

add: Callable[[int, int], int] = lambda x, y: x + y
result = add(10, 20);
print(result);


from collections.abc import Iterator

def my_range (start: int, end: int, step: int = 1)->Iterator[int]:
    for i in range (start, end+1, step):
        yield i

a: Iterator[int] = my_range(1, 10);
print(next(a));
print(next(a));
print(type(a));

def abc(*nums): #single star will return tuple
    print(nums,type(nums))
    total=0
    for n in nums:
        total += n
        
    return total

abc(1,2,3,4,5,6);

def xyz(**kargs): # double star will return dict
    print(kargs,type(kargs));
xyz(a=7, b=20, name="Maaz")

from typing import Tuple

def greet (*names: Tuple[str, ...])->None:
    """
    This function greets all persons in the names tuple
    """
    for name in names:
        print("Hello", name);
        
greet(("Monica", "Luke", "Steve", "John"))

def my_function (a: int, b: int, *abc: int, **xyz: int) -> None:
    print(a, b, abc, xyz);
    
my_function(1, 2, 7, 9, 9, 9, c=20, d=30, x=100)

def my_decorator(func: Callable[[], None])-> Callable[[], None]:
    def wrapper():
        print("Something is happening before the function is called");
        func();
        print("Something is happening after the function is called");
    return wrapper;

@my_decorator
def say_hello():
    print("Hello!")
