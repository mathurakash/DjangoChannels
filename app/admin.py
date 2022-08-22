from django.contrib import admin
from .models import Chat,Group,User_Profile,User_Group
# Register your models here.

admin.site.register(Chat)
admin.site.register(Group)
admin.site.register(User_Profile)
admin.site.register(User_Group)