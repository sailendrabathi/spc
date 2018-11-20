import requests
import argparse
import getpass
import os.path
# import sys
# sys.path.insert(0, 'E-D/')
# import e_d

parser = argparse.ArgumentParser()
parser.add_argument("--signup", action='store_true')
parser.add_argument("--login", action='store_true')
parser.add_argument("--upload_file", action='store_true')
parser.add_argument("--set_url", action='store_true')
parser.add_argument("--logout", action='store_true')
parser.add_argument("--upload_folder", action='store_true')
parser.add_argument("--delete_file", action='store_true')
parser.add_argument("--delete_folder", action='store_true')
parser.add_argument("--sync", action='store_true')
parser.add_argument("--show_data", action='store_true')
parser.add_argument("--config", action='store_true')
parser.add_argument("--observe", action='store_true')
parser.add_argument("--version", action='store_true')
parser.add_argument("--server", action='store_true')
parser.add_argument("--info", action='store_true')
parser.add_argument("--download_file", action='store_true')
parser.add_argument("--download_folder", action='store_true')
parser.add_argument("--list", action='store_true')
parser.add_argument("--dump")
parser.add_argument("--update", action='store_true')
parser.add_argument("--update1")

args = parser.parse_args()

apiauth = "http://127.0.0.1:8000/apiauth/"
apiregister = "http://127.0.0.1:8000/apiregister/"
apilogin = "http://127.0.0.1:8000/apilogin/"
apiuploadfolder = "http://127.0.0.1:8000/folderuploadapi/"
apilogout = "http://127.0.0.1:8000/apilogout/"
apideletefile = "http://127.0.0.1:8000/filedeleteapi/"
apideletefolder = "http://127.0.0.1:8000/folderdeleteapi/"
apiuploadfile = "http://127.0.0.1:8000/fileuploadapi/"
apisync = "http://127.0.0.1:8000/apisync/"
apishowdata = "http://127.0.0.1:8000/apishowdata/"
apidownloadfile = "http://127.0.0.1:8000/apidownloadfile/"
apidownloadfolder = "http://127.0.0.1:8000/apidownloadfolder/"
s = requests.session()  # add session time also(to be done in django and delete user.txt or write to null)

dir_path = ""
ver = "1.0"
ip = "127.0.0.1:8000"


def checkauth(file):
    if not os.path.isfile(file):
        return False

    with open(file, 'r') as f1:
        lines = f1.read().splitlines()
        if len(lines) == 2:
            user = lines[0]
            passwd = lines[1]
            r = s.post(apiauth, data={'username': user, 'password': passwd})
            j = r.json()
            if j[0]["status"] == "successful":
                return True
            else:
                return False
        else:
            return False


if args.set_url:
    ip = input("Server's ip and port(format - <ip>:<port>): ")
    apiauth = "http://" + ip + "/apiauth/"
    apiregister = "http://" + ip + "/apiregiste/r"
    apilogin = "http://" + ip + "/apilogin/"
    apilogout = "http://" + ip + "/apilogout/"
    apiuploadfolder = "http://" + ip + "/folderuploadapi"
    apiuploadfile = "http://" + ip + "/fileuploadapi/"
    apideletefile = "http://" + ip + "/filedeleteapi/"
    apideletefolder = "http://" + ip + "/folderdeleteapi/"
    apishowdata = "http://" + ip + "/apishowdata/"
    apisync = "http://" + ip + "/apisync/"
    apidownloadfile = "http://" + ip + "/apidownloadfile/"
    apidownloadfolder = "http://" + ip + "/apidownloadfolder/"

    print("address set to :", ip)

elif args.signup:
    user = input("username: ")
    email = input("email: ")
    p123 = email.split('@')
    if len(p123) == 2:
        p1 = p123[0]
        p23 = p123[1]
        p23_1 = p23.split('.')
        if p1 == "" or p23 == "" or p1 == " " or p23 == " ":
            print("invalid email format")
        elif len(p23_1) > 1:
            p2 = p23_1[0]
            p3 = p23_1[1]
            if p2 == "" or p3 == "" or p2 == " " or p3 == " ":
                print("invalid email format")
            else:
                passwd = getpass.getpass("password: ")
                passwd1 = getpass.getpass("confirm password: ")
                if passwd == passwd1:
                    r = s.post(apiregister, data={'username': user, 'email': email, 'password': passwd})
                    j = r.json()
                    if j[0]["status"] == "successful":
                        print("signup successful")
                    else:
                        print("signup failed, try again")
                else:
                    print("passwords did not match, try again")
        else:
            print("invalid email format")
    else:
        print("invalid email format")

elif args.config:
    user = input("username: ")
    passwd = getpass.getpass("password: ")
    passwd1 = getpass.getpass("confirm password: ")
    if passwd == passwd1:
        f = open("user.txt", 'w')
        f.write(user + '\n' + passwd)
    else:
        print("passwords did not match, try again")

elif args.observe:
    dir_path = input("enter directory path: ")

elif args.version:
    print(ver)

elif args.server:
    address = ip.split(":")[0]
    port = ip.split(":")[1]
    print("address:", address)
    print("port:", port)

elif args.login:
    user = input("username: ")
    passwd = getpass.getpass("password: ")
    r = s.post(apilogin, data={'username': user, 'password': passwd})
    j = r.json()
    if j[0]["status"] == "successful":
        f = open("user.txt", 'w')
        f.write(user + '\n' + passwd)  # encrypt and pass to file(preferred)
        print("login successful")
    elif j[0]["status"] == "account deleted":
        f = open("user.txt", 'w')
        f.write('')
        print("login failed, account has been deleted")
    else:
        f = open("user.txt", 'w')
        f.write('')
        print("login failed, try again.")

