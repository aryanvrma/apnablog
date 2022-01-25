from django.contrib import admin
from django.urls import path, include
from . import views
from apnablog import settings


   
urlpatterns = [
    path('postcomment', views.comment, name="comment"),
    path('', views.blogHome, name="bloghome"),
    
    path('<str:slug>', views.blogPost, name="blogPost"),

]




