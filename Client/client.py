import socket, select, string, sys

def prompt():
    sys.stdout.flush()

if __name__ == "__main__":
    if(len(sys.argv)<3):
        print("Usage: python client.py hostname port")
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(10)

    try:
        s.connect((host,port))
    except Exception as err:
        print(err)
        print("unable to connect")
        sys.exit()

    print("connect success")
    prompt()

    while 1:
        rlist = [sys.stdin, s]
        readList, wirteList, errorList = select.select(rlist,[], [])
        for sock in readList:
            if sock == s:
                data = sock.recv(4096).decode("utf8")
                if not data:
                    print("Disconnected from chat server")
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    prompt()
            else:
                msg = sys.stdin.readline()
                s.send(msg.encode("utf8"))
                prompt()