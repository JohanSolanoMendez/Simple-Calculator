from tkinter import *
from tkinter import ttk
import os
import time

COLOR_SCREEN = "#2A9DF4"
NUMERIC_BUTTON_COLOR="#4C566A"
CALCULATOR_COLOR="#A5C770"
TEXT_COLOR="#0A0A0A"
OPERATION_BUTTON_COLOR = "#5E81AC"
EQUAL_BUTTON_COLOR = "#88C0D0"
CLEAR_BUTTON_COLOR = "#BF616A"
MAIN_COLOR = "#2E3440"

CALCULATOR_TEXT = ""
TEMP_TEXT = ""
RESULT = None
OPERATION_TEXT = ""

MAX_DIGITS = 10
BUTTON_WIDTH = 5
BUTTON_HEIGHT = 5

BUTTONS = [
    'AC', 'C', '%', '/',
    '7', '8', '9', '*',
    '4', '5', '6', '-',
    '1', '2', '3', '+',
    '.', '0', '=', 
]

#Config Window
root = Tk()
root.title("Simple Calculator")
root.resizable(False, False)
root.geometry("400x460")
root.configure(bg=MAIN_COLOR)

#Icon
script_dir = os.path.dirname(__file__)
image_path = os.path.join(script_dir, "calculator.png")
if os.path.exists(image_path):
    icon = PhotoImage(file=image_path)
    root.iconphoto(True, icon)

#Screen
screen = Frame(root)
screen.config(bg=COLOR_SCREEN,width=370, height=100,bd=3, relief="sunken")
screen.pack(side="top",pady=30)

#Text labels
textScreen = Label(
    screen, 
    text=CALCULATOR_TEXT,
    fg=TEXT_COLOR,
    padx=10,
    pady=10,
    bg=COLOR_SCREEN,
    font=("Digital",40)
)
textScreen.place(relx=1.0, rely=0.6, anchor=E)

textOperation = Label(
    screen,
    text="",
    bg=COLOR_SCREEN,
    font=("Digital",15),
)
textOperation.place(relx=1.0, rely=0.2, anchor=E)

def pressed(button):
    global TEMP_TEXT
    global RESULT
    global OPERATION_TEXT
    operators = {"+","-","/","*","%"}

    if button in operators:
        if RESULT is not None:
            TEMP_TEXT = RESULT + str(button)
            RESULT = None
        else:
            TEMP_TEXT += str(button)
        textScreen.config(text="")
        textOperation.config(text=TEMP_TEXT)
    elif button == "C":
        actual = textScreen.cget("text")
        if actual:
            textScreen.config(text=actual[:-1])
    elif button == "AC":
        TEMP_TEXT = ""
        RESULT = None
        textScreen.config(text="")
        textOperation.config(text="")
    elif button == "=":
        calculate()
        textOperation.config(text=textOperation.cget("text"))
    else:
        if RESULT is not None:
            TEMP_TEXT = RESULT + str(button)
            textScreen.config(text="")
            RESULT = None
   
        actual = textScreen.cget("text")
        if len(actual) < MAX_DIGITS:
            textScreen.config(text=actual + str(button))
            TEMP_TEXT += str(button) 
            textOperation.config(text=TEMP_TEXT)

#Methods
def fix_input(text):
    import re
    if re.fullmatch(r"^\.\d+$",text):
        return "0" + text
    elif re.fullmatch(r"^\d+\.$",text):
        return text + "0"
    return text

def calculate():
    global TEMP_TEXT
    global RESULT
    TEMP_TEXT=fix_input(TEMP_TEXT)
    try:
        operation = eval(TEMP_TEXT)
        if operation % 1 != 0:
            operation = "{:.10f}".format(operation)
        textScreen.config(text=str(operation))
        RESULT = str(operation)
        TEMP_TEXT = str(operation)
    except:
        textScreen.config(text="Error")
        time.sleep(1)
        TEMP_TEXT = ""
        RESULT = None
        textScreen.config(text="")

#Numerics Buttons Style
style = ttk.Style()
style.theme_use("alt")
style.configure("Numeric.TButton",
                borderwidth=5,
                width=BUTTON_WIDTH, 
                height=BUTTON_HEIGHT,
                relief="flat",
                background=NUMERIC_BUTTON_COLOR, 
                foreground=TEXT_COLOR,
                font=('American typewriter', 19, "bold"))

style.map("Numeric.TButton",
          background=[("active", "#434C5E"),
                      ("!disabled",NUMERIC_BUTTON_COLOR)])

#Operators Buttons Style
style.configure("Operation.TButton",
                background=OPERATION_BUTTON_COLOR,
                foreground=TEXT_COLOR,
                borderwidth=5,
                width=BUTTON_WIDTH, 
                height=BUTTON_HEIGHT,
                relief="flat",
                font=('American typewriter', 19, "bold"))
style.map("Operation.TButton",
          background=[("active","#81A1C1"),
                      ("!disabled",OPERATION_BUTTON_COLOR)])

#Clear Button Style
style.configure("Clear.TButton",
                background=CLEAR_BUTTON_COLOR,
                foreground=TEXT_COLOR,
                borderwidth=5,
                width=BUTTON_WIDTH, 
                height=BUTTON_HEIGHT,
                relief="flat",
                font=('American typewriter', 19, "bold"))
style.map("Clear.TButton",
          background=[("active","#D08770"),
                      ("!disabled",CLEAR_BUTTON_COLOR)])

#Equal Button Style
style.configure("Equal.TButton",
                background=EQUAL_BUTTON_COLOR,
                foreground=TEXT_COLOR,
                borderwidth=5,
                width=BUTTON_WIDTH, 
                height=BUTTON_HEIGHT,
                relief="flat",
                font=('American typewriter', 19, "bold"))
style.map("Equal.TButton",
          background=[("active","#8FBCBB"),
                      ("!disabled",EQUAL_BUTTON_COLOR)])

#Create buttons
buttons = Frame(bg=MAIN_COLOR)
buttons.pack()
row, column = 0,0
PADX=5
PADY=5

for button in BUTTONS:
    operations = {"+","-","*","/","%"}
    if button in operations:
        if button == "+":
            ttk.Button(buttons,
                   text=button,
                   style="Operation.TButton",
                   command=lambda b=button:pressed(b)).grid(row=row,column=column,rowspan=2,columnspan=1,sticky="ns",padx=PADX, pady=PADY)
        else:
            ttk.Button(buttons,
                   text=button,
                   style="Operation.TButton",
                   command=lambda b=button:pressed(b)).grid(row=row,column=column,padx=PADX, pady=PADY)

    elif button in {"AC","C"}:
       ttk.Button(buttons,
                  text=button,
                  style="Clear.TButton",
                  command=lambda b=button:pressed(b)).grid(row=row,column=column,padx=PADX, pady=PADY)

    elif button == "=":
        ttk.Button(buttons,
                   text=button,
                   style="Equal.TButton",
                   command=lambda b = button:pressed(b)).grid(row=row,column=column,padx=PADX, pady=PADY)

    else:
        ttk.Button(buttons, 
           text=button, 
           style= "Numeric.TButton",
           command=lambda b=button: pressed(b)).grid(row=row, column=column,padx=PADX, pady=PADY)
    column += 1
    if column > 3:
        column = 0
        row += 1

root.mainloop()