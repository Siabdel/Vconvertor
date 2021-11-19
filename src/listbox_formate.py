from Tkinter import *
import tkFont

master = Tk()
master.resizable(width=False, height=False)
master.geometry('{width}x{height}'.format(width=300, height=100))
my_font = tkFont.Font(family="Monaco", size=12) # use a fixed width font so columns align

listbox = Listbox(master, width=400, height=400, font=my_font)
listbox.pack()

table = [["spam", 42, "test", ""],["eggs", 451, "", "we"],["bacon", "True", "", ""]]
headers = ["item", "qty", "sd", "again"]

row_format ="{:<8}  {:>8}  {:<8}  {:8}" # left or right align, with an arbitrary '8' column width 

listbox.insert(0, row_format.format(*headers, sp=" "*2))
for items in table:
    listbox.insert(END, row_format.format(*items, sp=" "*2))
mainloop()