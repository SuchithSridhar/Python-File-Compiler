"""
This is a GUI program to compiler
python files for assignments
This is taking the main functions
from a file : CompilerBase
CompilerBase.py:

the_main(questions_list, values_dict, wait_func, file_to_write="Compiled Files.txt") :
Does everything needed :)

wait_func --> event to be waited for before the thing is copied from clip_board

example vals :
vals_dict = {
    'title': "list based assignment",
    'by_line': "suchith sridhar",
    'files': q_list,
    'question_line': True,
    'doc_string': "Name : Suchith\nClass:12 C",
    'output': True,
    'output_data': None,
    'output_start': string
    'output_end': string
}
"""
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import CompilerBase as cb
import time
import os
import pickle

ORGINAL_PATH = os.getcwd()
COMPILER_FOLDER = 'FileCompilerData'
READFILE = "cached.piler"
COMPLETE_READFILE = os.path.join(COMPILER_FOLDER, READFILE)


class MakeButton:
    def __init__(self, text="", pos=(0, 0), dims=None, command=None):
        # dims - (w,h)
        self.button = ttk.Button(
            root, text=text, command=command, style='Kim.TButton')
        self.pos = pos
        self.dims = dims
        self.command = command
        self.place_button()

    def place_button(self, changed_pos=None, changed_dims=None):
        if changed_pos is not None:
            self.pos = changed_pos
        if changed_dims is not None:
            self.dims = changed_dims

        if self.dims is not None:
            self.button.place(x=self.pos[0], y=self.pos[1],
                              width=self.dims[0], height=self.dims[1])
        else:
            self.button.place(x=self.pos[0], y=self.pos[1])


class MakeLabel:

    def __init__(self, text="", pos=(0, 0),
                 dims=None, font_size=13, bg_color=None):
        # dims - (w,h)
        self.label = Label(root, text=text, bg=bg_color)
        self.label.config(font=("Courier", font_size))
        self.pos = pos
        self.dims = dims

        self.place_label()

    def place_label(self, changed_pos=None, changed_dims=None):
        if changed_pos is not None:
            self.pos = changed_pos
        if changed_dims is not None:
            self.dims = changed_dims

        if self.dims is not None:
            self.label.place(x=self.pos[0], y=self.pos[1],
                             width=self.dims[0], height=self.dims[1])
        else:
            self.label.place(x=self.pos[0], y=self.pos[1])


class MakeTextbox:

    def __init__(self, pos=(0, 0), dims=None):
        # dims - (w,h)
        self.textbox = Text(root)
        self.textbox.config(font=("Courier", 13))
        self.pos = pos
        self.dims = dims

        self.place_textbox()

    def place_textbox(self, changed_pos=None, changed_dims=None):
        if changed_pos is not None:
            self.pos = changed_pos
        if changed_dims is not None:
            self.dims = changed_dims

        if self.dims is not None:
            self.textbox.place(x=self.pos[0], y=self.pos[1],
                               width=self.dims[0], height=self.dims[1])
        else:
            self.textbox.place(x=self.pos[0], y=self.pos[1])

    def get_text(self):
        value = self.textbox.get('0.0', 'end')
        try:
            while value[-1] == "\n":
                value = value[:-1]  # removes the default \n
        except IndexError:
            pass

        return value

    def add_text(self, text=""):
        self.textbox.insert('end', text)


class MakeCheckbox:

    def __init__(self, pos=(0, 0), dims=None):
        # dims - (w,h)
        self.var = IntVar()
        self.var.set(1)
        self.checkbox = ttk.Checkbutton(root, variable=self.var)
        self.pos = pos
        self.dims = dims

        self.place_checkbox()

    def place_checkbox(self, changed_pos=None, changed_dims=None):
        if changed_pos is not None:
            self.pos = changed_pos
        if changed_dims is not None:
            self.dims = changed_dims

        if self.dims is not None:
            self.checkbox.place(x=self.pos[0], y=self.pos[1],
                                width=self.dims[0], height=self.dims[1])
        else:
            self.checkbox.place(x=self.pos[0], y=self.pos[1])

    def value(self):
        return self.var.get()


