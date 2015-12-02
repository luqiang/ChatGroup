from tkinter import *
import socket



TITLE_FONT = ("Arial", 12, "")
class ClientNet:
    def __init__(self,aHost,aPort):
        self.serverHost=aHost
        self.port=aPort
        self.connected=False


    def connectServer(self):
        try:
            self.clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.clientSock.connect(self.serverHost,self.port)
            self.connected=True
        except:
            self.connected=False


class ChatShow(Frame):

     def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        #scrollbar
        consoleShowScrollBar=Scrollbar(self)
        consoleShowScrollBar.pack(side=RIGHT,fill=Y)
        #console:text and pictures
        consoleShow = Listbox(self,width=100,)
        consoleShow['yscrollcommand'] = consoleShowScrollBar.set
        consoleShow.pack(expand=1,fill=BOTH)
        consoleShowScrollBar['command'] = consoleShow.yview()


    # def receiverMessage(self):
    #     try:
    #         self.clientSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #         self.clientSock.connect((self.local, self.port))


class Log(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        lab1 = Label(self,text = "User:", font=TITLE_FONT)
        lab1.grid(row = 0,column = 0,sticky = W)
        ent1 = Entry(self)
        ent1.grid(row = 0,column = 1,sticky = W)
        lab2 = Label(self,text = "Password:", font=TITLE_FONT)
        lab2.grid(row = 1,column = 0)
        ent2 = Entry(self,show = "*")
        ent2.grid(row = 1,column = 1,sticky = W)

        showServerState = Label(self,text="")
        showServerState.grid(row=3,column=0,sticky=W)

        button = Button(self,text = "登录",command=lambda: controller.showChatShow(), font=TITLE_FONT)
        button.grid(row = 2,column = 0,sticky = W)
        button2 = Button(self,text = "注册",command =None, font=TITLE_FONT)
        button2.grid(row = 2,column = 1,sticky = E)


    def log(self):
        """
        用来登录账户，登录成功，文本框提示成功，并自动跳转到接收消息界面
        """
        s1 = self.ent1.get()
        s2 = self.ent2.get()
        if s1 == 'freedom' and s2 == '123':
            self.lab3["text"] = "Confirm"
        else:
            self.lab3["text"] = "Error!"
        self.ent1.delete(0,len(s1))
        self.ent2.delete(0,len(s2))
    def register(self):
        self.destory()
        return True


class Client(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # for F in (Log, ChatShow):
        #     frame = F(container, self)
        #     self.frames[F] = frame
        #     frame.grid(row=0, column=0, sticky='nsew')
        # self.show_frame(Log)
        #加载登录窗口

        self.showLog()




    def showLog(self):
        tempFrame=Log(self.container,self)
        tempFrame.grid(row=0, column=0, sticky='nsew')
        tempFrame.tkraise()
        self.updateFrame()

    def showChatShow(self):
        tempFrame=ChatShow(self.container,self)
        tempFrame.grid(row=0, column=0, sticky='nsew')
        tempFrame.tkraise()
        self.geometry("150x500")
        self.updateFrame()

    def updateFrame(self):
        """主要是用来移动界面到屏幕中央"""
        self.update() # update window ,must do
        curWidth = self.winfo_reqwidth() # get current width
        curHeight = self.winfo_height() # get current height
        print(str(curWidth)+"fds"+str(curHeight))
        scnWidth,scnHeight = self.maxsize() # get screen width and height
        tmpcnf = '%dx%d+%d+%d'%(curWidth,curHeight,(scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
        self.geometry(tmpcnf)

if __name__ == "__main__":
    app = Client()
    app.mainloop()