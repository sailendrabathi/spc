import requests
import sys
import json
import argparse
import getpass

parser = argparse.ArgumentParser()
parser.add_argument("--login", action='store_true')
parser.add_argument("--upload_file", action='store_true')
parser.add_argument("--set_url", action='store_true')
args = parser.parse_args()


loginurl = "http://127.0.0.1:8000/webclient/"
apilogin = "http://127.0.0.1:8000/apilogin/"
apiuploadfile = "http://127.0.0.1:8000/fileuploadapi/"
s = requests.session()

if args.set_url:
	ip = input("Server's ip and port(<ip>:<port>): ")
	apilogin = "http://" + ip + "/apilogin/"
	apiuploadfile = "http://" + ip + "/fileuploadapi"
	print("address set to :", ip)

if args.login:
	user = input("username: ")
	passwd = getpass.getpass("password: ")
	r = s.post(apilogin, data={'username':user, 'password':passwd})
	j = r.json()
	if j[0]["status"] == "successful":
		f = open("user.txt", 'w')
		f.write(user + '\n' + passwd)
		print("login successful")	
	else:
		f = open("user.txt",'w')
		f.write('')
		print("login failed, try again.")

if args.upload_file:
	folder = input("folder: ")
	name = input("name: ")
	file = input("file: ")
	r = s.post(apiuploadfile, data={'folder':folder, 'name':name, 'file':file})
	j = r.json()
	if j[0]["status"] == "successful":
		print("file upload successful")


#user = input("user :")
#passwd = input("pass: ")

#f = open("user.txt","w")
#f.write(user + "\n" +passwd)

#s= requests.session()
#r = s.get(apiurl, data={'username': user, 'password' : passwd})
#j= r.json()
#print(j[0]["detail"])
