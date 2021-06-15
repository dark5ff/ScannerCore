from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import hashlib
from api.models import onionCrawlerEngine, detectKeywords, detectedUrl
def index(request):
    detectedObj= detectedUrl.objects.all()
    print(detectedObj[0].created_at)
    return render(request, 'dashboard/dashboard.html', {"detecteds":detectedObj})

def search(request):
    key=request.GET.get("key")
    if key:
        detectedObj=detectedUrl.objects.filter(title__icontains=key)
        if (not detectedObj):
            detectedObj=detectedUrl.objects.filter(onion_http__icontains=key)

    else:
        detectedObj={}
        key='Search Title, URL, ...'
    return render(request, 'dashboard/search.html',{"detecteds":detectedObj, "key":key})

def detail(request):
    key=request.GET.get("key")
    detectedObj= detectedUrl.objects.all().get(onion_http_hash=key)
    return render(request, 'dashboard/detail.html',{'detectOne':detectedObj})

def init(request):
    crawlerObj= onionCrawlerEngine.objects.all()
    keywordObj= detectKeywords.objects.all()
    return render(request, 'dashboard/init.html',{"crawlers":crawlerObj,"keywords":keywordObj})
def room(request, room_name):
    return render(request, 'dashboard/index.html', {})

def apiCreateServer(request):
    return render(request, 'dashboard/index.html', {})


def error400(request, exception):
    data = {"message": "Bad Request "}
    return render(request,'dashboard/error.html', data)

def error403(request, exception):
    data = {"message": "Permission Denied"}
    return render(request,'dashboard/error.html', data)

def error404(request, exception):
    data = {"message": "Page Not Found"}
    return render(request,'dashboard/error.html', data)

def error500(request, exception):
    data = {"name": "Server Error"}
    return render(request,'dashboard/error.html', data)

