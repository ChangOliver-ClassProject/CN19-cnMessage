from printSection import *
from encryption import *
from util import *

# return hashed password
def input_password(message = "Password : "):
    password = input(message)
    password_hash = hashlib.sha256()
    password_hash.update(password.encode('utf-8'))

    return password_hash.hexdigest()

def non_login(s):
    while (True):
        printSection("NON_LOGIN")
        action = input(colored("Input: ", THEME_col, attrs=[THEME_attr]))

        username = ""
        if action == "0":
            username = input(colored("Username : ",THEME_col, attrs=[THEME_attr]))
            password = input_password(colored("Password : ", THEME_col, attrs=[THEME_attr]))
            s.sendall(pickle.dumps(packet(100, [username, password])))
            recv_pkt = pickle.loads(s.recv(RECV_SIZE))
            if recv_pkt.content[0] == True:
                public_key = gen_RSA_key(username)
                s.sendall(pickle.dumps(packet(103, [username, public_key])))
            else:
                print("\n%s" % (colored(recv_pkt.content[1], ERROR)))
                input(colored("Press \"Enter\" to continue...", NOTIFY_col, attrs=[NOTIFY_attr]))
                os.system("clear")
                continue                
        elif action == "1":           
            username = input(colored("Username : ", THEME_col, attrs=[THEME_attr]))
            password = input_password(colored("Password : ", THEME_col, attrs=[THEME_attr]))
            s.sendall(pickle.dumps(packet(101, [username, password])))
        elif action == "2":   
            username = input(colored("Username : ", THEME_col, attrs=[THEME_attr]))
            old_password = input_password(colored("Old Password : ", THEME_col, attrs=[THEME_attr]))
            new_password = input_password(colored("New Password : ", THEME_col, attrs=[THEME_attr]))
            s.sendall(pickle.dumps(packet(102, [username, old_password, new_password])))
        elif action == "3":
            printSection("EXIT")
            time.sleep(1)
            os.system("clear")
            return "EXIT", username
        else:
            print(colored("Unknown action\n", ERROR))
            return "NON_LOGIN", username

        recv_pkt = pickle.loads(s.recv(RECV_SIZE))
        if recv_pkt.content[0] == True:
            print("\n%s" % (colored(recv_pkt.content[1], SUCCESS)))
        else:
            print("\n%s" % (colored(recv_pkt.content[1], ERROR)))
        input(colored("Press \"Enter\" to continue...", NOTIFY_col, attrs=[NOTIFY_attr]))
        os.system("clear")
        
        if (recv_pkt.content[0] == True):
            return "LOGGED", username