import hashlib

#hash password again and store to database
def sign_up(username, password, filename):
    if username == "":
        return False, "Please type your username"
    
    empty_hash = hashlib.sha256()
    empty_hash.update("".encode('utf-8'))
    if password == empty_hash.hexdigest():
        return False, "Please type your password"

    #check if username exists
    with open(filename, mode='r') as f:
        try:   
            for line in f.readlines():
                if line == "":
                    break
                username_data, password_data = line.split()    
                if username == username_data:
                    return False, "Username already exists"
        except Exception as e:
            return False, e

    #write user info to database
    with open(filename, mode='a') as f:
        try:    
            password_hash2 = hashlib.sha256()
            password_hash2.update(password.encode('utf-8'))
            f.write(username + ' ' + password_hash2.hexdigest() + '\n')
            return True, "Sign up successful!"
        except Exception as e:
            return False, e

#database lookup
def sign_in(username, password, filename):

    with open(filename, mode='r') as f:
        try:
            password_hash2 = hashlib.sha256()
            password_hash2.update(password.encode('utf-8'))                        
            for line in f.readlines():
                username_data, password_data = line.split()
                if username == username_data and password_hash2.hexdigest() == password_data:
                    return True, "Sign in successful!"
                elif username == username_data and password_hash2.hexdigest() != password_data:
                    return False, "Incorrect password"
            return False, "Username not found"                    
        except Exception as e:
            return False, e

def change_password(username, old_password, new_password, filename):
    
    with open(filename, mode='r+') as f:
        try:
            old_password_hash2 = hashlib.sha256()
            old_password_hash2.update(old_password.encode('utf-8'))        
            for line in f.readlines():
                username_data, password_data = line.split()    
                if username == username_data and old_password_hash2.hexdigest() == password_data:
                    f.seek(0)
                    content = f.read()
                    with open(filename, mode='w') as fw:
                        new_password_hash2 = hashlib.sha256()
                        new_password_hash2.update(new_password.encode('utf-8'))
                        fw.write(content.replace(username_data+' '+password_data, username+' '+new_password_hash2.hexdigest()))                    
                    return True, "Password successfully changed"
                elif username == username_data and old_password_hash2.hexdigest() != password_data:
                    return False, "Incorrect old password"
            return False, "Username not found"
        except Exception as e:
            return False, e

def store_RSA_key(username, public_key):

    with open('database/public_keys/'+username+'_public.pem', mode='wb') as f:
        try:
            f.write(public_key)
            return True, "Sign up successful!"
        except Exception as e:
            return False, e
