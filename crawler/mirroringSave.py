from termcolor import colored
import requests
import socks
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from uuid import uuid4
from os import makedirs
from os import path as osPath
from os import getcwd
from os import system
from re import compile as reCompile
import time
from os import environ


def downloadStatic(urlfilePath):
    url,filePath,proxiesNumber=urlfilePath
    #print(url)
    cssObj=None
    print(f"Download URL : {url[-30:]} ==> Proxy Container INFO : {proxiesNumber.get('http')}",end='\r')
    time.sleep(0.02) 
    with requests.get(url,proxies=proxiesNumber,headers={'Connection':'close'},stream=True) as r:
      try:
        r.raise_for_status()
        print(len(f"Download URL : {url[-30:]} ==> Proxy Container INFO : {proxiesNumber.get('http')}")*" ",end='\r')
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
        makedirs(f"./static/{makePath}",exist_ok=True)
    print("[*] Onion HTTP Request Thread Start [*]")

    cnt=0
    global PacketCount
    with ThreadPoolExecutor(max_workers=50) as executor:
        for url in downloadMapping.keys():
            PacketCount+=1
            cnt=cnt%3
            threadProcesses.append(executor.submit(downloadStatic, [url,downloadMapping.get(url),proxies[cnt]]))
            #print(f"Download URL : {url[-30:]} ==> Proxy Container INFO : {proxies[cnt]}",end='\r')
            #time.sleep(0.03)
            #print(len(f"Download URL : {url[-30:]} ==> Proxy Container INFO : {proxies[cnt]}")*" ",end='\r')
            cnt+=1
    print(colored('\t\tDownload all file: SUCCESS', 'yellow'))

    for task in as_completed(threadProcesses):
        if task.result():
           cssObj=task.result()
           createNewCssObj=cssExtractLink(cssObj,urlPattern)
           linkInCss[cssObj.get('url')]= {'text':cssObj.get('text'),'cssObjs':createNewCssObj}

    return linkInCss 

def validCheckLink(transDict,rootUrlObj,cssLocalSrc=False):
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
    if tag.attrs.get("src"):
        fullPath=tag.attrs.get("src")
    elif tag.attrs.get('href'):
        fullPath=tag.attrs.get("href")
    elif tag.attrs.get('action'):
        fullPath=tag.attrs.get("action")
    elif tag.attrs.get('background'):
        fullPath=tag.attrs.get("backgorund")
    else:
        return htmlText
    if(fullPath.find(".php")>=0):
        return htmlText

    print(f"FIND {tag.name} TAG => Full Path: {fullPath[len(fullPath)//2:]}...",end='\r')
    time.sleep(0.03)
    print(len(f"FIND {tag.name} TAG => Full Path: {fullPath[len(fullPath)//2:]}...")*" ",end='\r')

    if bool(urlparse(fullPath).netloc) and fullPath.find(".onion")<=0:
        return htmlText

    originBackupPath=fullPath
    nowUrlObj= urlparse(fullPath)
    otherOnion=False

    if(nowUrlObj.netloc == rootUrlObj.netloc and nowUrlObj.path =='/'):
        return htmlText
    if nowUrlObj.netloc == rootUrlObj.netloc or bool(nowUrlObj.netloc)== False:
        fullUrl=  urljoin(f"http://{rootUrlObj.netloc}",nowUrlObj.geturl())
        onlyPath= fullUrl[fullUrl.find(nowUrlObj.path):]
    else:
        # another onion url
        otherOnion=True
        rootUrlObj= urlparse(fullPath)
        onlyPath=rootUrlObj.geturl()
        fullUrl=onlyPath
 
    if otherOnion == True:
         if not uuidMapping.get(fullUrl,False):
            uuidMapping[fullUrl]=str(uuid4().hex)
         newName=uuidMapping.get(fullUrl)
    else: 
        lastPath= onlyPath[onlyPath.rfind('/'):]
        if len(lastPath)==1 or lastPath.find("?")>=0 :
            onlyPath=onlyPath[:onlyPath.rfind("/")] + onlyPath[onlyPath.rfind("/")+1:]
            
        for path in onlyPath.split('/'):
            if path == '': continue
            if not uuidMapping.get(path,False):
                uuidMapping[path]=str(uuid4().hex)
            pathPosition=onlyPath.find(path)
            newName=uuidMapping.get(path)
            onlyPath=onlyPath[0:pathPosition] + newName + onlyPath[pathPosition+len(path):]
    _,extension=osPath.splitext(originBackupPath)
    if extension.find('.css')>=0:
        onlyPath+='.css'
        newName+='.css'

    
    downloadMapping[fullUrl]=onlyPath
    directories.append(onlyPath.replace(newName,''))
    if cssLocalSrc != False:
       htmlText=htmlText.replace(fullPath,f"./{onlyPath}")
    else:
       htmlText=htmlText.replace(fullPath,f"./{onlyPath}")

    return htmlText

