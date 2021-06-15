from DarkWebCrawler import Crawler
import UrlRequestExecutor
import time
import pymysql
from mirroringSave import SaveMain
from os import environ

from time import sleep
def db_info():

    print(environ.get("DJANGO_DB_HOST"))
    dbObj = pymysql.connect(
        user='intadd', 
        passwd='intadd', 
        host=environ.get("DJANGO_DB_HOST"),
        db=environ.get("DJANGO_DB_NAME"),
        charset='utf8'
    )

    return dbObj

def keywords():
    while (True):
        try:
            dbObj=db_info()
            break
        except Exception as e:
            sleep(5)
            print(e)

    cursor=dbObj.cursor()
    sql=''' SELECT keyword FROM api_detectkeywords; '''
    cursor.execute(sql)
    keywordsList= [ item[0] for item in cursor.fetchall()]
    return keywordsList


if __name__ == "__main__":
    keyword_list = keywords()
    all_result=[]
    for keyword in keyword_list:
        print(f'Search keyword is {keyword}')
        crawler = Crawler(keyword)
        for engine in crawler.urls.keys():
            print(f'Call {engine}')
            callMethod = getattr(Crawler, engine)
            result = callMethod(crawler)
            all_result+=result
            #UrlRequestExecutor.ThreadWorker(result)
    for url in all_result:
        SaveMain(url)

