# This file is created to practice Python programming concepts for beginners.

# ---------------------------------------------------------------------------
# Introduction to Python Data Types
# ---------------------------------------------------------------------------

# String data type
name = "Bob James"  # This is a string
print(name)  # Output: Bob James
print(type(name))  # Output: <class 'str'>
print(name[0])  # Accessing the first character, Output: B

# Integer data type
HouseNumber = 10  # This is an integer
print(HouseNumber)  # Output: 10
print(type(HouseNumber))  # Output: <class 'int'>

# List data type
my_list = [1, 2, 3, "hello", True]  # A list can hold multiple data types
print(my_list)  # Output: [1, 2, 3, 'hello', True]

# Modifying list
my_list[0] = 100
my_list.append(200)
my_list.insert(1, 300)
print(my_list)  # Updated list with new values

# Checking for membership in a list
print(2 in my_list)  # Output: True
print("Akhil" in my_list)  # Output: False

# Looping through a list
s3_bucket_name = ["bucket1", "bucket2", "bucket3"]
for i in s3_bucket_name:
    if i == "bucket2":
        print("Don't Delete")
    else:
        print(i + " Deleted")
print("Bucket names printed")

# ---------------------------------------------------------------------------
# Tuple in Python (Immutable Sequence)
# ---------------------------------------------------------------------------

my_tuple = (1, 2, 3, "world")  # Tuples are immutable
print(my_tuple[0])  # Accessing tuple elements, Output: 1
print(my_tuple[1:4])  # Slicing a tuple, Output: (2, 3, 'world')

# ---------------------------------------------------------------------------
# Dictionary in Python (Key-Value Pairs)
# ---------------------------------------------------------------------------

my_dict = {'name': 'John', 'id': 301, 'email_addr': 'abc.com'}
print(my_dict)  # Printing dictionary
print(my_dict.get('dob', '01-01-1990'))  # Fetching with a default value

# Iterating over dictionary
for key, value in my_dict.items():
    print(f"{key}: {value}")

# ---------------------------------------------------------------------------
# Set in Python (Unique Elements)
# ---------------------------------------------------------------------------

my_set = {1, 2, 3, 4, 4, 4}  # Duplicates are removed
print(my_set)  # Output: {1, 2, 3, 4}

# ---------------------------------------------------------------------------
# User Input
# ---------------------------------------------------------------------------

user_input_int = int(input("Enter an integer: "))
print(f"You entered an integer: {user_input_int}")

# ---------------------------------------------------------------------------
# Conditional Statements
# ---------------------------------------------------------------------------

# Example: Checking if a number is even or odd
num = 7
if num % 2 == 0:
    print("Even")
else:
    print("Odd")

# ---------------------------------------------------------------------------
# Loops
# ---------------------------------------------------------------------------

# For loop
fruits = ['apple', 'banana', 'cherry']
for fruit in fruits:
    print(fruit)

# While loop
count = 0
while count < 3:
    print(count)
    count += 1

# ---------------------------------------------------------------------------
# Functions in Python
# ---------------------------------------------------------------------------

# Defining a function
def greet(name):
    """This function greets the user."""
    print(f"Hello, {name}!")

greet("Alice")

# Function with a return value
def add(x, y):
    """This function returns the sum of two numbers."""
    return x + y

result = add(3, 4)
print(result)  # Output: 7

# ---------------------------------------------------------------------------
# Using Modules
# ---------------------------------------------------------------------------

import math

print(math.sqrt(16))  # Using the math module, Output: 4.0

# ---------------------------------------------------------------------------
# Working with JSON
# ---------------------------------------------------------------------------

import json

# JSON example
json_data = '{"name": "John", "age": 30}'
data = json.loads(json_data)  # Parse JSON string
print(data['name'])  # Output: John

# Modify JSON and convert back
data['age'] = 31
updated_json = json.dumps(data)
print(updated_json)  # Output: {"name": "John", "age": 31}

# ---------------------------------------------------------------------------
# Reading/Writing Files
# ---------------------------------------------------------------------------

# Writing to a file
with open('output.txt', 'w') as file:
    file.write("Hello, World!")

# Reading from a file
with open('output.txt', 'r') as file:
    content = file.read()
print(content)

# ---------------------------------------------------------------------------
# Web Scraping with BeautifulSoup
# ---------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

url = 'https://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extracting links
links = [link['href'] for link in soup.find_all('a', href=True)]
print(links)

# ---------------------------------------------------------------------------
# Conclusion
# ---------------------------------------------------------------------------
# Practice is key to mastering Python programming. Explore each concept further!
