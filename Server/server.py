import socket, select
from user import *

#还要改成From admin
def broadcaseData(sock, message):
    for socket in CONNECTIONLIST:
        if socket != serverSocket:
            try:
                print("broad"+message)
                socket.send(message.encode("utf8"))
            except:
                print(sock, "Client (%s, %s) is offline" % addr)
                socket.close()
                CONNECTIONLIST.remove(socket)


def logOn(userName,userPasswd):
    if userName == 'find' and userPasswd=='hello':
        return True
    else:
        return False
def register(userName,userPasswd):
    print('ok')
def readUserInfoFromFile():
    """从文件读入用户信息，目前存储的格式：
        userName key isAdmin lastRead
    """
    fin=open("users", "r")
    while 1:
        line=fin.readline()
        if not line:
            break
        tempuser = line.split(" ")
        users[tempuser[0]] = tempuser[1:4]
    fin.close()
    return 0


def checkLog(data,sock):
    """
    @return value False:用户名或者密码错误 True:成功
    :param data: 传入参数data的格式是userName@key,解出name和key，匹配数据库中的
    """
    temp=data.split("@")
    aName=temp[0]
    aKey=temp[1]
    if aName not in users:
        print("no user")
        return False
    if users[aName][0] == aKey:
        loggers[sock].name=aName
        loggers[sock].logged= True

        if(users[aName][1]=='1'):
            loggers[sock].isAdmin = True
            return 2
        else:
            return 1
    else:
        return 0

def checkRegister(data):
    """传入参数userName@key，查找数据库中是否已经存在当前用户名"""
    temp=data.split("@")
    aName = temp[0]
    aKey = temp[1]
    if aName in users:
        return '0'
    tempContent=[aKey,'0','0']
    users[aName]=tempContent
    #write content to file
    f=open('users','a')
    f.write(aName+' '+aKey+' '+'0'+' '+'0')
    f.close()
    return '1'


if __name__ == "__main__":
    # 建立连接的人
    loggers={}
    #从硬盘读取的已经注册的用户信息,以名字作为key，以其他的信息作为[]的键值
    users={}
    #读用户信息
    readUserInfoFromFile()

    # save normal users
    CONNECTIONLIST = []
    # save admin user
    RECVBUFFER = 4096
    PORT = 5000

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(('', PORT))
    serverSocket.listen(100)

    # add serverClient
    serverInstance = User()
    serverInstance.connection=serverSocket

    CONNECTIONLIST.append(serverSocket)

    print("server started on port " + str(PORT))

    while 1:
        readSockets, writeSockets, errorSockets = select.select(CONNECTIONLIST, [], [])
        for sock in readSockets:
            # new client connects
            if sock == serverSocket:
                sockfd, addr, = serverSocket.accept()
                CONNECTIONLIST.append(sockfd)
                anewuser=User()
                loggers[sockfd]=anewuser
                print("client %s %s connected" % addr)
                # broadcaseData(sockfd, "[%s:%s] entered room\n" % addr)
            else:
                try:
                    data = sock.recv(RECVBUFFER).decode("utf8")
                    #仍然有问题，没法判断用户退出了。不过貌似系统会自己维护sock的连接，超时会自动判断except
                    if not data:
                        raise Exception("null data")
                    #如果有name,那么肯定已经登录了，直接发送消息就可以
                    if loggers[sock].isAdmin:
                        # 先不管图片了,只处理文字消息
                        data="admin " + loggers[sock].name + " say: " + data
                        broadcaseData(sock, data)
                        print("admin say :" + data)
                    else:
                        if sock in loggers:
                            #尝试登录
                            if data[0:2]=='1_':
                                print("logging")
                                temp1=checkLog(data[2:],sock)

                                sock.sendall(str(temp1).encode("utf8"))
                            #注册
                            elif data[0:2]=='2_':
                                print('registering')
                                temp2 = checkRegister(data[2:])
                                sock.sendall(str(temp2).encode('utf8'))
                            else:
                                print("no code")
                        else:
                            print("No connection")
                except Exception as err :
                    print(err)
                    # broadcaseData(sock, "Client (%s, %s) is offline" % addr)
                    print(sock, "Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTIONLIST.remove(sock)
                    del loggers[sock]
                    continue
    serverSocket.close()
