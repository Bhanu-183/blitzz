from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', views.index, name='index'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('my_blogs', views.my_blogs, name='my_blogs'),
    path('register',views.register, name='register'),
    path('addpost', views.addpost, name='addpost'),
    path('posts',views.posts, name='posts'),
    path('single_blog/<int:post_id>/<int:comment_id>/', views.single_blog, name='single_blog'),
    path('editpost/<int:post_id>',views.editpost,name='editpost'),
    path('delete_blog/<int:post_id>', views.delete_blog, name='delete_blog'),
    path('search_posts',csrf_exempt(views.search_posts),name='search_posts')
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

