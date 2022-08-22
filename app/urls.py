from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.view_name, name="view_name"),
    path('logout/',views.logout,name="logout"),
    path('index/',views.index,name="index"),
    path('<str:group_name>/',views.chatbox,name="chatbox"),
    path('delete_group/<int:pk>/',views.delete_group,name="delete_group"),
    path('profile/<int:pk>/',views.profile,name="profile"),
    path('join_group/<int:pk>/',views.add_group,name="add_group")
    
]
