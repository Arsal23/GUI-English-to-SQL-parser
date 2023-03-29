import os
import sys
from tkinter import Tk, Label, Button, Entry, StringVar, Frame
import sqlite3
import subprocess
from collections import defaultdict as dd

dir = __file__.replace(os.path.basename(__file__), '')
os.chdir(dir)

db = sqlite3.connect('database.sqlite')

try:
    parser_exec = os.path.join(dir, sys.argv[1])
except:
    parser_exec = os.path.join(dir, "parser")

#defining colours
base = "#C1E1C1"
black = "#000000"
white = "#ffffff"
blue = "#0FB5B5"
red = "#FF4500"
grey = "#777777"
orange = "#FFA400"
bold = 'bold'



window = Tk()
window.title("English to SQL")
window.configure(bg=base, border=5)
window.geometry("750x550")

# def check_parser() -> bool:
#     var = os.path.exists(parser_exec)
#     return var


def sqlite_exceptions(s):
    exceptions = {'SHOW TABLES;': "SELECT name FROM sqlite_master WHERE type='table';"}
    return exceptions.get(s, s)



def parse():
    statement = bytes(input.get() + "\n", 'utf-8')
    p = subprocess.run(parser_exec, input=statement, capture_output=True)
    # print(p)
    if p.returncode != 0:
        parser_output = "INCORRECT"
    else:
        parser_output = p.stdout.decode()

    sql.set(parser_output)

def execute():
    cur = db.cursor()
    # print(sqlite_exceptions[sql.get()])
    s = sqlite_exceptions(sql.get())
    print(s)
    cur.execute(s)
    results = cur.fetchall()

    output.set(results)
    db.commit()
    cur.close()


Label(window, text='English To SQL generator', bg=base, font=(bold, 30)).pack(pady=40)

row1 = Frame(window, bg=base)
input = StringVar(row1)

Label(row1, text='Enter your english query here: ', bg=base, font=(bold, 18)).pack(side='top', padx=10)
Entry(row1, textvariable=input, bg=white, width=100, font=bold).pack()
row1.pack()

Button(window, text="Parse Sentence", font=(bold, 12), width=50, bg="yellow", command=parse).pack(pady=10)

row2 = Frame(window, bg=base)
sql = StringVar(row2)
sql.set("")
Label(row2, text="Generated SQL statement: ", bg=base, font=(bold, 18)).pack(side='top', padx=10)
Label(row2, textvariable=sql, bg=white, font=(bold, 12), width=100).pack(side='right', padx=10)
row2.pack()

row3 = Frame(window, bg=base)
Label(row3, bg=base, font=(bold, 12)).pack(side='left', padx=10)
Button(row3, text="Exeute Statement", font=(bold, 12), width=50, bg="yellow", command=execute).pack(side='right', padx=10)
row3.pack(pady=10)

output = StringVar(window)
Label(window, textvariable=output, width=100, height=10, bg=white, anchor='nw', padx=10, pady=10, font=(bold, 14)).pack()


try:
    window.mainloop()
    pass
finally:
    db.close()

# print(check_parser())
