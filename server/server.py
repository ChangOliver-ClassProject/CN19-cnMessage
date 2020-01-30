import sys
import os
import socket                
import select
import queue
import time
import pickle
from registration import *
from message import *
from util import *

MAX_CLINET = 10
USER_DATABASE = "database/user.txt"

def recvall(sock, timeout=1):
    sock.setblocking(0)
    total_data = []; data = ''; begin = time.time()
    while 1:
        if total_data and time.time()-begin > timeout:
            break
        elif time.time()-begin > timeout*2:
            break
        try:
            data = sock.recv(8192)
            if data:
                total_data.append(data)
                begin = time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    return b''.join(total_data)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
    print("Socket successfully created")
     
    server.bind(('', PORT))         
    print("socket binded to %s" % (PORT))

    server.listen(MAX_CLINET)      
    print("socket is listening")       
      
    inputs = [server]
    outputs = []
    return_queues = {}
    user_socket = {}

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for s in readable:
            if s is server: # new client
                connection, client_address = s.accept()
                connection.setblocking(0)
                inputs.append(connection)
                return_queues[connection] = queue.Queue()
                print("There is a new client : " + str(client_address))
                connection.send(b'Welcome')
            else:
                data = recvall(s)  
                if data:
                    data_variable = pickle.loads(data)         
                    print("%s, %s" % (data_variable.identifier, data_variable.content))

                    if (data_variable.identifier == 000):
                        s.sendall(pickle.dumps(packet(000, [True, "close thread"])))
                    if (data_variable.identifier == 100):
                        username, password = data_variable.content
                        success, message = sign_up(username, password, USER_DATABASE)
                        return_queues[s].put(packet(100, [success, message]))
                        if success:
                            user_socket[username] = s
                    elif (data_variable.identifier == 101):
                        username, password = data_variable.content
                        success, message = sign_in(username, password, USER_DATABASE)
                        return_queues[s].put(packet(101, [success, message]))
                        if success:
                            user_socket[username] = s
                    elif (data_variable.identifier == 102):
                        username, old_password, new_password = data_variable.content
                        success, message = change_password(username, old_password, new_password, USER_DATABASE)
                        return_queues[s].put(packet(102, [success, message]))                    
                        if success:
                            user_socket[username] = s
                    elif (data_variable.identifier == 103):
                        username, public_key = data_variable.content
                        success, message = store_RSA_key(username, public_key)
                        return_queues[s].put(packet(103, [success, message]))
                    elif (data_variable.identifier == 104): # log out
                        s.sendall(pickle.dumps(packet(000, [True, "close thread"])))
                        username = data_variable.content[0]
                        # del user_socket[username]
                        # TODO : maybe send back a packet
                    elif (data_variable.identifier == 200):
                        success, u_list = view_ulist(USER_DATABASE)
                        if success:
                            return_queues[s].put(packet(200, u_list))
                    elif (data_variable.identifier == 201):
                        username, recipient = data_variable.content
                        success, message = establish_connection(username, recipient, USER_DATABASE)
                        return_queues[s].put(packet(201, [success, message]))
                    elif (data_variable.identifier == 202):
                        username, recipient = data_variable.content
                        success, AES_key = get_encoded_AES(username, recipient)
                        return_queues[s].put(packet(202, [success, AES_key]))                        
                    elif (data_variable.identifier == 203):
                        recipient = data_variable.content[0]
                        success, public_key = get_public_key(recipient)
                        return_queues[s].put(packet(203, [success, public_key]))
                    elif (data_variable.identifier == 204):
                        username, recipient, encoded_AES = data_variable.content
                        success, message = store_encoded_AES(username, recipient, encoded_AES)
                        return_queues[s].put(packet(204, [success, message]))
                    elif (data_variable.identifier == 300):
                        username, recipient, message_to_sent = data_variable.content
                        success, message = send_message(username, recipient, message_to_sent)
                        # if success and (recipient in user_socket): 
                        #     return_queues[user_socket[recipient]].put(packet(303, []))
                        return_queues[s].put(packet(300, [success, message]))
                    elif (data_variable.identifier == 301):
                        username, recipient, filename, file_content = data_variable.content
                        success, message = check_recipient(username, recipient, user_socket)
                        if success:
                            user_socket[recipient].sendall(pickle.dumps(packet(301, [filename, file_content])))
                        return_queues[s].put(packet(301, [success, message]))
                    elif (data_variable.identifier == 302):
                        username, recipient = data_variable.content
                        success, message = view_log(username, recipient)
                        return_queues[s].put(packet(302, [success, message]))
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del return_queues[s]

        for s in writable:
            try:
                next_pkt = return_queues[s].get_nowait()
            except queue.Empty:
                outputs.remove(s)
            else:
                s.sendall(pickle.dumps(next_pkt))

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del return_queues[s]

if __name__ == '__main__':
    main()