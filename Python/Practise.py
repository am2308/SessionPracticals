# This file is created to practise python programming
# List in python
name = "Bob James" # String
print(name)  # Bob James
print(type(name))  # <class 'str'>
print(name[0])  # B

#print(type(name.split(' ')))  # A


HouseNumber = 10
print(HouseNumber)  # 10
print(type(HouseNumber))  # <class 'int'>
print(type(name))  # <class 'str'>

my_list = [1, 2, 3, "hello", True]
print(my_list)  # [1, 2, 3, 'hello', True]
print(my_list[0])  # 1

my_list[0] = 100
print(my_list)  # [100, 2, 3, 'hello', True]

my_list.append(200)
print(my_list)  # [100, 2, 3, 'hello', True, 200]

my_list.insert(1, 300)
print(my_list)  # [100, 300, 2, 3, 'hello', True, 200]

my_list.remove(3)
print(my_list)  # [100, 300, 2, 'hello', True, 200]

my_list.pop(1)
print(my_list)  # [100, 2, 'hello', True, 200]

print(my_list.index('hello'))  # 2
print(my_list.count(2))  # 1

print(2 in my_list)  # True
print ("Akhil" in my_list)  # False
print(my_list[0:4])  # [100, 2] --> from 0th to 2nd index but include 0th position value explude 2nd position value

s3_bucket_name = ["bucket1", "bucket2", "bucket3"]
for i in s3_bucket_name:
   if i == "bucket2":
       print("Don't Delete")
   else:
       print(i + "Deleted") # s3.deleet(bucket)
print("Bucket names printed")

# Tuple in python(where we can't change the values)
my_tuple = (1, 2, 3, "world")
print(my_tuple[0])  # 1
print(my_tuple[1:4])  # (2, 3, 'world')
print(my_tuple + (6, 7))  # (1, 2, 3, 'world', 6, 7)
print(my_tuple * 2)  # (1, 2, 3, 'world', 1, 2, 3, 'world')

#my_tuple[0] = 100
#my_tuple.pop()  # AttributeError: 'tuple' object has no attribute 'pop'
#my_tuple.append(100)  # AttributeError: 'tuple' object has no attribute 'append'
#my_tuple.insert(1, 100)  # AttributeError: 'tuple' object has no attribute 'insert'

# Dictionary in python
my_dict = {'name': 'John', 'id': 301, 'email_addr': 'abc.com'}

print(my_dict)  # {'name': 'John', 'age': 30, 'city': 'New York'}
print(my_dict['name'])  # John
print(my_dict.get('name'))  # John
print(my_dict.get('dob'))  # None
print(my_dict.get('dob', '01-01-1990'))  # 01-01-1990
print(my_dict.keys())  # dict_keys(['name', 'age', 'city'])
print(my_dict.values())  # dict_values(['John', 30, 'New York'])
print(my_dict.items())  # dict_items([('name', 'John'), ('age', 30), ('city', 'New York'])
print('name' in my_dict)  # True
print('dob' in my_dict)  # False
for key in my_dict:
    print(key)
    print(key, my_dict[key])

# Set in python(Uniquesness)
# Creating a set
my_set = {1, 2, 3, 4, 4, 4}

# Adding and removing elements
my_set.add(5)
print("Original set:", my_set)
my_set.remove(2)
print("Updated set:", my_set)


# User Input
user_input_int = int(input("Enter an integer: "))
print(f"You entered an integer: {user_input_int}")

## Conditional Statements
# Example 1: Checking if a number is positive
num = 10

if num > 0:
    print("The number is positive.")
print("Statement outside if block")

# If-else statement
# Example 2: Checking if a number is even or odd
num = 7

if num % 2 == 0:
    print("The number is even.")
else:
    print("The number is odd.")

# If-elif-else statement
# Example 3: Determining the grade based on a score
score = 75

if score >= 90:
    print("Grade A")
elif score >= 80:
    print("Grade B")
elif score >= 70:
    print("Grade C")
elif score >= 60:
    print("Grade D")
else:
    print("Grade F")

# Nested-if statement
# Example 4: Nested if statements to determine eligibility for a loan
income = 50000
credit_score = 700

if income >= 60000:
    if credit_score >= 700:
        print("You are eligible for a loan with a low interest rate.")
    else:
        print("You are eligible for a loan with a higher interest rate.")
else:
    print("You are not eligible for a loan.")

## Loops

# For loop
fruits = ['apple', 'banana', 'cherry']
for fruit in fruits:
    print(fruit)
print("End of loop")

# while loop
count = 0
while count < 5:
    print(count)
    count += 1
print("End of loop", count)

# break and continue statement
for i in range(10):
    if i == 5:
        break
    print(i)
print("End of loop")

for i in range(10):
    if i == 5:
        continue
    print(i)
print("End of loop")

# Looping through a dictionary
person = {'name': 'John', 'age': 30, 'city': 'New York'}
for key, value in person.items():
    print(f'{key}: {value}')

# Loop control statements
for i in range(5):
    print(i)
else:
    print("Loop completed without a break.")

## Functions
def greet(name):
    """
    This function prints a greeting message.
    """
    print(f"Hello, {name}!")

# Call the function
greet("Alice")

# Function with return value
def add(x, y):
    """
    This function returns the sum of two numbers.
    """
    return x + y

result = add(3, 4)
print(result)  # Output: 7

# Function with default arguments
def greet(name="Alice"):
    print(f"Hello, {name}!")

greet()  # Output: Hello, Alice!

# Function with keyword arguments
def greet(name, message):
    print(f"{message}, {name}!")

greet(message="Good morning", name="Alice")  # Output: Good morning, Alice!

# Function with variable-length arguments
def add(*args):
    sum = 0
    for num in args:
        sum += num
    return sum
add(1, 2, 3)  # Output: 6

# Module
import mathmodule
result_add = mathmodule.add(3, 4)
result_subtract = mathmodule.subtract(7, 2)

print(result_add)     # Output: 7
print(result_subtract)  # Output: 5

from mathmodule import multiply, divide

result_multiply = multiply(5, 6)
result_divide = divide(8, 2)

print(result_multiply)  # Output: 30
print(result_divide)    # Output: 4.0