import socket,select;

def broadcaseData(sock,message):
    for socket in CONNECTIONLIST:
        print(message)
        if socket != serverSocket and socket!= sock:
            try:
                socket.send(message.encode("utf8"))
            except:
                socket.close()
                CONNECTIONLIST.remove(socket)

if __name__ == "__main__":

    CONNECTIONLIST = []
    RECVBUFFER = 4096
    PORT=5000

    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(('', PORT))
    serverSocket.listen(100)

    CONNECTIONLIST.append(serverSocket)

    print("server started on port "+str(PORT))

    while 1:
        readSockets, writeSockets, errorSockets = select.select(CONNECTIONLIST, [], [])
        for sock in readSockets :
            if sock == serverSocket:
                sockfd, addr, = serverSocket.accept()
                CONNECTIONLIST.append(sockfd)
                print("client %s %s connected" % addr)
                broadcaseData(sockfd, "[%s:%s] entered room\n" % addr)
            else:
                try:
                    data=sock.recv(RECVBUFFER).decode("utf8")
                    if data:
                        broadcaseData(sock,"\r" + '<' + str(sock.getpeername()) + '> ' + data)
                except:
                    broadcaseData(sock,"Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTIONLIST.remove(sock)
                    continue
    serverSocket.close()