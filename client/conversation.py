from printSection import *
from encryption import *
from util import *
from Thread_Controller import *

def conversation(s, username, recipient):
    t_controller = Thread_Controller(s, username, recipient)
    recv_thread = threading.Thread(target = t_controller.run, args = (s, ))
    recv_thread.start()

    while (True):
        printSection("MESSAGE", hasNewMessage = t_controller.messageDetector.hasNewMessage)
        action = input(colored("Input: ", THEME_col, attrs=[THEME_attr]))
        if action == "0":
            print(colored("Press \"Enter\" twice to send", NOTIFY_col))
            line = "a"
            message = ""
            while line != "":
                line = input(colored("> ", THEME_col, attrs=[THEME_attr]))
                message += '\t' + line + '\n'
            success, AES_key = query_AES(username, recipient)
            message = username + ":\n" + message
            message = AES_encrypt(message, AES_key)
            with open(t_controller.messageDetector.log_name, mode='ab') as f:
                try:
                    f.write(message)
                    f.write(b"\n")
                except Exception as e:
                    print(colored("Write local log:" + str(e), ERROR))
            data = [username, recipient, message]
            s.sendall(pickle.dumps(packet(300, data)))
            print(colored("Message sent!", SUCCESS))
            input(colored("Press \"Enter\" to continue...", NOTIFY_col, attrs=[NOTIFY_attr]))
            os.system("clear")
        elif action == "1":
            pathlist = input(colored("Input File Path:", THEME_col, attrs=[THEME_attr]))
            for path in pathlist.split():
                with open(path, mode="rb") as f:
                    try:
                        file_content = f.read()
                    except Exception as e:
                        print(colored("Send File:" + str(e), ERROR))
                filename = path.split('/')[-1]
                data = [username, recipient, filename, file_content]
                print("send file : " + filename + "")
                s.sendall(pickle.dumps(packet(301, data)))    
                time.sleep(0.5)      
        elif action == "2":
            print(colored("\n" + "=" * os.get_terminal_size().columns + "\n", THEME_col, THEME_hi))
            t_controller.lock()
            t_controller.messageDetector.hasNewMessage = False
            s.sendall(pickle.dumps(packet(302, [username, recipient])))
            while (t_controller.islocked()):
                pass
            print(colored("\n" + "=" * os.get_terminal_size().columns + "\n", THEME_col, THEME_hi))
            input(colored("Press \"Enter\" to continue...", NOTIFY_col, attrs=[NOTIFY_attr]))  
            os.system("clear")
        elif action == "3":
            s.sendall(pickle.dumps(packet(000, [username])))
            t_controller.terminate()
            time.sleep(0.5)
            recv_thread.join()
            return "LOGGED", username, recipient
        elif action == "4":
            s.sendall(pickle.dumps(packet(104, [username])))
            t_controller.terminate()
            time.sleep(0.5)
            recv_thread.join()
            return "NON_LOGIN", username, recipient
        else:
            print(colored("Unknown action\n", ERROR)) 
            return "MESSAGE", username, recipient 
