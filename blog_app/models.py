from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from django.urls import reverse
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=80)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    text = models.TextField(max_length=2000)
    hashtag=models.CharField(max_length=300,blank=False,null=True)
    blog_img=models.ImageField(upload_to='blog_imgs',blank=True)
    published_date = models.DateTimeField()
        
    def approve_comments(self):
        return self.comments.filter(approved_comments=True)

    

    def __str__(self):
        return self.title

class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    commented_date=models.DateTimeField(default=False)
    
    def __str__(self):
        return self.text

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    reply_date=models.DateTimeField(default=False)
    
    def __str__(self):
        return self.text
