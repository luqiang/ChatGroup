from tkinter import *

root = Tk()
a=1

def task():
    global a
    a = a+1
    print("hello")
    root.after(1000, task)  # reschedule event in 2 seconds

root.after(1000, task)
root.mainloop()