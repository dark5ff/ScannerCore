from django.shortcuts import render, redirect
from celery import shared_task
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .tasks import main
from .models import onionCrawlerEngine,detectKeywords,detectedUrl
import json

def index(request):
    if request.GET.get("url",False):
        url=request.GET.get("url")
        main.delay(url)
    return HttpResponse("Thread Call OK")


def checkEngine(request):
    statusObj=onionCrawlerEngine.objects.all()
    responseList=[]

    for engine in statusObj:
        responseList.append({
                    "name": engine.engine_name,
                    "url":engine.engine_url,
                    "status":engine.status_code,
                    "time":engine.checked_at.strftime("%m/%d/%Y, %H:%M:%S")})
    return JsonResponse(responseList,safe=False)

def checkKeyword(request):
    statusObj=detectKeywords.objects.all()
    responseList=[]
    
    for engine in statusObj:
        responseList.append({
                    "keyword": engine.keyword,
                    "author":engine.created_from.username,
                    "time":engine.created_at.strftime("%m/%d/%Y, %H:%M:%S")})
    return JsonResponse(responseList,safe=False)

def showDetect(request):
    statusObj=detectedUrl.objects.all()
    responseList=[]
    
    for engine in statusObj:
        responseList.append({
                    "title": engine.title,
                    "url":engine.onion_http,
                    "mirrorUrl":engine.mirror_http,
                    "contentLength":engine.content_length,
                    "keyword":engine.keyword.keyword,
                    "status": engine.status_code,
                    "pk":engine.onion_http_hash,
                    "referer":engine.crawlerName,
                    "time":engine.created_at.strftime("%m/%d/%Y, %H:%M:%S")})
    return JsonResponse(responseList,safe=False)


