import socket, select
from user import *

#还要改成From admin
def broadcaseData(sock, message):
    for socket in CONNECTIONLIST:
        print(message)
        if socket != serverSocket and socket != sock:
            try:
                socket.send(message.encode("utf8"))
            except:
                socket.close()
                CONNECTIONLIST.remove(socket)


def logOn(userName,userPasswd):
    if(userName == 'find' and userPasswd=='hello'):
        return  True
    else:
        return False
def register(userName,userPasswd):
    print('ok')
#从文件读取用户信息
def readUserInfoFromFile():
    return 0

def checkLog(data):
    """传入参数data的格式是userName@key,解出name和key，匹配数据库中的"""
    return  True

def checkRegister(data):
    """传入参数userName@key，查找数据库中是否已经存在当前用户名"""
    return  True


if __name__ == "__main__":
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
    # 建立连接的人
    loggers={}
    admins=[]
    #普通用户发送的操作码和对应的操作标记
    operations={"1_":1,"2_":2}
    print("server started on port " + str(PORT))

    while 1:
        readSockets, writeSockets, errorSockets = select.select(CONNECTIONLIST, [], [])
        for sock in readSockets:
            # new client connects
            if sock == serverInstance:
                sockfd, addr, = serverSocket.accept()
                CONNECTIONLIST.append(sockfd)
                anewuser=User()
                loggers[sockfd]=anewuser
                print("client %s %s connected" % addr)
                # broadcaseData(sockfd, "[%s:%s] entered room\n" % addr)
            else:
                try:
                    data = sock.recv(RECVBUFFER).decode("utf8")
                    #如果有name,那么肯定已经登录了，直接发送消息就可以
                    if loggers[sock].name in admins:
                        # 先不管图片了,只处理文字消息
                        broadcaseData(sock,data)
                    else:
                        if sock in loggers:
                            if data in operations:
                                loggers[sock].state = operations[data]
                            else:
                                #正在尝试登录
                                if loggers[sock].state == 1:
                                    #还需要添加成功以后，服务器往回发什么数据，或者添加在checkLog里
                                    checkLog(data)
                                #正在尝试注册
                                elif loggers[sock].state == 2:
                                    checkRegister(data)
                                #登录的普通用户无权限发送
                                else:
                                    print("You have no permission")
                        else:
                            print("No connection")




                except:
                    # broadcaseData(sock, "Client (%s, %s) is offline" % addr)
                    print(sock, "Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTIONLIST.remove(sock)
                    del loggers[sock]
                    continue
    serverSocket.close()
