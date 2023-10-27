import sys

l1 : list[int] = [1,2,3,4,5];

for n in l1:
    print(f"Current number {n}");

l1: tuple[int] = (1,2,3,4,5);
for n in l1:
    print(f"Item in tuple: {n}");

l1: str = "Pakistan";
for c in l1:
    print(f"Current character: {c}");

l1: dict[str,str] = {"name": "Maaz", "Age":'25'}; #Iteration perfom on keys
for k in l1:
    print(f"Dictionary key {k} and value is {l1[k]}");


l1: set[int] = {1,2,3,4,1,1,2};
for s in l1:
    print(f"Items in set: {s}");

name : str = input("What is your name: \t");
print(f"Welcome {name}")

print(sys.argv) #data passed in the console. Returns a list where every element is string