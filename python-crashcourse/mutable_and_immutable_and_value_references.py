x: int = 10
print("Before Modification: ",x, id(x));

x += 1
print("After Modification: ",x, id(x));

a : list[int] = [1,2,3,4,5]

def abc(num1: list[int])->None:
    
    num1.append(100); 
    print(f"num1 value is {num1}");

abc(a); #pass by reference
print(a);

b : int = 5 #pass by value or pass by copy

def bcd(num1: int)->None:
    print(f"Num1 value before {num1}");
    num1 = 6;
    print(f"num1 value is {num1}");

bcd(b);
print(f"Original variable value is {b}");