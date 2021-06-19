from django import forms
from django.core import validators
from blog_app.models import Post,Author,Comment
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 're_password')
        help_texts = {
            'username': None,
            'email': None,
        }
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
        }
    def clean(self):
        all_clean = super().clean()
        
        p1 = all_clean['password']
        p2 = all_clean['re_password']
        if p1 != p2:
            raise forms.ValidationError("Passwords didn't match")

class AuthorForm(forms.ModelForm):
    class Meta():
        model = Author
        fields=(('qualification',))
        widgets={
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
        }

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title', 'text','hashtag','blog_img')
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'hashtag': forms.TextInput(attrs={'class': 'form-control'}),
            'text': Textarea(attrs={'cols': 118, 'rows': 15,'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta():
        model=Comment
        fields=(('text',))


