import sys

l1 : list[int] = [1,2,3,4,5];

for n in l1:
    print(f"Current number {n}");

from typing import Tuple
l0: Tuple[int, ...] = (1, 2, 3, 4, 5)
for n in l0:
    print(f"Item in tuple: {n}")

l2: str = "Pakistan";
for c in l2:
    print(f"Current character: {c}");

from typing import Dict
l3: Dict[str, str] = {"name": "Maaz", "Age": '25'}  # Change '25' to 25 if 'Age' should be an integer
for k in l3:
    print(f"Dictionary key {k} and value is {l3[k]}")


l4: set[int] = {1,2,3,4,1,1,2};
for s in l4:
    print(f"Items in set: {s}");

name : str = input("What is your name: \t");
print(f"Welcome {name}")

print(sys.argv) #data passed in the console. Returns a list where every element is string