from ntpath import join
from django.shortcuts import redirect, render
from.models import Chat,Group,User_Profile,User_Group
from datetime import datetime,date
from django.contrib.auth.models import User
from .myforms import UserProfileForm
from django.http import JsonResponse

from django.contrib.auth import logout as auth_logout
# Create your views here.

def index(request):
    if request.method=="GET":
        mygroup=Group.objects.filter(created_by=request.user.username)
        print(mygroup,'==================mygroup======================')
        # user=User.objects.get(username=request.user.username)
        user_profile=User_Profile.objects.get(user=User.objects.get(username=request.user.username))
        print(user_profile,'==================user======================')
        joingroup=User_Group.objects.filter(user=user_profile)
        print(joingroup,'==================joingroup======================')
        allgroup=Group.objects.all()
        return render(request,'app/index.html',{'allgroup':allgroup,'mygroup':mygroup,'joingroup':joingroup})
    else:
        if request.POST.get('searchinput'):
            search=request.POST.get('searchinput')
            print(search,'==================Search======================')
            group=Group.objects.filter(name__icontains=search)
            allgroup=Group.objects.all()
            return render(request,'app/search.html',{'group':group,'allgroup':allgroup})
        else: 
            print(request.POST.get("group_name"),'====================================')
            obj=Group()
            obj.name=request.POST.get("group_name")
            obj.image=request.FILES['image']
            obj.background=request.FILES['background']
            obj.created_by=request.POST.get("created_by")
            obj.timestamp=datetime.now()
            obj.save()


        
        
    return redirect('index')




def chatbox(request,group_name):
    if request.method=="GET":
        print("groupname.....",group_name)
        group = Group.objects.filter(name=group_name).first()

        chats=[]
        if group:
            chats = Chat.objects.filter(group=group)
        else:
            group=Group(name=group_name)
            group.save()
        
        mygroup=Group.objects.filter(created_by=request.user.username)
        print(mygroup,'==================mygroup======================')
        # user=User.objects.get(username=request.user.username)
        user_profile=User_Profile.objects.get(user=User.objects.get(username=request.user.username))
        print(user_profile,'==================user======================')
        joingroup=User_Group.objects.filter(user=user_profile)
        print(joingroup,'==================joingroup======================')
        allgroup=Group.objects.all()
        user=User.objects.get(username=request.user.username)
        profile=User_Profile.objects.get(user=user)
        return render(request,'app/chatbox.html',{'group_name':group_name,'chats':chats,'group':group,'profile':profile,'allgroup':allgroup,'mygroup':mygroup,'joingroup':joingroup})
    else:
        print(request.POST.get("group_name"),'====================================')
        obj=Group()
        obj.name=request.POST.get("group_name")
        obj.image=request.FILES['image']
        obj.background=request.FILES['background']
        obj.created_by=request.POST.get("created_by")
        obj.timestamp=datetime.now()
        obj.save()
        return redirect('/%s/'%group_name)





def view_name(request):
    year=date.today()
    return render(request, 'app/login.html', {'year':year.year})


def logout(request):
    auth_logout(request)
    return redirect('/')



def delete_group(request,pk):
    obj = Group.objects.get(id=pk)
    obj.delete()
    return redirect('index')


def profile(request,pk):
    if request.method=="GET":
        user=User.objects.get(id=pk)
        sender = User_Profile.objects.get(user=user)
        allgroup=Group.objects.all()
        return render(request,"app/profile.html",{'allgroup':allgroup,'sender':sender})
    else:
        user=User.objects.get(id=pk)
        f=User_Profile()
        f.user=user
        f.first_name=request.POST.get("fname")
        f.last_name=request.POST.get("lname")
        f.email=request.POST.get("email")
        f.phone=request.POST.get("phone")
        f.image=request.FILES['image']
        f.save()
    return redirect('index')
   



def add_group(request,pk):
    group_add=User_Group()
    user=User.objects.get(username=request.user.username)
    group_add.user=User_Profile.objects.get(user=user)
    group_add.group = Group.objects.get(id=pk)
    group_add.status="True"

    group_add.save()

    return redirect('/index/')
