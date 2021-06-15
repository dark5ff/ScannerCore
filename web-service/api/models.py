from django.db import models
from django.contrib.auth.models import User

class onionCrawlerEngine(models.Model):
    engine_name=models.CharField(max_length=50)
    engine_url=models.CharField(max_length=512)
    status_code= models.SmallIntegerField()
    checked_at= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.engine_name

class detectKeywords(models.Model):
    keyword=models.CharField(max_length=50,primary_key=True)
    created_at= models.DateTimeField(auto_now_add=True)
    created_from= models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.keyword

class detectedUrl(models.Model):
    onion_http_hash=models.CharField(max_length=512,primary_key=True)
    onion_http=models.URLField(max_length=1024)
    mirror_http=models.URLField(max_length=2048)
    content_length=models.SmallIntegerField()
    keyword=models.ForeignKey(detectKeywords, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    lastChecked_at=models.DateTimeField(auto_now_add=True)
    status_code=  models.SmallIntegerField()
    title = models.CharField(max_length=512)
    crawlerName= models.CharField(max_length=50)
    def __str__(self):
        return self.onion_http

class fileUuidMap(models.Model):
    source_hash=models.CharField(max_length=512)
    content_length=models.SmallIntegerField()
    system_path=models.CharField(max_length=2048)

    def __str__(self):
        return self.source_hash