def linkExtract(url,htmlText):
    soup=BeautifulSoup(htmlText,'html.parser')
    uuidMapping,downloadMapping={},{}
    threadProcesses,directories=[],[]

    httpObjLists=[]
    httpObjLists+= soup.find_all(href=True)
    httpObjLists+= soup.find_all(src=True)
    httpObjLists+= soup.find_all(background=True)
    httpObjLists+= soup.find_all(action=True)

    print("[*] Detect Tag for Rendering Start [*]")

    rootUrlObj=urlparse(url)
    for bs4Obj in httpObjLists:
        transDict={"tag":bs4Obj,
                   "htmlText":htmlText,
                   "uuidMapping":uuidMapping,
                   "downloadMapping":downloadMapping,
                   "directories":directories,
        }
        htmlText=validCheckLink(transDict,rootUrlObj)

    print(colored('\t\tDetect of all tag: SUCCESS', 'yellow'))

    #htmlText=htmlText.replace("http://ly75dbzixy7hlp663j32xo4dtoiikm6bxb53jvivqkpo6jwppptx3sad.onion","./") 
    htmlText=htmlText.replace("http://ahmarsqpatnhdtvq2e3s6tca2z4ivxaax4liunijf7tabnvkka3rzlqd.onion","./")
    with open(f"./static/{saveFile}.html", 'w') as f:
        f.write(htmlText)

    print("[*] UUID Mapping Start [*]")
    for j in transDict.get('uuidMapping').keys():
        print(f"Origin Name : {j[len(j)//2:]} ===> UUID : {transDict.get('uuidMapping').get(j)}",end='\r')
        time.sleep(0.03)
        print(len(f"Origin Name : {j[len(j)//2:]} ===> UUID : {transDict.get('uuidMapping').get(j)}")*" ",end="\r")

    print(colored('\t\tUUID Mapping: SUCCESS', 'yellow'))


    torToLocalfile(directories, downloadMapping)
    
    return 
    cssLinks=torToLocalfile(directories, downloadMapping)
    rootDownloadMapping=downloadMapping.copy()
    downloadMapping={}
    directories=[]
    soup=BeautifulSoup('','html.parser')
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
             patchText=validCheckLink(transDict,cssLocalSrc)
         cssPatchMapping[cssRootUrl]= transDict.get('htmlText')

    for j in cssPatchMapping.keys():
        localFilepath=rootDownloadMapping.get(j)
        with open(f"./static/{localFilepath}", 'w') as f:
            f.write(cssPatchMapping.get(j))

    torToLocalfile(directories, downloadMapping)

    for j in cssPatchMapping.keys():
        localFilepath=rootDownloadMapping.get(j)
        with open(f"./static/{localFilepath}", 'w') as f:
            f.write(cssPatchMapping.get(j))


session = requests.session()

#host=os.environ.get("DJANGO_DB_HOST"),
session.proxies = {'http':  f'socks5h://{environ.get("proxy_host")}',
                   'https': f'socks5h://{environ.get("proxy_host")}'}
proxies1 = {'http':  f'socks5h://{environ.get("proxy_host")}',
                   'https': f'socks5h://{environ.get("proxy_host")}'}
proxies2 = {'http':  f'socks5h://{environ.get("proxy_host")}',
                   'https': f'socks5h://{environ.get("proxy_host")}'}
proxies3 = {'http':  f'socks5h://{environ.get("proxy_host")}',
                   'https': f'socks5h://{environ.get("proxy_host")}'}
proxies=[proxies1, proxies2, proxies3]

def SaveMain(url):
    print(url)
    print(proxies1)
    saveFile=uuid4().hex

    try:
        origin=session.get(url,headers={'Connection':'close'})
    except Exception as e:
        print(e)
        return 
    linkExtract(url,origin.text)


'''
for i in range(0,10):
    url='http://ly75dbzixy7hlp663j32xo4dtoiikm6bxb53jvivqkpo6jwppptx3sad.onion/'
    start=time.time()
    origin=session.get(url,headers={'Connection':'close'})
    linkExtract(url,origin.text)
    end=time.time()
    print(end-start)
------
PacketCount=0
saveFile=uuid4().hex
print(colored('[*] Mirroring Save Start[*]', 'green'))
#url='http://ly75dbzixy7hlp663j32xo4dtoiikm6bxb53jvivqkpo6jwppptx3sad.onion/'
url='http://ahmarsqpatnhdtvq2e3s6tca2z4ivxaax4liunijf7tabnvkka3rzlqd.onion/'
print(f"Target URL : {url}")
origin=session.get(url,headers={'Connection':'close'})
soup=BeautifulSoup(origin.text,'html.parser')
print(f"Target URL Response Status : {origin}")
print("="*15)
print(f"TITLE : {soup.title.get_text()}")
print(f"\t\tSERVER : {origin.headers.get('Server')}")
print(f"\t\tX-Powered-By : {origin.headers.get('X-Powered-By')}")
print(f"\t\tCONTENT-LENGTH : {len(origin.text)}")
print("="*15)
print(f"Target URL Response Status : {origin}")
linkExtract(url,origin.text)

print("="*15)
print(colored('[*] Mirroring Save Done[*]', 'green'))
print(f'\t\tTarget URL :{url}')

print('\t\tGeneral Browser Rending Path :',end='')
print(colored(f'{getcwd()}/static/{saveFile}.html', 'yellow'))
print('\t\tCount of Requests :',end='')
print(colored(f'{PacketCount}', 'yellow'))
print('\t\tLoad File Directory :',end='')
print(colored(f'{getcwd()}/static/{saveFile}/', 'yellow'))

system(f'cp -R /Users/intadd/Desktop/0000 {getcwd()}/static/FILES')

system(f'chmod -R 777 {getcwd()}/static')
---

'''
