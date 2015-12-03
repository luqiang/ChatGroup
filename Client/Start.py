from tkinter import *
import socket
from tkinter import messagebox


TITLE_FONT = ("Arial", 12, "")
class ClientNet:
    def __init__(self,aHost,aPort):
        self.serverHost=aHost
        self.port=int(aPort)
        self.connected=False

    def connectServer(self):
        try:
            self.clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.clientSock.settimeout(10)
            self.clientSock.connect((self.serverHost,self.port))
            self.connected=True
            return True
        except Exception as err:
            print(err)
            print("unable to connect")
            self.connected=False


class ChatShow(Frame):
    """普通用户展示的"""

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

class AdminSHow(Frame):
    """admin用，根据客户端有关，如果只是普通用户，那么即便在客户端代码设置了也没用。"""
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        #scrollbar
        self.consoleShowScrollBar=Scrollbar(self)
        self.consoleShowScrollBar.pack(side=RIGHT,fill=Y)
        #console:text and pictures
        self.consoleShow = Listbox(self)
        self.consoleShow['yscrollcommand'] = self.consoleShowScrollBar.set
        self.consoleShowScrollBar['command'] = self.consoleShow.yview()
        self.consoleShow.pack(expand=1,fill=Y)
        self.ent=Entry(self)
        self.ent.pack(expand=1,fill=Y)



class Log(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        lab1 = Label(self,text = "User:", font=TITLE_FONT)
        lab1.grid(row = 0,column = 0,sticky = W)
        self.ent1 = Entry(self)
        self.ent1.insert(0,"test1")
        self.ent1.grid(row = 0,column = 1,sticky = W)
        lab2 = Label(self,text = "Password:", font=TITLE_FONT)
        lab2.grid(row = 1,column = 0)
        self.ent2 = Entry(self,show = "*")
        self.ent2.insert(0,"hello")
        self.ent2.grid(row = 1,column = 1,sticky = W)

        self.showServerState = Label(self,text="")
        self.showServerState.grid(row=3,column=0,sticky=W)

        # button = Button(self,text = "登录",command=lambda: controller.showChatShow(), font=TITLE_FONT)
        button = Button(self,text = "登录",command=lambda :self.log(controller.net.clientSock,controller), font=TITLE_FONT)
        button.grid(row = 2,column = 0,sticky = W)
        button2 = Button(self,text = "注册",command =None, font=TITLE_FONT)
        button2.grid(row = 2,column = 1,sticky = E)


    def log(self,sock,controller):
        """
        用来登录账户，登录成功，文本框提示成功，并自动跳转到接收消息界面
        """
        s1 = self.ent1.get()
        s2 = self.ent2.get()
        sock.sendall(str("1_"+s1+"@"+s2).encode("utf8"))
        self.showServerState['text']="正在登录，请等待。。。"
        data = sock.recv(2048).decode("utf8")
        print(data)
        if data:
            if data=='1':
                controller.showChatShow()
            elif data== '2':
                controller.showAdminShow()
            else:
                self.showServerState['text']='用户名或密码错误'
        self.ent2.delete(0,len(s2))
    def register(self):
        self.destory()
        return True

    def showLogInfor(self,text):
        self.showServerState['text']=text


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

        self.net=ClientNet("192.168.1.133",'5000')
        self.connectedSuccess=False
        self.showLog()



    def tryConnect(self,showTextView):
        if self.net.connectServer():
            showTextView.showLogInfor("服务器连接成功")
            self.connectedSuccess=True
        else:
            showTextView.showLogInfor("服务器连接失败")

    def showLog(self):
        tempFrame=Log(self.container,self)
        tempFrame.grid(row=0, column=0, sticky='nsew')
        tempFrame.tkraise()
        self.updateFrame()
        self.tryConnect(tempFrame)

    def showChatShow(self):
        tempFrame=ChatShow(self.container,self)
        tempFrame.grid(row=0, column=0, sticky='nsew')
        tempFrame.tkraise()
        self.geometry("150x500")
        self.updateFrame()
    def showAdminShow(self):
        tempFrame=AdminSHow(self.container,self)
        tempFrame.grid(row=0, column=0, sticky='nsew')
        tempFrame.tkraise()
        # self.geometry("150x500")
        self.updateFrame()
    def updateFrame(self):
        """主要是用来移动界面到屏幕中央"""
        self.update() # update window ,must do
        curWidth = self.winfo_reqwidth() # get current width
        curHeight = self.winfo_height() # get current height
        scnWidth,scnHeight = self.maxsize() # get screen width and height
        tmpcnf = '%dx%d+%d+%d'%(curWidth,curHeight,(scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
        self.geometry(tmpcnf)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.net.clientSock.close()
        app.destroy()

if __name__ == "__main__":
    app = Client()
    app.mainloop()
