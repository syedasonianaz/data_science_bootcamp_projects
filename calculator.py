from tkinter import *
from tkinter import ttk
import math

last_value = None

# Making Calculator Buttons Functionality
def click(value):
    global last_value

    current_expression = entryField.get()
    answer = ""

    if value == "CE":
        entryField.delete(0, END)
        last_value = None
    elif value == "=":
        try:
            answer = str(eval(current_expression))
            entryField.delete(0, END)
            entryField.insert(END, answer)
            last_value = answer
        except Exception as e:
            entryField.delete(0, END)
            entryField.insert(END, "Error: Please enter a number first")
    elif value == "√":
        try:
            result = math.sqrt(eval(current_expression))
            entryField.delete(0, END)
            entryField.insert(END, result)
            last_value = result
        except Exception as e:
            entryField.delete(0, END)
            entryField.insert(END, "Error: Please enter a number first")
    elif value == "sin":
        try:
            result = math.sin(math.radians(eval(current_expression)))
            entryField.delete(0, END)
            entryField.insert(END, result)
            last_value = result
        except Exception as e:
            entryField.delete(0, END)
            entryField.insert(END, "Error: Please enter a number first")
    elif value == "cos":
        try:
            result = math.cos(math.radians(eval(current_expression)))
            entryField.delete(0, END)
            entryField.insert(END, result)
            last_value = result
        except Exception as e:
            entryField.delete(0, END)
            entryField.insert(END, "Error: Please enter a number first")
    elif value == "tan":
        try:
            result = math.tan(math.radians(eval(current_expression)))
            entryField.delete(0, END)
            entryField.insert(END, result)
            last_value = result
        except Exception as e:
            entryField.delete(0, END)
            entryField.insert(END, "Error: Please enter a number first")
    elif value in ["+", "-", "*", "/"]:
        if last_value in ["+", "-", "*", "/"] or not current_expression:
            entryField.delete(0, END)
            entryField.insert(END, "Error: Please enter a valid expression")
        else:
            entryField.insert(END, value)
            last_value = value
    else:
        entryField.insert(END, value)
        last_value = value

def calculate_columnspan():
    num_columns = 4  # Adjust the number of columns as needed
    return num_columns if num_columns > 0 else 1

# Creating window for calculator
root = Tk()
root.title("Scientific Calculator")
root.geometry('350x450')
root.config(bg='#282c34') 

# Entry widget
entryField = Entry(root, font=('Arial', 16), bd=3, bg='#383838', fg='white', relief=SUNKEN)
entryField.grid(row=0, column=0, columnspan=6, pady=5, padx=5, sticky='nsew')

# Style for themed buttons
style = ttk.Style()
style.configure('TButton', font=('Arial', 14), padding=5, relief='flat', background='#1e2328') 

button_text_list = ["√", "sin", "cos", "tan", # Creating list instead of creating all buttons separately
                    "7", "8", "9", "/",
                    "4", "5", "6", "*",
                    "1", "2", "3", "-",
                    "CE", "0", ".", "+",
                    "="]

# Function to create themed buttons
def create_button(root, text, row, column, columnspan=1):
    button = ttk.Button(root, text=text, command=lambda: click(text))
    button.grid(row=row, column=column, columnspan=columnspan, pady=2, padx=2, sticky='nsew')

# Loop to create buttons
row_value = 1
column_value = 0
for i in button_text_list:
    if i == "=":
        create_button(root, i, row_value, column_value, columnspan=calculate_columnspan())  # Make "=" cover the entire line
    else:
        create_button(root, i, row_value, column_value)
    column_value += 1
    if column_value > 3:
        row_value += 1
        column_value = 0

# Adjust column and row weights for better resizing behavior
for i in range(6):
    root.columnconfigure(i, weight=1)
for i in range(1, 6):
    root.rowconfigure(i, weight=1)

root.mainloop()
