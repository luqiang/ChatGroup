from tkinter import *
import socket,threading,_thread,time
from queue import Queue,Empty
TITLE_FONT = ("Arial", 12, "")



def position(self):
    self.master.withdraw()
    self.screen_width = self.master.winfo_screenwidth()
    self.screen_height = self.master.winfo_screenheight()
    # self.master.resizable(False,False) # 固定尺寸，不可变
    self.master.update_idletasks()   # 显示正常窗口的关键语句
    self.master.deiconify()   # 重新显示
    self.master.withdraw() # TK
    curWidth = self.master.winfo_reqwidth() # get current width
    curHeight = self.master.winfo_height() # get current height
    scnWidth,scnHeight = self.master.maxsize() # get screen width and height
    tmpcnf = '%dx%d+%d+%d'%(curWidth,curHeight,(scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
    self.master.geometry(tmpcnf)
    self.master.deiconify()

class ThreadTask(threading.Thread):

    def __init__(self, queue, sock):
        threading.Thread.__init__(self)
        self.queue=queue
        self.sock = sock

    def run(self):
        while 1:
            try:
                clientMsg = self.sock.recv(4096).decode('utf8')
                if not clientMsg:
                    continue
                else:
                    print("i got :"+clientMsg)
                    self.queue.put(clientMsg)
            except socket.timeout:
                pass



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

    def sendData(self,data):
        self.clientSock.sendall(data.encode('utf8'))
class AdminShow(Frame):
    """admin用，根据客户端有关，如果只是普通用户，那么即便在客户端代码设置了也没用。"""
    def __init__(self,master,controller):
        Frame.__init__(self,master)
        self.controller = controller
        self.pack()
        self.frameLeftTop = Frame(self)
        self.frameLeftMid = Frame(self)
        self.frameLeftBottom = Frame(self)

        self.scrollbar = Scrollbar(self.frameLeftTop)
        self.chatShow = Listbox(self.frameLeftTop,width=70,height=18,yscrollcommand=self.scrollbar.set)
        self.chatShow.yview_moveto(1.0)
        self.scrollbar.config(command=self.chatShow.yview)
        self.scrollbar.pack(side="right", fill=Y)
        self.chatShow.pack(side="left")
        self.frameLeftTop.pack()

        # self.sendPic= Button(self.frameLeftMid)
        # self.sendPic['text'] = '发送图片'
        if controller.isAdmin:
            self.messageInput= StringVar()
            self.messageSend = Entry(self.frameLeftBottom,textvariable=self.messageInput)
            self.messageSend['width'] = 70
            self.messageSend.bind('<Return>',self.sendMessage)
            self.messageSend.pack(fill=X)
            self.frameLeftBottom.pack()

        position(self)
        self.queue = Queue()
        th=ThreadTask(self.queue,controller.net.clientSock)
        th.start()
        self.master.after(100,self.processQueue)


    def sendMessage(self,event):
        tempMessage=self.messageSend.get().strip(" ")
        if tempMessage:
            print("local: "+tempMessage)
            self.controller.net.sendData(tempMessage)
            self.messageSend.delete(0,len(self.messageSend.get()))
        else:
            print("不能发送空消息")

    def processQueue(self):
        try:
            msg = self.queue.get(0)
            print(msg)
            self.chatShow.insert(END, msg)
            self.chatShow.yview_moveto(1.0)
        except Empty:
            pass
        self.master.after(100, self.processQueue)
class Log(Frame):
    def __init__(self,master, controller):
        Frame.__init__(self,master)
        self.pack()
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

        position(self)



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
            self.ent2.delete(0,len(s2))
            if data=='1':
                controller.isAdmin = False
                controller.showAdminShow(self.master)
            elif data== '2':
                controller.isAdmin = True
                controller.showAdminShow(self.master)
            else:
                self.showServerState['text']= '用户名或密码错误'
    def register(self):
        self.destory()
        return True

    def showLogInfor(self,text):
        self.showServerState['text']=text


class Client():
    def __init__(self):
        self.root=Tk()
        self.net=ClientNet("192.168.1.133",'5000')
        self.connectedSuccess=False
        self.app= Log(self.root,self)
        self.isAdmin = False
        #检测服务器连接
        self.tryConnect(self.app)

        self.root.mainloop()


    def tryConnect(self,showTextView):
        if self.net.connectServer():
            showTextView.showLogInfor("服务器连接成功")
            self.connectedSuccess=True
        else:
            showTextView.showLogInfor("服务器连接失败")


    def showAdminShow(self,temproot):
        self.root.destroy()
        self.root2=Tk()
        self.tempFrame = AdminShow(self.root2,self)
        self.root2.mainloop()

runClient=Client()