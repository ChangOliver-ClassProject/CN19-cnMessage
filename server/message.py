import sys
import os
import hashlib

def decide_filename(username, recipient):
    if username < recipient:
        return ['database/log/' + username + '_' + recipient + '.log', 'database/AES_keys/' + username + '_' + recipient + '.key']
    else:
        return ['database/log/' + recipient + '_' + username + '.log', 'database/AES_keys/' + recipient + '_' + username + '.key']

def view_ulist(filename):
    with open(filename, mode='r') as f:
        try:
            u_list = []
            for line in f.readlines():
                u_list.append(line.split()[0])
            u_list.append('\n')
            return True, u_list
        except Exception as e:
            return False, e

def establish_connection(username, recipient, filename):
    if recipient == username:
        return False, "Recipient can't be yourself"

    log_path, key_path = decide_filename(username, recipient)

    if os.path.isfile(log_path):
        return True, "Esablishing Connection...."

    with open(filename, mode='r') as f:
        for line in f.readlines():
            if recipient == line.split()[0]:                        
                try :
                    flog = open(log_path, mode='a')
                    flog.close()
                    return True, "Esablishing Connection...."
                except Exception as e:
                    return False, e                
        return False, "Recipient is not a user"
    return False, "Fatal Error"

def view_log(username, recipient):
    
    log_path, key_path = decide_filename(username, recipient)

    with open(log_path, mode='rb') as f:
        try:
            data = [line for line in f.readlines()]
            return True, data
        except Exception as e:
            return False, e

def send_message(username, recipient, message):

    log_path, key_path = decide_filename(username, recipient)
    
    with open(log_path, mode='ab') as f:
        try:          
            f.write(message)
            f.write(b"\n")
            return True, "Message sent!"
        except Exception as e:
            return False, e

def check_recipient(username, recipient, user_socket):
    if recipient in user_socket:
        return True, "File sent!"
    else:
        return False, "Recipient not online!"

def get_public_key(recipient):

    with open('database/public_keys/'+ recipient + '_public.pem', mode='rb') as f:
        try:
            public_key = f.read()
            return True, public_key
        except Exception as e:
            return False, e

def get_encoded_AES(username, recipient):

    log_path, key_path = decide_filename(username, recipient)
    # print(log_path)
    # print(key_path)
    if os.path.isfile(key_path):
        with open(key_path, mode='rb') as f:
            try:
                key = f.read()
                return True, key
            except Exception as e:
                return False, e
    else:
        return False, ""

def store_encoded_AES(username, recipient, encoded_AES):

    log_path, key_path = decide_filename(username, recipient)
    with open(key_path, mode='wb') as f:
        try:
            f.write(encoded_AES)
            return True, "Connection Esablished!"
        except Exception as e:
            return False, e