'''
vals_dict = {
    'title': "list based assignment",
    'by_line': "suchith sridhar",
    'files': q_list,
    'question_line': True,
    'doc_string': "Name : Suchith\nClass:12 C",
    'output': True,
    'output_data': None,
    'output_start': string
    'output_end': string
}
'''


def finish(texts, window, folder):
    try:
        os.chdir(folder.get())
    except Exception as e:
        print(e)

    types = ["title", "by_line", "question_line",
             "doc_string", "output", "output_start", "output_end", 'word_file']

    make_file_vals = {'lasttime_file': folder.get()}
    values = {'lasttime_file': folder.get()}

    for i in types:
        try:
            if checkboxes[i].value():
                try:
                    values[i] = textboxes[i].get_text()
                    make_file_vals[i] = values[i]
                except KeyError:
                    values[i] = True

            else:
                values[i] = None
        except KeyError:
            try:
                values[i] = textboxes[i].get_text()
                make_file_vals[i] = values[i]

            except KeyError:
                print("Something happend")
                raise Exception
    q_list = []
    for i in texts:
        string = i.get()
        try:
            open(string)
        except FileNotFoundError:
            print("no", string)
            pass
        else:
            q_list.append(string)

    values["q_list"] = q_list
    values["files"] = q_list

    cache_data(make_file_vals)
    print("Got here 1")
    cb.the_main(q_list, values)
    print("got here 2")
    window.destroy()


def cache_data(make_file_vals):
    temp_path = os.getcwd()

    os.chdir(ORGINAL_PATH)

    if os.path.isdir(COMPILER_FOLDER):
        print(COMPILER_FOLDER)
    else:
        os.makedirs(COMPILER_FOLDER)
        print(COMPILER_FOLDER)

    with open(COMPLETE_READFILE, 'wb') as File:
        pickle.dump(make_file_vals, File)

    os.chdir(temp_path)


def questions_prompt(lasttime_file):
    count = 0
    texts = []
    window = Toplevel(root, height=600, width=600)
    window.title("Add Questions")

    for y in range(75, 500, 30):
        for x in range(50, 600, 300):
            texts.append(None)
            texts[count] = ttk.Entry(window)
            texts[count].place(x=x, y=y, width=200, height=25)
            count += 1

    auto = ttk.Button(window, text="Auto Generate",
                      command=lambda: automate(texts))
    auto.place(x=25, y=40, width=275, height=25)

    # Wait time just so that all the textboxes can appear

    # clear = ttk.Button(window, text="Clear Questions", command=add_question)
    # clear.place(x=225, y=25, width=150, height=25)

    search_folder = StringVar()
    search_folder.set(lasttime_file)

    folder_entry = Entry(window, textvariable=search_folder)
    folder_entry.place(x=100, y=5, width=450-25, height=25)

    done = ttk.Button(window, text="Compile",
                      command=lambda: finish(texts, window, search_folder))
    done.place(x=300, y=40, width=275, height=25)

    browsebutton = ttk.Button(window, text="Browse",
                              command=lambda: browsefunc(search_folder))
    browsebutton.place(x=500, y=5, width=75, height=25)

    text_folder = Label(window, text="Questions in: ")
    text_folder.place(x=25, y=5, height=25)


def browsefunc(folder):
    filename = filedialog.askdirectory()
    # filename = filedialog.askopenfilename()
    folder.set(filename)


def automate(texts):
    for textbox in texts:
        text = "Q"+str(texts.index(textbox)+1)+".py"
        textbox.insert("end", text)


root = Tk()
root.geometry("800x650")
root.resizable(False, True)
root.geometry("+250+0")
root.title("Comipler - SuchithSridhar")

textboxes = {}
buttons = {}
checkboxes = {}
labels = {}

# Retrive Cached Text -----------------------

try:
    with open(READFILE, 'rb') as retrive:
        retrived_text = pickle.load(retrive)

