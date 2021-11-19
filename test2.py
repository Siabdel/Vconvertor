import tkinter as tk
import tkinter.ttk as ttk
import Pmw as pmw
 
root = tk.Tk()
root.geometry("800x600")
pmw.initialise()
 
notebook = pmw.NoteBook(root)
notebook.pack(side='top', anchor='w', padx=50, pady=50)
root.mainloop()
