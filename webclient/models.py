from db_file_storage.model_utils import delete_file_if_needed, delete_file
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.urls import reverse
class FileModel(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)

class Folder(models.Model) :
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    folder = models.ForeignKey('self',on_delete=models.CASCADE,null=True,related_name='children')
    name=models.CharField(max_length=250)
    var = models.CharField(max_length=1, default='0')
    def get_absolute_url(self):
        return reverse('webclient:detail',kwargs={'pk':self.pk})
    def __str__(self):
        return self.name

class File(models.Model) :
    folder= models.ForeignKey(Folder, on_delete=models.CASCADE)
    name: str = models.CharField(max_length=250)
    media_file = models.FileField(default='',upload_to='webclient.FileModel/bytes/filename/mimetype',)
    md5sum = models.CharField(max_length=250,default='0')
    var = models.CharField(max_length=1,default='0')
    def get_absolute_url(self):
        return reverse('webclient:detail',kwargs={'pk':self.folder.id})
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'media_file')
        super(File, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        delete_file(self, 'media_file')
        super(File, self).delete(*args, **kwargs)

