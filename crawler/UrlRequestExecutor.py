import requests
import urllib.parse
import time
import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_request(url):
    web_content_dic = {}
    proxies = {'http': 'socks5h://localhost:9150',
               'https': 'socks5h://localhost:9150'}

    headers = {'Connection': 'close',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'}


    #request try
    try:
        res = requests.get(url, proxies=proxies, headers=headers, timeout=10)
        if(res.status_code < 200 or res.status_code > 300):
            return {}

    except requests.exceptions.Timeout:
        try:
            res = requests.get(url, proxies=proxies, headers=headers, timeout=10)
        except:
            return {}

    except Exception as e:
        print(e)
        return {}

    ## catch hostname, content length, http status code, html source code
    try:
        host_name = urllib.parse.urlparse(res.url).netloc

        try:
            content_length = res.headers['Content-Length']

        except KeyError:
            content_length = len(res.text)

        web_content_dic[res.url] = {'host name': host_name, 'content length' :
                    content_length, 'status_code' : res.status_code}
                                  #"source code" : res.text


        print(web_content_dic)

        return web_content_dic[res.url]

    except Exception as e:
        print(f'{url} : {e}')
        return {}


def ThreadWorker(url_list):

    request_task = []
    response_results = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in url_list:
            future = executor.submit(get_request, url)
            request_task.append(future)
            print(f"url : {url} request...")

        for future in as_completed(request_task):
            response_data = future.result()
            if(response_data != {}):
                response_results.update(response_data)

    pprint.pprint(f"Dictionary : {response_results} ")

    return response_results