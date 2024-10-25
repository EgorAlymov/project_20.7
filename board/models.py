from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.name}'


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField('Title', max_length=128)
    text = RichTextUploadingField('Text')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')

    def __str__(self):
        return f'{self.title}'


class Response(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1536)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    approved = models.BooleanField('Approved', null=True, blank=True)
    dateCreation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}'
    #- {self.datetime}