import os
import hashlib
from threading import Condition
import requests
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Folder, File
from .forms import UserForm, FolderForm, FileForm
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.files import File as file1
from . import e_d
import hashlib
fu = open("urls.txt")
ip = ""
for line in fu:
    for word in line.split():
        ip = word
        break
    break
apiauth = "http://" + ip + "/apiauth/"
apiregister = "http://" + ip + "/apiregister/"
apilogin = "http://" + ip + "/apilogin/"
apilogout = "http://" + ip + "/apilogout/"
apiuploadfolder = "http://" + ip + "/folderuploadapi/"
apiuploadfile = "http://" + ip + "/fileuploadapi/"
apideletefile = "http://" + ip + "/filedeleteapi/"
apideletefolder = "http://" + ip + "/folderdeleteapi/"
apishowdata = "http://" + ip + "/apishowdata/"
apisync = "http://" + ip + "/apisync/"
apidownloadfile = "http://" + ip + "/apidownloadfile/"
apidownloadfolder = "http://" + ip + "/apidownloadfolder/"
# Create your views here.
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# def md5sum(f):

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'webclient/login.html')
    all_folders1= Folder.objects.select_related().filter(user=request.user)
    all_folder=all_folders1.first()
    all_folders = Folder.objects.select_related().filter(folder=all_folder.id)
    folder_id = all_folder.id
    files = File.objects.select_related().filter(folder_id=folder_id)
    # all_folders=all_folder.get(pk=11)
    context = {'folder_id':folder_id,'all_folders': all_folders,'files':files}
    return render(request,'webclient/index.html',context)

def detail(request, folder_id):
    if not request.user.is_authenticated:
        return render(request, 'webclient/login.html')
    user = request.user
    # folder = get_object_or_404(Folder, pk=folder_id)
    folders = Folder.objects.select_related().filter(folder_id=folder_id)
    files = File.objects.select_related().filter(folder_id=folder_id)
    return render(request, 'webclient/detail.html', {'folder_id':folder_id,'folders': folders, 'user': user, 'files':files})


def create_folder(request , folder_id):
    if not request.user.is_authenticated:
        return render(request, 'webclient/login.html')
    if request.user.id != get_object_or_404(Folder , pk=folder_id).user_id:
        return render(request , 'webclient/noaccess.html' , {'error_msg' : "You are not allowed to access this folder"})
    form = FolderForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        folder1 = form.save(commit=False)
        folder1.user = request.user
        folder1.folder=get_object_or_404(Folder , pk=folder_id)
        folder1.save()
        folders= Folder.objects.select_related().filter(folder_id=folder1.id)
        return render(request, 'webclient/detail.html', {'folder_id':folder1.id,'folders':folders})
    context = {
        "form": form,
    }
    return render(request, 'webclient/folder_form.html', context)

def update(request , pk) :
    if not request.user.is_authenticated:
        return render(request, 'webclient/login.html')
    return redirect('webclient:folder_update', pk= pk)

class update_folder(UpdateView):
    model = Folder
    fields = ['name']

    def dispatch(self, request, *args, **kwargs):
        # here you can make your custom validation for any particular user
        if not request.user.is_authenticated:
            return render(self.request , 'webclient/login.html')
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return render(self.request, 'webclient/login.html')
        folder = form.save(commit=False)
        folder.save()
        return redirect('webclient:detail', folder_id=folder.id)

def delete_folder(request, folder_id):
    if not request.user.is_authenticated:
        return render(request, 'webclient/lo   gin.html')
    folder = Folder.objects.get(pk=folder_id)
    folder.delete()
    folders = Folder.objects.select_related().filter(user=request.user)
    all_folders=folders.first()
    all_folders1=Folder.objects.select_related().filter(folder=all_folders)
    return render(request, 'webclient/index.html', {'folder_id':all_folders.id,'all_folders': all_folders1})

def create_file(request,folder_id) :
    if not request.user.is_authenticated:
        return render(request, 'webclient/login.html')
    else:
        form = FileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            folder2 = form.save(commit=False)
            # folder1.user = request.user
            folder2.folder = get_object_or_404(Folder, pk=folder_id)
            # folder2.md5sum = md5(folder2.media_file.url)
            folder2.save()
            # folder2.md5sum = md5("http://127.0.0.1"+folder2.media_file.url)
            # folder2.save()
            folders = Folder.objects.select_related().filter(folder_id=folder_id)
            return render(request, 'webclient/detail.html', {'folder_id': folder_id, 'folders': folders})
        context = {
            "form": form,
        }
        return render(request, 'webclient/folder_form.html', context)




