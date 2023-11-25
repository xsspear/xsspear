from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import List, Item
from .forms import CreateNewList, RegisterForm
from django.contrib.auth import authenticate, login
import subprocess
import psutil


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],)
            login(request, new_user)
            l = List(name=form.cleaned_data['username'])
            l.save()
            request.user.targetslist.add(l)
        return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form":form})


def targets(response):
    ls = List.objects.get(name=response.user)
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("type") == "subdomain": # subdomain scan
            txt = response.POST.get("new")
            s = str(response.user)
            process = subprocess.Popen(["/workspaces/XSSpear2-0.com/spearsubdomain.sh", txt, s])
            if len(txt) > 7:
                ls.item_set.create(text=txt, pid=process.pid)
            else:
                print("invalid")
            process.communicate()
        elif response.POST.get("type") == "url": # url scan
            txt = response.POST.get("new")
            s = str(response.user)
            process = subprocess.Popen(["/workspaces/XSSpear2-0.com/spearurl.sh", txt, s])
            if len(txt) > 7:
                ls.item_set.create(text=txt, pid=process.pid)
            else:
                print("invalid")
            process.communicate()
            #tid = ls.item_set.get(pid=process.pid)
            #return HttpResponseRedirect("/targets/%s" %tid.id)
    return render(response, "main/targets.html", {})

def target_info(response, id):
    try:
        i = List.objects.get(name=response.user)
        target = i.item_set.get(id=id)
        target_proc = psutil.pid_exists(target.pid)
    except:
        return HttpResponseRedirect("/targets/")
    return render(response, "main/info.html", {"target":target,"target_proc":target_proc})

def home(response):
    return render(response, "main/home.html", {})

def results(response):
    try:
        un = str(response.user) + ".txt"
        fn = open("/workspaces/XSSpear2-0.com/" + un, 'r').read().splitlines()
    except:
        return HttpResponseRedirect("/xsscan/")
    return render(response, "main/results.html", {"fn":fn})
    
    
def xsscan(response):
    return render(response, "main/xsscan.html", {})