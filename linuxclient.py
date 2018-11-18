import requests
import argparse
import getpass

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
ver = "not specified"
ip = "127.0.0.1:8000"


def checkauth(file):
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

if args.signup:
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

if args.config:
    user = input("username: ")
    passwd = getpass.getpass("password: ")
    passwd1 = getpass.getpass("confirm password: ")
    if passwd == passwd1:
        f = open("user.txt", 'w')
        f.write(user + '\n' + passwd)
    else:
        print("passwords did not match, try again")

if args.observe:
    dir_path = input("enter directory path: ")

if args.version:
    print(ver)

if args.server:
    address = ip.split(":")[0]
    port = ip.split(":")[1]
    print("address:", address)
    print("port:", port)

if args.login:
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

if args.logout:
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

if args.upload_file:
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

if args.upload_folder:
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

if args.delete_file:
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


if args.delete_folder:
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

if args.sync:
    print("not implemented")

if args.show_data:
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

if args.download_file:
    print("not implemented")

if args.download_folder:
    print("not implemented")

if args.info:
    print("not implemented")

# user = input("user :")
# passwd = input("pass: ")

# f = open("user.txt","w")
# f.write(user + "\n" +passwd)

# s= requests.session()
# r = s.get(apiurl, data={'username': user, 'password' : passwd})
# j= r.json()
# print(j[0]["detail"])