elif args.logout:
    if checkauth("user.txt"):
        conf = input("logout?(Y/n): ")
        if conf == "Y" or conf == "y":
            r = s.post(apilogout)
            j = r.json()
            if j[0]["status"] == "successful":
                f = open("user.txt", 'w')
                f.write('')
                print("logged out")
            else:
                print("logout failed, try again")
        elif conf == "N" or conf == "n":
            print("logout cancelled")
        else:
            print("Invalid option, please choose between (Y/n)")
    else:
        print("logout failed, user logged out already")

elif args.upload_file:
    if checkauth("user.txt"):
        folder = input("parent folder id in destination: ")
        name = input("name of the file in server: ")
        file = input("path of the file to upload: ")
        r = s.post(apiuploadfile, data={'folder': folder, 'name': name, 'file': file})
        j = r.json()
        if j[0]["status"] == "successful":
            print("file upload successful")
        else:
            print("file upload failed, try again")
    else:
        print("no user logged in, please log in ")

elif args.upload_folder:
    if checkauth("user.txt"):
        folder = input("parent folder id in destination: ")
        name = input("name of the folder in server: ")
        ftu = input("path of the folder to upload(add '/' at the end): ")
        username = ""
        f = open("user.txt")
        for line in f:
            for word in line.split():
                username = word
                break
            break
        r = s.post(apiuploadfolder, data={'folder': folder, 'name': name, 'ftu': ftu,'user': username})
        j = r.json()
        if j[0]["status"] == "successful":
            print("folder upload successful")
        else:
            print("folder upload failed, try again")
    else:
        print("no user logged in, please log in")

elif args.delete_file:
    if checkauth("user.txt"):
        file = input("id of the file to delete: ")
        r = s.post(apideletefile, data={'file': file})
        j = r.json()
        if j[0]["status"] == "successful":
            print("file delete successful")
        else:
            print("file delete failed, try again")
    else:
        print("no user logged in, please log in ")


elif args.delete_folder:
    if checkauth("user.txt"):
        folder = input("id of the folder to delete: ")
        r = s.post(apideletefolder, data={'folder': folder})
        j = r.json()
        if j[0]["status"] == "successful":
            print("folder delete successful")
        else:
            print("folder delete failed, try again")
    else:
        print("no user logged in, please log in ")

elif args.sync:
    print("not implemented")

elif args.show_data:
    if checkauth("user.txt"):
        r = s.post(apishowdata)
        j = r.json()
        if j[0]["status"] == "successful":
            dict1 = j[0]["folders"]
            dict2 = j[0]["files"]
            print(dict1)
            print(dict2)
        else:
            print("fetching data failed, try again")
    else:
        print("no user logged in, please log in ")

elif args.download_file:
    if checkauth("user.txt"):
        file = input("id of the file to download: ")
        print("downloading file...")
        r = s.post(apidownloadfile, data={'file': file})        #change the algo in views.py
        j = r.json()
        if j[0]["status"] == "successful":
            print("file download successful")
        else:
            print("file download failed, try again")
    else:
        print("no user logged in, please log in ")


elif args.download_folder:
    if checkauth("user.txt"):
        folder = input("id of the folder to download: ")
        print("downloading folder...")
        r = s.post(apidownloadfolder, data={'folder': folder})
        j = r.json()
        if j[0]["status"] == "successful":                  #change the algo in views.py
            print("folder download successful")
        else:
            print("folder download failed, try again")
    else:
        print("no user logged in, please log in ")

elif args.info:
    print("not implemented")

elif args.list:
    print("Supported encryption schemes:")
    print("1. AES-CBC")                                                 #need a third scheme
    print("2. RSA")
    print("3. ------")

elif args.update:
    schema = input("Schema: ")
    if schema == "RSA":
        pub_key = input("Public Key(4096 bits): ")
        pri_key = input("Private Key(4096 bits): ")                     ##encrypt and pass
        f = open("pass.txt", 'w')
        f.write(schema + '\n' + pub_key + '\n' + pri_key)               ##sync is required
        print("update completed")
    elif schema == "AES-CBC":
        key = input("Key: ")
        f = open("pass.txt", 'w')
        f.write(schema + '\n' + key)
        print("update completed")
    else:
        print("Invalid Schema, use \"spc list\" to list supported schemes")

elif args.dump:
    if os.path.isfile("pass.txt"):
        f = open(args.dump, 'w')
        f0 = open("pass.txt", 'r')
        for line in f0:
            f.write(line)
        print("dump completed")
        print(args.dump, "now contains the schema data")
    else:
        print("no schema data to dump, please specify update the schema")

elif args.update1:
    if os.path.isfile(args.update1):
        f0 = open("pass.txt", 'w')                                      ##sync is required
        f = open(args.update1, 'r')
        for line in f:                                                  ##encrypt amd pass (only pass.txt)
            f0.write(line)
        print('update completed')
    else:
        print("update failed, no such file", args.update1)


# user = input("user :")
# passwd = input("pass: ")

# f = open("user.txt","w")
# f.write(user + "\n" +passwd)

# s= requests.session()
# r = s.get(apiurl, data={'username': user, 'password' : passwd})
# j= r.json()
# print(j[0]["detail"])
