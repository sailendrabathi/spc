import os

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import View
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from spc1.settings import MEDIA_URL
from webclient.serializers import FileSerializer, FolderSerializer
from .models import Folder, File
from django.views import generic
from .forms import UserForm, FolderForm, FileForm
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.files import File as file1
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'webclient/login.html')
    all_folders1= Folder.objects.select_related().filter(user=request.user)
    all_folder=all_folders1.first()
    all_folders = Folder.objects.select_related().filter(folder=all_folder.id)
    folder_id = all_folder.id
    # all_folders=all_folder.get(pk=11)
    context = {'folder_id':folder_id,'all_folders': all_folders}
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
        return render(request, 'webclient/login.html')
    folder = Folder.objects.get(pk=folder_id)
    folder.delete()
    folders = Folder.objects.filter(user=request.user)
    all_folders=folders.first()
    return render(request, 'webclient/index.html', {'folder_id':all_folders.id,'all_folders': all_folders})

def create_file(request,folder_id) :
    if not request.user.is_authenticated:
        return render(request, 'webclient/login.html')
    else:
        form = FileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            folder2 = form.save(commit=False)
            # folder1.user = request.user
            folder2.folder = get_object_or_404(Folder, pk=folder_id)
            folder2.save()
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

class FileDelete(DeleteView):
    def dispatch(self, request, *args, **kwargs):
        # here you can make your custom validation for any particular user
        if not request.user.is_authenticated:
            return render(self.request , 'webclient/login.html')
        return super().dispatch(request, *args, **kwargs)
    model = File
    success_url = reverse_lazy('webclient:index')

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
                context = {'folder_id':folder_id,'all_folders': all_folders}
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
    # permission_classes = (permissions.AllowAny,)
    def get(self,request):
        folder = Folder.objects.all()
        serializer = FolderSerializer(folder, many=True)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        username = request.POST.get('username')
        passwd = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username,email,passwd)
        user.first_name = "fn"
        user.last_name = "ln"
        user.save()
        folder = Folder.objects.select_related().filter(user = user.id)
        serializer = FolderSerializer(folder,many = True)
        return Response(serializer.data)

class loginapi(APIView):

    def post(self,request,*args):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            folder = Folder.objects.select_related().filter(user=user.id)
            serializer = FolderSerializer(folder, many=True)
            return Response([{"status":"successful"}])
        return Response([{"status":"not successful"}])

class fileuploadapi(APIView):
    def post(selfself,request):
        folder = request.data["folder"]
        name = request.data["name"]
        file = request.data["file"]
        folder1 = Folder.objects.select_related().filter(id=folder).first()
        up_file1 = open(file, "wb+")
        up_file = file1(up_file1)
        f = File()
        f.name = name
        f.folder = folder1
        f.media_file.save(os.path.basename(up_file1.name),up_file,save=True)
        f.save()
        return Response([{"status":"successful"}])