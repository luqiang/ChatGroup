from tkinter import *
class Log (Frame):
    def __init__(self,master):
        frame = Frame(master)
        frame.pack()
        self.lab1 = Label(frame,text = "User:")
        self.lab1.grid(row = 0,column = 0,sticky = W)
        self.ent1 = Entry(frame)
        self.ent1.grid(row = 0,column = 1,sticky = W)
        self.lab2 = Label(frame,text = "Password:")
        self.lab2.grid(row = 1,column = 0)
        self.ent2 = Entry(frame,show = "*")
        self.ent2.grid(row = 1,column = 1,sticky = W)
        self.button = Button(frame,text = "登录",command = self.Submit)
        self.button.grid(row = 2,column = 1,sticky = E)
        self.lab3 = Label(frame,text = "")
        self.lab3.grid(row = 3,column = 0,sticky = W)
        self.button2 = Button(frame,text = "退出",command = frame.quit)
        self.button2.grid(row = 3,column = 3,sticky = E)
    def Submit(self):
        s1 = self.ent1.get()
        s2 = self.ent2.get()
        if s1 == 'freedom' and s2 == '123':
            self.lab3["text"] = "Confirm"
        else:
            self.lab3["text"] = "Error!"
        self.ent1.delete(0,len(s1))
        self.ent2.delete(0,len(s2))
root = Tk()
root.title("登录")
app = Reg(root)
root.mainloop()