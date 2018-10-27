# Generated by Django 2.1.2 on 2018-10-23 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webclient', '0008_auto_20181018_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bytes', models.TextField()),
                ('filename', models.CharField(max_length=255)),
                ('mimetype', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AlterField(
            model_name='file',
            name='media_file',
            field=models.FileField(default='', upload_to='webclient.FileModel/bytes/filename/mimetype'),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
