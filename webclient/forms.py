from django.contrib.auth.models import User
from django import forms

from webclient.models import Folder, File


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['name', 'media_file']