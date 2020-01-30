from printSection import *
from encryption import *
from util import *

def logged_in(s, username):
    while (True):
        recipient = ""
        printSection("LOGGED")
        action = input(colored("Input: ", THEME_col, attrs=[THEME_attr]))
        if action == "0":
            s.sendall(pickle.dumps(packet(200, [])))
            recv_pkt = pickle.loads(s.recv(RECV_SIZE))
            print(colored("\n[User List]", THEME_col, attrs=[THEME_attr]))
            print(colored('\n'.join(recv_pkt.content), CONTENT))
            recipient = input(colored("Recipient Username : ", THEME_col, attrs=[THEME_attr]))

            s.sendall(pickle.dumps(packet(201, [username, recipient])))
            recv_pkt = pickle.loads(s.recv(RECV_SIZE))                
            
            if recv_pkt.content[0] == True:
                print("%s" % (colored(recv_pkt.content[1], NOTIFY_col)))
                success, AES_key = query_AES(username, recipient)
                if success:
                    print(colored("Connection established!", SUCCESS))
                    input(colored("Press \"Enter\" to continue...", NOTIFY_col, attrs=[NOTIFY_attr]))
                    os.system("clear")
                    return "MESSAGE", username, recipient     
                else:
                    print(colored("Fetching keys...", NOTIFY_col))
                    s.sendall(pickle.dumps(packet(202, [username, recipient])))
                    recv_pkt = pickle.loads(s.recv(RECV_SIZE))
                    if recv_pkt.content[0] == True:
                        encoded_AES = recv_pkt.content[1]
                        AES_key = decode_AES(encoded_AES, username)
                        store_AES_key(AES_key, username, recipient)
                        print(colored("Connection established!", SUCCESS))
                        input(colored("Press \"Enter\" to continue...", NOTIFY_col, attrs=[NOTIFY_attr]))
                        os.system("clear")
                        return "MESSAGE", username, recipient
                    else:               
                        AES_key = gen_AES_key(username, recipient)
                        s.sendall(pickle.dumps(packet(203, [recipient])))
                        recv_pkt = pickle.loads(s.recv(RECV_SIZE))
                        recipient_public_key = recv_pkt.content[1]
                        encoded_AES = encode_AES(AES_key, recipient_public_key)
                        s.sendall(pickle.dumps(packet(204, [username, recipient, encoded_AES])))                  
            else:
                print("%s" % (colored(recv_pkt.content[1], ERROR)))
                input(colored("Press \"Enter\" to continue...", NOTIFY_col, attrs=[NOTIFY_attr]))
                os.system("clear")
                continue             
        elif action == "1":
            s.sendall(pickle.dumps(packet(104, [username])))
            print(colored("Logging out....", NOTIFY_col))
            return "NON_LOGIN", username, recipient
        else:
            print(colored("Unknown action\n",  ERROR))
            return "LOGGED", username, recipient       

        recv_pkt = pickle.loads(s.recv(RECV_SIZE))
        if recv_pkt.content[0] == True:
            print("%s" % colored(recv_pkt.content[1], SUCCESS))
        else:
            print("%s" % colored(recv_pkt.content[1], ERROR))
        input(colored("Press \"Enter\" to continue...", NOTIFY_col, attrs=[NOTIFY_attr]))
        os.system("clear")

        if (recv_pkt.content[0] == True):
            return "MESSAGE", username, recipient