from django.shortcuts import render, redirect
from celery import shared_task
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .tasks import main
from .models import onionCrawlerEngine,detectKeywords,detectedUrl
import json
import datetime

def mainGraph(request):
    statusObj=detectedUrl.objects.order_by('created_at')


    lastTime=statusObj.last().created_at

    timeTable=[]
    for divTime in range(10,0,-1):
        graphTime= lastTime-datetime.timedelta(hours=divTime)
        print(graphTime)
        timeTable.append({
                'x':graphTime.strftime("%m/%d/%Y, %H:%M:%S"),
                'data': len(statusObj.filter(created_at__lte =graphTime)),
                })

    return JsonResponse(timeTable,safe=False)


def stickGraph(request):
    crawlers=[]
    crawlerTable=[]

    statusObj=detectedUrl.objects.all()

    for crawlerName in onionCrawlerEngine.objects.all():
        crawlers.append(crawlerName.engine_name.lower())
    

    for crawlerName in crawlers:
        crawlerTable.append({
                'x': crawlerName,
                'data':len(statusObj.filter(crawlerName=crawlerName)),
        })

    return JsonResponse(crawlerTable,safe=False)

