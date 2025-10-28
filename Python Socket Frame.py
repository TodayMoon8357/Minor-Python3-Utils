import socket
import time

### PAYLOAD CREATION ###
hostname = ""
port = 0

#Custom Functions space here pls :)
#Note, make sure all functions have a variable for server response:
# def resend(serverresp):

#Signals must follow format of type,value,resp in dict (EXAMPLE: {'type':'turn','value':1,'resp':b'set'})
#type: 'turn','text'
#value: int(turnno.), str('capturetext')
#resp: bytes('text'), function
#Start your counts from 1,2,...,n
signals = []

### ~-~-~-~-~-~-~-~ ###
#Function: Gets all server messages with small timeout exception (DEFAULT: 1s)
def recvall (s,b=2048):
    d=t=""
    try: 
        while True:
            t = s.recv(b).decode()
            if not t: break
            print (t)
            d+=t
            time.sleep(0.25)
    except socket.timeout:
        return d

#Function Netcat
def nc(h,p):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((h,p))
    s.settimeout(1)
    count = 0
    while True:
        r = recvall(s)
        count+=1
        if r == None:
            s.close()
            break
        # FIX SIGNALS
        b = ""
        if signals:
            for sig in signals:
                try:
                    if sig['type'] == "turn" and count == sig['value'] or sig['type'] == "text" and sig['value'] in r:
                        b = sig['resp'](r) if callable(sig['resp']) else sig['resp']
                        s.sendall(b+b'\n')
                        break
                except:
                    b=""
                    continue
            if b:
                continue
        # FIX SIGNALS
        if r:
            b = input("> ").strip().encode('utf-8')
            s.sendall(b+b'\n')

if __name__ == "__main__":
    while True:
        print("#"+"-"*200+"#")
        nc(hostname,port)