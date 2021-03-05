import hashlib
import os

selfpath=""

def get_md5_info():
    login_name=input("User Name:")
    login_pwd=input("Code:\033[8m")
    print("\033[0m")
    md5_name=hashlib.md5(login_name.title().encode("utf-8")).hexdigest()
    md5_pwd=hashlib.md5(login_pwd.encode("utf-8")).hexdigest()
    return (login_name,md5_name,md5_pwd)

def createUser(login_name,md5_name,md5_pwd):
    if (login_name.isdigit()):
        print("\033[1;31mName cannot be digit\033[0m")
        return False
    if (not os.path.exists(selfpath+"/Users")):
        os.mkdir(selfpath+"/Users")
    if (os.path.exists(selfpath+"/Users/"+md5_name)):
        print("\033[1;31mAccount already exists\033[0m")
        return False
    fd = open(selfpath+"/Users/"+md5_name,mode="w")
    fd.write(md5_pwd)
    fd.close()
    return True

def auth(login_name,md5_name,md5_pwd):
    if (os.path.exists(selfpath+"/Users/"+md5_name)):
        fd = open(selfpath+"/Users/"+md5_name,mode="r")
        if (fd.read()==md5_pwd):
            return login_name
        else:
            print("\033[1;31mIncorrect password\033[0m")
    else:
        print("\033[35mNo such user\033[0m")

def safes(path):
    global selfpath
    selfpath=path
    while(True):
        if (os.path.exists(selfpath+"/Users")):
            (login_name,md5_name,md5_pwd)=get_md5_info()
            x=auth(login_name,md5_name,md5_pwd)
            if (x):
                return login_name
        else:
            print("\033[4;31mNo exists User,create account\033[0m")
            (login_name,md5_name,md5_pwd)=get_md5_info()
            createUser(login_name,md5_name,md5_pwd)
            print("\033[4mAccount has been created,please login\033[0m")

def addUser():
    print("\033[4mCreating account\033[0m")
    (login_name,md5_name,md5_pwd)=get_md5_info()
    if (createUser(login_name,md5_name,md5_pwd)):
        print("\033[4mAccount has been created\033[0m")

def changeAccount(login_name,mode):
    login_pwd=input("Current Code:\033[8m")
    print("\033[0m")
    md5_pwd=hashlib.md5(login_pwd.encode("utf-8")).hexdigest()
    md5_name=hashlib.md5(login_name.title().encode("utf-8")).hexdigest()
    x=auth(login_name,md5_name,md5_pwd)
    if (x):
        os.remove(selfpath+"/Users/"+md5_name)
        if (mode):
            login_pwd=input("New Code:\033[8m")
            print("\033[0m")
            md5_pwd=hashlib.md5(login_pwd.encode("utf-8")).hexdigest()
            createUser(login_name,md5_name,md5_pwd)
            print("\033[4mPassword is changed\033[0m")
            return True
        else:
            print("\033[4;31mDelete Account(\033[35m"+login_name+"\033[4;31m) is success\033[0m")
            return True
    else:
        print("\033[1;31mWrong Code,please try again\033[0m")

def changePwd(login_name):
    return changeAccount(login_name,True)

def deleteAccount(login_name):
    return changeAccount(login_name,False)