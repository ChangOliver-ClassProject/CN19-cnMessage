from non_login import *
from logged_in import *
from conversation import *
from printSection import *
from util import *


def sign_up(s, username, password):
    password_hash = hashlib.sha256()
    password_hash.update(password.encode('utf-8'))
    s.sendall(pickle.dumps(packet(100, [username, password_hash.hexdigest()])))
    recv_pkt = pickle.loads(s.recv(RECV_SIZE))
    print("%s, %s" % (recv_pkt.identifier, recv_pkt.content))
    success, message = recv_pkt.content
    return success, message

def sign_in(s, username, password):
    password_hash = hashlib.sha256()
    password_hash.update(password.encode('utf-8'))
    s.sendall(pickle.dumps(packet(101, [username, password_hash.hexdigest()])))
    recv_pkt = pickle.loads(s.recv(RECV_SIZE))
    print("%s, %s" % (recv_pkt.identifier, recv_pkt.content))
    success, message = recv_pkt.content
    return success, message

####################################################

def main():
    STATE = "NON_LOGIN"
    s = socket.socket()          
    s.connect((SERVER_IP, PORT))           
    welcome_message = str(s.recv(RECV_SIZE))[2:-1]

    os.system("clear")

    printSection("NON_LOGIN", welcomeMessage = True)

    while (True):
        if (STATE == "EXIT"):
            break
        elif (STATE == "NON_LOGIN"):
            time.sleep(0.8)
            os.system("clear")
            STATE, username = non_login(s)         
        elif (STATE == "LOGGED"):
            time.sleep(0.8)
            os.system("clear")
            STATE, username, recipient = logged_in(s, username)
        elif (STATE == "MESSAGE"):
            os.system("clear")         
            STATE, username, recipient = conversation(s, username, recipient)

    # close the connection 
    s.close()
    
if __name__ == '__main__':
    main()