except FileNotFoundError:
    try:
        with open(COMPLETE_READFILE, "rb") as retrive:
            retrived_text = pickle.load(retrive)

    except FileNotFoundError:
        retrived_text = {"title": "\t\tName Of  Assignment",
                         "by_line": "\t\t\t- Your Name",
                         "doc_string": "Name: Your Name\nClass: Your Class",
                         "output_start": "'''\n--------- Output ---------",
                         "output_end": "'''",
                         "lasttime_file": ORGINAL_PATH}

# ------------------------------------------------


n_height = 25
n_width = 500

# Introduction
title = "---------------------- Assignment Compiler ----------------------"
labels["intro"] = MakeLabel(text=title, pos=(0, 0),
                            dims=(800, n_height * 2 - 10), font_size=15,
                            bg_color="lightgrey")

# Title
textboxes["title"] = MakeTextbox(pos=(25, 50), dims=(n_width, n_height))
textboxes["title"].add_text(retrived_text["title"])
labels["title"] = MakeLabel(text="Title", pos=(550, 50))
checkboxes["title"] = MakeCheckbox(pos=(750, 50 + 3))

# By-Line
textboxes["by_line"] = MakeTextbox(pos=(25, 80), dims=(n_width, n_height))
textboxes["by_line"].add_text(retrived_text["by_line"])
labels["by_line"] = MakeLabel(text="By-Line", pos=(550, 80))
checkboxes["by_line"] = MakeCheckbox(pos=(750, 80 + 3))

# Question Line
question_line = "-------------------------------- Q1"
labels["q_line_display"] = MakeLabel(
    text=question_line, pos=(25, 110), bg_color="white")
labels["question_line"] = MakeLabel(text="Question Line", pos=(550, 110))
checkboxes["question_line"] = MakeCheckbox(pos=(750, 110 + 3))

# Doc_string
labels["doc_string"] = MakeLabel(text="'''", pos=(25, 150),
                                 font_size=10, bg_color="white")
labels["doc_string"] = MakeLabel(text="Program: Q1", pos=(25, 170),
                                 bg_color="white")
textboxes["doc_string"] = MakeTextbox(pos=(25, 200),
                                      dims=(n_width, n_height * 3))
textboxes["doc_string"].add_text(retrived_text["doc_string"])
labels["doc_string"] = MakeLabel(text="Doc-String", pos=(550, 200))
checkboxes["doc_string"] = MakeCheckbox(pos=(750, 200 + 3))
labels["doc_string"] = MakeLabel(text="'''", pos=(25, 276),
                                 font_size=10, bg_color="white")
# pos=(25, 290) To be

# Program Code
string = """-------------------------------
You program code for
each question exits here
-------------------------------"""
labels["program_code"] = MakeLabel(text=string, pos=(25, 300),
                                   bg_color="white",
                                   dims=(n_width, n_height * 3))

# Code Output
textboxes["output_start"] = MakeTextbox(
    pos=(25, 400), dims=(n_width, n_height * 2))
textboxes["output_start"].add_text(retrived_text["output_start"])

labels["output"] = MakeLabel(text="Add Output", pos=(550, 430))
checkboxes["output"] = MakeCheckbox(pos=(750, 430 + 3))

labels["output"] = MakeLabel(text="Output text", pos=(550, 460))
checkboxes["output_start"] = MakeCheckbox(pos=(750, 460 + 3))

labels["word_file"] = MakeLabel(text="Make WordFile", pos=(550, 490))
checkboxes["word_file"] = MakeCheckbox(pos=(750, 490+3))

string = """-------------------------------
You program output
for each program
-------------------------------"""
labels["program_code"] = MakeLabel(text=string, pos=(
    25, 460), bg_color="white", dims=(n_width, n_height * 3))
textboxes["output_end"] = MakeTextbox(
    pos=(25, 550), dims=(n_width, n_height * 2))
textboxes["output_end"].add_text(retrived_text["output_end"])

# FinalButton
buttons["final"] = MakeButton(text="Compile Assignment", pos=(150, 610),
                              dims=(500, n_height),
                              command=lambda: questions_prompt(
    lasttime_file=retrived_text['lasttime_file']))

root.mainloop()