class FileUpdate(UpdateView):
    model = File
    fields = ['folder','name','media_file']
    def dispatch(self, request, *args, **kwargs):
        # here you can make your custom validation for any particular user
        if not request.user.is_authenticated:
            return render(self.request , 'webclient/login.html')
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        file = form.save(commit=False)
        file.save()
        return redirect('webclient:detail', folder_id=file.folder_id)

def FileDelete(request , pk):
    if not request.user.is_authenticated:
        return render(request, 'webclient/login.html')
    file=File.objects.select_related().filter(pk=pk)
    file.delete()
    all_folder1 = Folder.objects.select_related().filter(user=request.user.id)
    all_folder = all_folder1.first()
    folder_id = all_folder.id
    all_folders = Folder.objects.select_related().filter(folder=all_folder.id)
    context = {'folder_id': folder_id, 'all_folders': all_folders}
    return render(request, 'webclient/index.html', context)

class UserFormView(View):
    form_class = UserForm
    template_name = 'webclient/registration_form.html'
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self, request):
        form=self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    Folder.objects.create(user=request.user, name="root")
                    return redirect('webclient:index')
        return render(request, self.template_name, {'form': form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                all_folder1 = Folder.objects.select_related().filter(user=request.user.id)
                all_folder = all_folder1.first()
                folder_id = all_folder.id
                all_folders=Folder.objects.select_related().filter(folder=all_folder.id)
                files = File.objects.select_related().filter(folder=all_folder.id)
                context = {'folder_id':folder_id,'all_folders': all_folders,'files':files}
                return render(request, 'webclient/index.html', context)
            else:
                return render(request, 'webclient/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'webclient/login.html', {'error_message': 'Invalid login'})
    return render(request, 'webclient/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'webclient/login.html', context)

class register(APIView):
    def post(self,request,*args,**kwargs):
        username = request.data["username"]
        passwd = request.data["password"]
        email = request.POST.data["email"]
        user = User.objects.create_user(username,email,passwd)
        user.save()
        login(request,user)
        f = Folder(name="root", user=request.user)
        f.save()
        return Response([{"status": "successful"}])

class authapi(APIView):
    def post(self,request,*args):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                return Response([{"status": "successful"}])
            else:
                return Response([{"status": "account deleted"}])
        return Response([{"status": "not successful"}])


class loginapi(APIView):
    def post(self,request,*args):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response([{"status":"successful"}])
            else:
                return Response([{"status":"account deleted"}])
        return Response([{"status":"not successful"}])

class logoutapi(APIView):
    def post(self,request):
        logout(request)
        return Response([{"status":"successful"}])

class fileuploadapi(APIView):
    def post(self,request):
        folder = request.data["folder"]
        name = request.data["name"]
        file = request.data["file"]
        folder1 = Folder.objects.select_related().filter(id=folder).first()
        f = open("pass.txt", 'r')
        schema = []
        for line in f:
            for word in line.split():
                schema.append(word)
                break
        if schema[0] == "AES-CBC":
            key = hashlib.sha256(schema[1].encode('utf-8')).digest()
            e_d.encrypt_file_aes(key, file, "up_file.enc")
        elif schema[0] == "AES-ECB":
            key = hashlib.sha256(schema[1].encode('utf-8')).digest()
            e_d.encrypt_file_aes1(key, file, "up_file.enc")
        elif schema[0] == "AES-OFB":
            key = hashlib.sha256(schema[1].encode('utf-8')).digest()
            e_d.encrypt_file_aes2(key, file, "up_file.enc")
        up_file1 = open("up_file.enc", "rb")
        up_file = file1(up_file1)
        f1 = File.objects.select_related().filter(name=name, folder=folder).first()
        if f1:                                                                       ###ask whether to overwrite or to skip upload
            return Response([{"status":"file_already_exists","id":f1.id}])
        f = File()
        f.name = name
        f.folder = folder1
        f.media_file.save(os.path.basename(f.name), up_file, save=True)
        f.md5sum=md5(file)
        f.save()
        os.remove("up_file.enc")
        return Response([{"status":"successful"}])

def UF(folder,id,name,user):
    fold = Folder(user=user,folder=Folder.objects.select_related().filter(pk=id).first(),name=name)
    fold.save()
    list = os.listdir(folder)
    for element in list:
        ele = folder+element
        if os.path.isfile(ele):
            f1 = open("pass.txt", 'r')
            schema = []
            for line in f1:
                for word in line.split():
                    schema.append(word)
                    break
            if schema[0] == "AES-CBC":
                key = hashlib.sha256(schema[1].encode('utf-8')).digest()
                e_d.encrypt_file_aes(key, ele, "up_file.enc")
            elif schema[0] == "AES-ECB":
                key = hashlib.sha256(schema[1].encode('utf-8')).digest()
                e_d.encrypt_file_aes1(key, ele, "up_file.enc")
            elif schema[0] == "AES-OFB":
                key = hashlib.sha256(schema[1].encode('utf-8')).digest()
                e_d.encrypt_file_aes2(key, file, "up_file.enc")
            up_file1 = open("up_file.enc","rb")
            up_file = file1(up_file1)
            f=File()
            f.name = element
            f.folder=fold
            f.media_file.save(os.path.basename(element),up_file,save=True)
            f.md5sum = md5(ele)
            f.save()
            os.remove("up_file.enc")
        elif os.path.isdir(ele):
            UF(ele,fold.id,element,user)
        else:
            fold1 = Folder(user=user, folder=Folder.objects.select_related().filter(pk=fold.id).first(), name=element)
            fold1.save()
    return [{"status":"successful"}]

class folderuploadapi(APIView):
    def post(self,request):
        folder = request.data["folder"]
        name = request.data["name"]
        ftu = request.data["ftu"]
        username = request.data["user"]                                         ###ask whether to overwrite or to skip upload
        user = User.objects.get(username=username)
        f = Folder.objects.select_related().filter(folder=folder, name=name).first()
        if f:
            return Response([{"status":"folder_already_exists","id":f.id}])
        UF(ftu,folder,name,user)
        return Response([{"status":"successful"}])

def sdf(folder):
    d = {}
    d2 = {}
    files = File.objects.select_related().filter(folder=folder)
    for file in files:
        d2[file.name]=file.id
    folders = Folder.objects.select_related().filter(folder=folder)
    for folde in folders:
        d[folde.name +"("+str(folde.id)+")"] = sdf(folde)
    dict = {}
    dict["folders"]=d
    dict["files"]=d2
    return dict

class showdataapi(APIView):
    def post(self, request):
        username = ""
        f = open("user.txt")
        for line in f:
            for word in line.split():
                username = word
                break
            break
        user = User.objects.get(username=username)
        all_folders = Folder.objects.select_related().filter(user=user).first()
        dic = []
        dic1 = {}
        dic1[all_folders.name + "(" + str(all_folders.id) + ")"] = sdf(all_folders.id)
        dic.append(dic1)
        return Response(dic)

class filedeleteapi(APIView):
    def post(self, request):
        username = ""
        f = open("user.txt")
        for line in f:
            for word in line.split():
                username = word
                break
            break
        user = User.objects.get(username=username)
        all_folders = Folder.objects.select_related().filter(user=user)
        fil = request.data["file"]
        f = File.objects.select_related().filter(pk=fil).first()
        if f and f.folder in all_folders:
            file = request.data["file"]
            file1 = File.objects.select_related().filter(pk=file).first()
            file1.delete()
            return Response([{"status":"successful"}])
        else:
            return Response([{"status":"no_file"}])

class folderdeleteapi(APIView):
    def post(self,request):
        username = ""
        f = open("user.txt")
        for line in f:
            for word in line.split():
                username = word
                break
            break
        user = User.objects.get(username=username)
        all_folders = Folder.objects.select_related().filter(user=user)
        folder = request.data["folder"]
        f = Folder.objects.select_related().filter(pk=folder).first()
        if f in all_folders:
            f.delete()
            return Response([{"status":"successful"}])
        else:
            return Response([{"status":"no_folder"}])

class filedownloadapi(APIView):
    def post(self,request):
        username = ""
        f = open("user.txt")
        for line in f:
            for word in line.split():
                username = word
                break
            break
        user = User.objects.get(username=username)
        all_folders = Folder.objects.select_related().filter(user=user)
        file = request.data["file"]
        pa = request.data["path"]
        f = File.objects.select_related().filter(pk=file).first()
        if f and f.folder in all_folders:
            url = f.media_file.url
            fu = open("urls.txt")
            ip = ""
            for line in fu:
                for word in line.split():
                    ip = word
                    break
                break
            url1 = "http://"+ip+url
            s = requests.session()
            r = s.get(url1)
            out = open("down_file.enc", "wb")
            out.write(r.content)
            out.close()
            f1 = open("pass.txt", 'r')
            schema = []
            for line in f1:
                for word in line.split():
                    schema.append(word)
                    break
            if schema[0] == "AES-CBC":
                key = hashlib.sha256(schema[1].encode('utf-8')).digest()
                e_d.decrypt_file_aes(key, "down_file.enc", pa+f.name)
            elif schema[0] == "AES-ECB":
                key = hashlib.sha256(schema[1].encode('utf-8')).digest()
                e_d.decrypt_file_aes1(key, "down_file.enc", pa+f.name)
            elif schema[0] == "AES-OFB":
                key = hashlib.sha256(schema[1].encode('utf-8')).digest()
                e_d.decrypt_file_aes2(key, "down_file.enc", pa + f.name)
            os.remove("down_file.enc")
            return Response([{"status": "successful"}])
        else:
            return Response([{"status":"no_file"}])

def FD(folder,path):

    fold = Folder.objects.select_related().filter(pk=folder).first()
    flist = Folder.objects.select_related().filter(folder=fold)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    for element in flist :
        FD(element.id , path+"/"+element.name+"/")
    filelist = File.objects.select_related().filter(folder=folder)
    for ele in filelist:
        s = requests.session()
        url = ele.media_file.url
        fu = open("urls.txt")
        ip = ""
        for line in fu:
            for word in line.split():
                ip = word
                break
            break
        url1 = "http://"+ip+url
        r = s.get(url1)
        out = open("down_file.enc","wb")
        out.write(r.content)
        out.close()
        f1 = open("pass.txt", 'r')
        schema = []
        for line in f1:
            for word in line.split():
                schema.append(word)
                break
        if schema[0] == "AES-CBC":
            key = hashlib.sha256(schema[1].encode('utf-8')).digest()
            e_d.decrypt_file_aes(key, "down_file.enc", path+ele.name)
        elif schema[0] == "AES-ECB":
            key = hashlib.sha256(schema[1].encode('utf-8')).digest()
            e_d.decrypt_file_aes1(key, "down_file.enc", path+ele.name)
        elif schema[0] == "AES-OFB":
            key = hashlib.sha256(schema[1].encode('utf-8')).digest()
            e_d.decrypt_file_aes2(key, "down_file.enc", path + ele.name)
        os.remove("down_file.enc")
    return Response([{"status": "successful"}])

class folderdownloadapi(APIView):
    def post(self,request):
        username = ""
        f = open("user.txt")
        for line in f:
            for word in line.split():
                username = word
                break
            break
        user = User.objects.get(username=username)
        folder = request.data["folder"]
        pa = request.data["path"]
        folders = Folder.objects.select_related().filter(user=user)
        f = Folder.objects.select_related().filter(pk=folder).first()
        if f in folders:
            FD(folder , pa+f.name+"/")
            return Response([{"status":"successful"}])
        else:
            return Response([{"status":"no_folder"}])


def __sync1__(a,b):
    next=Condition()
    username = ""
    f = open("user.txt")
    for line in f:
        for word in line.split():
            username = word
            break
        break
    user = User.objects.get(username=username)
    folders = Folder.objects.select_related().filter(folder=a)
    files = File.objects.select_related().filter(folder=a)
    if(a.var=='1'):
        next.wait()
    else:
        next.acquire()
        a.var='1'
        a.save()
    dirs = os.listdir(b)
    s = requests.session()
    dirs1=[]
    dirs2=[]
    for f in dirs:
        if os.path.isfile(os.path.join(b,f)):
            dirs2.append(f)
        else:
            dirs1.append(f)
    for fold in folders:
        if dirs1:
            if fold.name in dirs1:
                __sync1__(fold,b+fold.name+"/")
                dirs.remove(fold)
            else :

                r = s.post(apidownloadfolder, data={'folder': fold.id,'path':b})
        else:
            s.post(apidownloadfolder, data={'folder': fold.id,'path':b})
    if dirs1:
        for f1 in dirs1:
            r=s.post(apiuploadfolder,data={'ftu':b+f1+"/",'folder':a.id,'name':f1,'user':user})
    for file in files:
        if dirs2:
            if file.name in dirs2:
                if file.md5sum==md5(os.path.join(b,file.name)):
                    dirs2.remove(file.name)
                    continue
            else :
                r=s.post(apideletefile,data={'file':file.id})
                r=s.post(apiuploadfile,data={'file':os.path.join(b,file.name),'folder':a.id,'name':file.name})
                dirs2.remove(file.name)
        else:
            r=s.post(apidownloadfile,data={'file':file.id,'path':b})
    if dirs2:
        for f2 in dirs2:
            r=s.post(apiuploadfile, data={'file': b+f2, 'folder': a.id, 'name': f2})
    a.var=0
    a.save()
    next.release()


def __sync2__(a, b):
    next=Condition()
    username = ""
    f = open("user.txt")
    for line in f:
        for word in line.split():
            username = word
            break
        break
    user = User.objects.get(username=username)
    folders = Folder.objects.select_related().filter(folder=a)
    files = File.objects.select_related().filter(folder=a)
    if(a.var==1):
        next.wait()
    else:
        next.acquire()
        a.var=1
        a.save()
    dirs = os.listdir(b)
    s = requests.session()
    dirs1 = []
    dirs2 = []
    for f in dirs:
        if os.path.isfile(os.path.join(b, f)):
            dirs2.append(f)
        else:
            dirs1.append(f)
    for fold in folders:
        if dirs1:
            if fold.name in dirs1:
                __sync1__(fold, b + fold.name+"/")
                dirs.remove(fold.name)
            else:
                r = s.post(apideletefolder, data={'folder': fold.id})
        else:
            s.post(apideletefolder, data={'folder': fold.id})
    if dirs1:
        for f1 in dirs1:
            s.post(apiuploadfolder, data={'ftu': b+f1+"/", 'folder': a.id, 'name': f1, 'user': user})
    for file in files:
        if dirs2:
            if file.md5sum==md5(os.path.join(b,file.name)):
                dirs2.remove(file.name)
                continue
            else :
                r=s.post(apideletefile,data={'file':file.id})
                r=s.post(apiuploadfile,data={'file':os.path.join(b,file.name),'folder':a.id,'name':file.name})
                dirs2.remove(file.name)
        else:
            s.post(apideletefile, data={'file': file.id})
    if dirs2:
        for f2 in dirs2:
            s.post(apiuploadfile, data={'file': os.path.join(b, f2), 'folder': a.id, 'name': f2})
    a.var = 0
    a.save()
    next.release()



class apisync(APIView):
    def post(self,request):
        username = ""
        f = open("user.txt")
        for line in f:
            for word in line.split():
                username = word
                break
            break
        user = User.objects.get(username=username)
        folder=request.data["folder"]
        f1 = request.data["f"]
        opt = request.data["option"]
        folders = Folder.objects.select_related().filter(pk=f1).first()
        if opt=="1":
            __sync1__(folders,folder)
            return Response([{"status": "successful"}])
        if opt=="2":
            __sync2__(folders,folder)
            return Response([{"status": "successful"}])
        else:
            return Response([{"status": "choose a valid option"}])



class apiupdate(APIView):
    def post(self,request):
        new_schema = request.data["schema"]
        new_key = request.data["key"]
        username = ""
        f = open("user.txt")
        for line in f:
            for word in line.split():
                username = word
                break
            break
        user = User.objects.get(username=username)
        folders = Folder.objects.select_related().filter(user=user)
        for folder in folders:
            files = File.objects.select_related().filter(folder=folder)
            for file in files:
                s = requests.session()
                url = file.media_file.url
                fu = open("urls.txt")
                ip = ""
                for line in fu:
                    for word in line.split():
                        ip = word
                        break
                    break
                url1 = "http://" + ip + url
                r = s.get(url1)
                out = open("temp.enc", "wb")
                out.write(r.content)
                out.close()
                f1 = open("pass.txt", 'r')
                schema = []
                for line in f1:
                    for word in line.split():
                        schema.append(word)
                        break
                if schema[0] == "AES-CBC":
                    key = hashlib.sha256(schema[1].encode('utf-8')).digest()
                    e_d.decrypt_file_aes(key, "temp.enc", "temp1.dec")
                elif schema[0] == "AES-ECB":
                    key = hashlib.sha256(schema[1].encode('utf-8')).digest()
                    e_d.decrypt_file_aes1(key, "temp.enc", "temp1.dec")
                elif schema[0] == "AES-OFB":
                    key = hashlib.sha256(schema[1].encode('utf-8')).digest()
                    e_d.decrypt_file_aes2(key, "temp.enc", "temp1.dec")
                if new_schema == "AES-CBC":
                    new_key1 = str(new_key)
                    new_key1 = hashlib.sha256(new_key1.encode('utf-8')).digest()
                    e_d.encrypt_file_aes(new_key1, "temp1.dec", "temp3.enc")
                elif new_schema == "AES-ECB":
                    new_key1 = str(new_key)
                    new_key1 = hashlib.sha256(new_key1.encode('utf-8')).digest()
                    e_d.encrypt_file_aes1(new_key1, "temp1.dec", "temp3.enc")
                elif new_schema == "AES-OFB":
                    new_key1 = str(new_key)
                    new_key1 = hashlib.sha256(new_key1.encode('utf-8')).digest()
                    e_d.encrypt_file_aes2(new_key1, "temp1.dec", "temp3.enc")
                up_file1 = open("temp3.enc", "rb")
                up_file = file1(up_file1)
                f = File()
                f.name = file.name
                f.folder = folder
                f.media_file.save(os.path.basename(file.name), up_file, save=True)
                f.md5sum = md5("temp1.dec")
                f.save()
                file.delete()
                os.remove("temp.enc")
                os.remove("temp1.dec")
                os.remove("temp3.enc")

        return Response([{"status": "successful"}])

def status(folderser,folder):
    folders = Folder.objects.select_related().filter(folder=folderser)
    files = File.objects.select_related().filter(folder=folderser)
    dirs = os.listdir(folder)
    # s = requests.session()
    dirs1 = []
    dirs2 = []
    insync={}
    for f in dirs:
        if os.path.isfile(os.path.join(folder, f)):
            dirs2.append(f)
        else:
            dirs1.append(f)
    for fold in dirs1:
        if Folder.objects.select_related().filter(name=fold):
            insync[fold]=status(Folder.objects.select_related().filter(name=fold).first(),folder+fold+"/")
        else:
            insync[fold]="not in-sync"
    for file in dirs2:
        if File.objects.select_related().filter(name=file):
            f=File.objects.select_related().filter(name=file).first()
            if f.md5sum==md5(folder+file):
                insync[file]="in-sync"
            else:
                insync[file]="not in-sync"
        else:
            insync[file] = "not in-sync"
    return insync

def status1(folderser,folder):
    folders = Folder.objects.select_related().filter(folder=folderser)
    files = File.objects.select_related().filter(folder=folderser)
    dirs = os.listdir(folder)
    # s = requests.session()
    dirs1 = []
    dirs2 = []
    insync={}
    for f in dirs:
        if os.path.isfile(os.path.join(folder, f)):
            dirs2.append(f)
        else:
            dirs1.append(f)
    for fold in folders:
        if fold.name in dirs1:
            insync[fold.name]=status(fold,folder+fold.name+"/")
        else:
            insync[fold.name]="not in-sync"
    for file in files:
        if file.name in files:
            if file.md5sum==md5(folder+file.name):
                insync[file.name]="in-sync"
            else:
                insync[file.name]="not in-sync"
        else:
            insync[file.name] = "not in-sync"
    return insync

class apistatus(APIView):
    def post(self, request):
        username = ""
        f = open("user.txt")
        for line in f:
            for word in line.split():
                username = word
                break
            break
        user = User.objects.get(username=username)
        folder = request.data["folder"]
        f1 = request.data["f"]
        folders = Folder.objects.select_related().filter(pk=f1,user=user).first()
        r=status(folders,folder)
        r1=status1(folders,folder)
        result=[]
        result.append(r)
        result.append(r1)
        return Response(result)






