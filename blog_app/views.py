from django.shortcuts import render
from . import models
from blog_app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from blog_app.forms import UserForm,AuthorForm,PostForm
from . import forms

from django.views.generic import (TemplateView,ListView,DetailView)
# Create your views here.

is_login=False
user = ""

def index(request):
    global is_login
    search_flag=False
    if request.method=='POST':
        search_key = request.POST['search']
        search_key = search_key.lower()
        search_flag=True
        posts = Post.objects.filter(Q(title__icontains=search_key) | Q(hashtag__icontains=search_key))
        return render(request,'index.html',context={'posts':posts,'is_login':is_login,'search_flag':search_flag,'search_key':search_key})
    posts=Post.objects.order_by('-published_date')[:6]
    return render(request,'index.html',context={'posts':posts,'is_login':is_login})

def user_login(request):
    global is_login
    global user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                is_login = True
                return HttpResponseRedirect(reverse('my_blogs'))
            else:
                print("Username {} and password {}".format(username, password))
                return HttpResponse("Account not active")
        else:
            print("Login Failed")
            return HttpResponse('User Not Found')
    else:
        return render(request, 'login.html')
        

@login_required
def user_logout(request):
    global is_login
    logout(request)
    is_login=False
    return HttpResponseRedirect(reverse('index'))


def my_blogs(request):
    global is_login
    global user
    if not is_login:
        return HttpResponseRedirect(reverse('user_login'))
    else:
        posts = []
        author=''
        for person in Author.objects.all():
            if person.user.id == user.id:
                author=person
        for post in Post.objects.order_by('-published_date'):
            if post.author.id == author.id:
                posts.append(post)
        return render(request, 'myblogs.html', context={'is_login': is_login, 'posts': posts, 'user': user})
        

def register(request):
    global is_login
    global user
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        author_form = AuthorForm(data=request.POST)
        if user_form.is_valid() and author_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            author=author_form.save(commit=False)
            author.user = user
            author.save()
            return HttpResponseRedirect(reverse('user_login'))
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
        author_form=AuthorForm()
    return render(request,'register.html',context={'user_form':user_form,'author_form':author_form,'is_login':is_login})

def addpost(request):
    global user
    global is_login
    if is_login:
        if request.method == 'POST':
            post_form = PostForm(data=request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.published_date = timezone.localtime(timezone.now())
                for person in Author.objects.all():
                    if person.user.id == user.id:
                        post.author = person
                if 'blog_img' in request.FILES:
                    post.blog_img = request.FILES['blog_img']
                post.save()
                return HttpResponseRedirect(reverse(my_blogs))
        else:
            post_form = PostForm()
        return render(request, 'postform.html', context={'post_form': post_form,'is_login':is_login})
    else:
        return HttpResponseRedirect(reverse('user_login'))

def single_blog(request, post_id,comment_id):
    global is_login
    global user
    flag=False
    posts = Post.objects.all()
    single_post=''
    for post in posts:
        if post.id == post_id:
            single_post = post
    if is_login and str(user).lower() == str(single_post.author).lower():
        flag = True
    else:
        flag=False
    if request.method == 'POST' and request.POST.get('user_comment'):
        new_comment=Comment(post=single_post,author=user,text=request.POST['user_comment'],commented_date=timezone.localtime(timezone.now()))
        new_comment.save()
    elif request.method == 'POST' and request.POST.get('reply'):
        temp_comment = Comment.objects.get(id=comment_id)
        new_reply =Reply(comment=temp_comment,author=user,text=request.POST['reply'],reply_date=timezone.localtime(timezone.now()))
        new_reply.save()
    elif (request.method == 'POST'):
        Comment.objects.filter(id=comment_id).delete()

    comments = Comment.objects.filter(post=single_post)
    reply_list = []
    comment_list=[]
    for comment in comments:
        replies = Reply.objects.filter(comment=comment)
        reply_list.append(replies)
        comment_list.append(comment)
    finallist=zip(comment_list,reply_list)
    return render(request, 'singleblog.html', context={'post': single_post, 'is_login': is_login, 'flag': flag, 'finallist':finallist,'comments':comments})

def delete_blog(request, post_id):
    if request.method == 'POST':
        Post.objects.filter(id=post_id).delete()
        return HttpResponseRedirect(reverse('my_blogs'))
    
def editpost(request, post_id):
    global is_login
    posts = Post.objects.all()
    post = ''
    for item in posts:
        if item.id == post_id:
            post=item
    if request.method == 'POST':
        post.title=request.POST['title']
        post.text = request.POST['blog']
        post.hashtag = request.POST['hashtag']
        post.published_date = timezone.localtime(timezone.now())
        if 'blog_img' in request.FILES:
            post.blog_img=request.FILES['blog_img']
        post.save()
        return HttpResponseRedirect(reverse('my_blogs'))
    else:
        return render(request,'editpost.html',context={'post': post,'is_login':is_login})
            

def posts(request):
    global is_login
    search_flag=False
    if request.method=='POST':
        search_key = request.POST['search']
        search_key = search_key.lower()
        search_flag=True
        posts = Post.objects.filter(Q(title__icontains=search_key) | Q(hashtag__icontains=search_key))
        return render(request,'posts.html',context={'posts':posts,'is_login':is_login,'search_flag':search_flag})
    posts=Post.objects.all()
    return render(request,'posts.html',context={'posts':posts,'is_login':is_login})    

