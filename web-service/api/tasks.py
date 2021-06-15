from celery import shared_task
import requests
import socks
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from uuid import uuid4
import os
from os import path as osPath
from re import compile as reCompile

proxies = {'http':  f'socks5h://{os.environ.get("PROXY_HOST")}:{os.environ.get("PROXY_PORT")}',
           'https': f'socks5h://{os.environ.get("PROXY_HOST")}:{os.environ.get("PROXY_PORT")}'}


def downloadStatic(urlfilePath):
    url,filePath=urlfilePath
    cssObj=None
    with requests.get(url,proxies=proxies,headers={'Connection':'close'},stream=True) as r:
      try:
        print(r)
        r.raise_for_status()
        if(filePath.find(".css")>=0):
            cssObj={'text':r.text,'url':url}
        with open(f"./static/{filePath}", 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
        return cssObj
      except Exception as e:
        print(e)
        return

def cssExtractLink(cssObj,urlPattern):
    cssText,cssUrl=cssObj.values()
    links=urlPattern.findall(cssText)
    relinks=[]
    for link in links:
        if(link.find("../") >=0):
            newCssObj={}
            newCssObj['httpUrl']=urljoin(cssUrl,link)
            newCssObj['localUrl']=link
            relinks.append(newCssObj)

    return relinks

def torToLocalfile(directories,downloadMapping):
    threadProcesses=[]
    linkInCss={}
    urlPattern = reCompile(r'url\(\'?([(..)/].*?)\'?\)')

    for makePath in directories:
        os.makedirs(f"./static/{makePath}",exist_ok=True)
    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in downloadMapping.keys():
            threadProcesses.append(executor.submit(downloadStatic, [url,downloadMapping.get(url)]))
    for task in as_completed(threadProcesses):
        if task.result():
           cssObj=task.result()
           createNewCssObj=cssExtractLink(cssObj,urlPattern)
           linkInCss[cssObj.get('url')]= {'text':cssObj.get('text'),'cssObjs':createNewCssObj}

    return linkInCss 

def validCheckLink(transDict,url,cssLocalSrc=False):
    ''' extensionType bs4 mod, transDict keys: tag,htmlText,uuidMapping,downloadMapping
                                         type: bs4, string, dict, dict 
                                         return : None if css
    '''
    tag=transDict.get('tag')
    htmlText=transDict.get('htmlText')
    tagString=str(tag)
    uuidMapping=transDict.get('uuidMapping')
    downloadMapping=transDict.get('downloadMapping')
    directories=transDict.get('directories')
        

    newLink=""
    if (tagString.find('//') >=0 and tagString.find('.onion') < 0) or tagString.find('data:') >=0:
        return
    if (tagString.find('http')>=0):
        print(tagString)
        return
    if tag.attrs.get("src"):
            fullPath=tag.attrs.get("src")
    elif tag.attrs.get('href'):
            fullPath=tag.attrs.get("href")

    newLink=fullPath
    for path in fullPath.split('/'):
        if not uuidMapping.get(path,False):
            uuidMapping[path]=str(uuid4().hex)
        pathPosition=newLink.find(path)
        newName=uuidMapping.get(path)
        newLink=newLink[0:pathPosition] + newName + newLink[pathPosition+len(path):]
    _,extension=osPath.splitext(fullPath)

    if extension.find('.css')>=0:
        newLink+='.css'
        newName+='.css'

    downloadMapping[urljoin(url,fullPath)]=newLink
    directories.append(newLink.replace(newName,''))
    if cssLocalSrc != False:
       htmlText=htmlText.replace(fullPath,f"/{newLink}")

    else:
       htmlText=htmlText.replace(fullPath,f"./{newLink}")

    return htmlText
def linkExtract(url,htmlText):
    soup=BeautifulSoup(htmlText,'html.parser')
    uuidMapping,downloadMapping={},{}
    threadProcesses,directories=[],[]

    for bs4Obj in soup.find_all(['script','link','img']):
        transDict={"tag":bs4Obj,
                   "htmlText":htmlText,
                   "uuidMapping":uuidMapping,
                   "downloadMapping":downloadMapping,
                   "directories":directories,
        }
        htmlText=validCheckLink(transDict,url)
    with open(f"./static/test.html", 'w') as f:
        f.write(htmlText)


    cssLinks=torToLocalfile(directories, downloadMapping)
    rootDownloadMapping=downloadMapping.copy()
    downloadMapping={}
    directories=[]
    soup=BeautifulSoup()
    cssPatchMapping={}
    for cssObjs in cssLinks.keys():
         cssRootUrl=cssObjs
         text,newCssObjs = cssLinks.get(cssObjs).values()
         patchText=text
         for cssObj in newCssObjs:
             src=urlparse(cssObj.get('httpUrl')).path
             cssLocalSrc=cssObj.get('localUrl')
             transDict={"tag":soup.new_tag("img",src=src),
                       "htmlText": patchText,
                       "uuidMapping":uuidMapping,
                       "downloadMapping":downloadMapping,
                       "directories":directories,
             }
             patchText=validCheckLink(transDict,url,cssLocalSrc)
         cssPatchMapping[cssRootUrl]= transDict.get('htmlText')
    torToLocalfile(directories, downloadMapping)
    for j in cssPatchMapping.keys():
        localFilepath=rootDownloadMapping.get(j)
        with open(f"./static/{localFilepath}", 'w') as f:
            f.write(cssPatchMapping.get(j))

@shared_task
def main(url):
    #url='http://jrw32khnmfehvdsvwdf34mywoqj5emvxh4mzbkls6jk2cb3thcgz6nid.onion/blogs.html'
    print(url)
    origin=requests.get(url,proxies=proxies,headers={'Connection':'close'})
    print(origin)
    linkExtract(url,origin.text)

