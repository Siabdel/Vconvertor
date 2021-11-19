import tkinter
import Pmw
 
 
class Demo:
    def __init__(self, parent):
        self.colors = ('yellow', 'green', 'orange')
        self.notebook = Pmw.NoteBook(parent, raisecommand=self.color_me,
                                     lowercommand=self.hide_me, borderwidth=0,
                                     pagemargin=0)
        self.notebook.pack(fill='both', expand=1, padx=10, pady=10)
        self.notebook.add('1')
        self.notebook.add('2')
        self.notebook.add('3')
        button = Tkinter.Button()
        self.defaultbg = button.cget('background')
        self.defaultfg = button.cget('foreground')
        button.destroy()
        self.notebook.tab('1').focus_set()
 
    def color_me(self, e):
        Pmw.Color.changecolor(self.notebook.tab(e), 'black',
                              foreground=self.colors[int(e)-1])
        Pmw.Color.changecolor(self.notebook.page(e), self.colors[int(e)-1],
                              foreground='red')
 
    def hide_me(self, e):
        Pmw.Color.changecolor(self.notebook.tab(e), self.defaultbg,
                              foreground=self.defaultfg)
        Pmw.Color.changecolor(self.notebook.page(e), self.defaultbg,
                              foreground=self.defaultfg)
 
 
# Pmw.NoteBook color demo
if __name__ == '__main__':
    root = tkinter.Tk()
    Pmw.initialise(root)
    root.title('Pmw.NoteBook color demo')
    widget = Demo(root)
    exitButton = Tkinter.Button(root, text='Exit', command=root.destroy)
    exitButton.pack(pady=5)
    root.mainloop()
