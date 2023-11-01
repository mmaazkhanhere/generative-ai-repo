print("logic1")
print("logic2")
try:
    print(5/0) #Error but we want to continue program
except ZeroDivisionError:
    print("Zero Division Error!")
print("logic4")
print("logic5")

print("\n")

print("logic1")
print("logic2")
try:
    print(5/0) #Error but we want to continue program
except ZeroDivisionError:
    pass
print("logic4")
print("logic5")


try:
    print(age)
except Exception as e:
    print(f"Something is wrong! \n{e}")

from typing import TextIO

data:TextIO = open("./abc.txt")
print(type(data))

with open("./abc.txt") as file: #local variable containing the file
    print(type(file))
    print(file.read()) #connectivity ends outside this block automatically
    
print("Pakistan")