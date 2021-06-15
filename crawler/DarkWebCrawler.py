import requests
import time
import json
import LogController

from urllib import parse
from bs4 import BeautifulSoup as Soup
import os

class Crawler:

    def __init__(self, keyword):
        self.keyword = keyword
        os.environ.get("DJANGO_DB_NAME"), 

        self.proxies = {'http': 'socks5h://172.26.0.3:9050',
                        'https': 'socks5h://172.26.0.3:9050'}
        self.headers = {'Connection': 'close',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'}

        self.logger = LogController.logController()

        self.urls = {
            'Ahmia' : 'http://msydqstlz2kzerdg.onion',
            'Phobos' : 'http://phobosxilamwcg75xt22id7aywkzol6q6rfl2flipcqoc4e4ahima5id.onion',
            'Abiko' : 'http://abikogailmonxlzl.onion',
            'Torch' : 'http://cnkj6nippubgycuj.onion',
            'Tor66' : 'http://www.tor66sezptuu2nta.onion',
            'OnionSearchEngine' : 'http://5u56fjmxu63xcmbk.onion',
            'DarkSearch' : 'https://darksearch.io',
            'Quo' : 'http://quosl6t6c64mnn7d.onion',
            'Haystak' : 'http://haystakvxad7wbk5.onion',
            'OnionLand' : 'http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion'
        }

    def ErrorPrint(self, msg):
        print(msg)

    def Ahmia(self):
        url = self.urls.get('Ahmia')
        url_list = []
        search_url = f"{url}/search?q={self.keyword}"

        try:
            self.logger.logInfo(f'Searching... {search_url}')
            res = requests.get(search_url, proxies=self.proxies, headers=self.headers)

        except Exception as e:
            self.ErrorPrint(f'Ahmia Error, Error message : {e}')
            self.logger.logInfo(f"Search Failed... {search_url}")
            return url_list

        else:
            if (res.status_code < 200 or res.status_code >= 300):
                msg = f'Ahmia status code is {res.status_code}'
                self.ErrorPrint(msg)
                self.logger.logInfo(f"Searching Failed... {search_url} {res}")
                return url_list

            soup = Soup(res.text, 'html.parser')

            for search_result in soup.find_all("li", {"class": "result"}):
                pull_url = url + search_result.find('a').get('href')
                url_list.append(pull_url[pull_url.find("redirect_url") + 13:])

            self.logger.logInfo(f"Searching Done {search_url} {res}")
            return list(set(url_list))

    def Phobos(self):
        url = self.urls.get('Phobos')
        url_list = []
        search_url = f"{url}/search?query={self.keyword}"

        try:
            self.logger.logInfo(f'Searching ... {search_url}')
            res = requests.get(search_url, proxies=self.proxies, headers=self.headers)

        except Exception as e:
            self.ErrorPrint(f'Phobos Error, Error message : {e}')
            self.logger.loginfo(f"Searching Failed... {search_url}")
            return url_list

        if (res.status_code < 200 or res.status_code >= 300):
            self.ErrorPrint(f'Phobos status code is {res.status_code}')
            self.logger.loginfo(f"Searching Failed {search_url} {res}")
            return url_list

        soup = Soup(res.text, 'html.parser')
        page_string = (str)(soup.find("div", {"class": "counter"}).get_text())

        if (page_string.find("About") > -1):
            page_count_check = (int)(page_string[6:page_string.find("results") - 1])
        else:
            page_count_check = (int)(page_string[:page_string.find("results") - 1])

        max_page = 14 if ((page_count_check - 1) / 7 + 1 > 14) else (int)((page_count_check - 1) / 7 + 1)

        for page in range(1, max_page + 1):
            page_url = f"{search_url}&p={str(page)}"
            try:
                self.logger.logInfo(f'Searching ... {page_url}')
                res = requests.get(page_url, proxies=self.proxies, headers=self.headers)

            except Exception as e:
                self.ErrorPrint(f'Phobos Error, Error message : {e}')
                time.sleep(2)
                continue

            else:
                if (res.status_code < 200 or res.status_code >= 300):
                    self.ErrorPrint(f'Phobos status code is {res.status_code}')
                    time.sleep(2)
                    continue

                soup = Soup(res.text, 'html.parser')

                for search_result in soup.find_all("a", {"class": "titles"}):
                    search_result_link = search_result.get('href')
                    url_list.append(search_result_link)

        self.logger.logInfo(f"Searching Done {search_url}")
        return list(set(url_list))

    def Abiko(self):
        url = self.urls.get('Abiko')
        url_list = []
        search_url = f"{url}/search?q={self.keyword}"

        try:
            self.logger.logInfo(f'Searching ... {search_url}')
            res = requests.get(search_url, proxies=self.proxies, headers=self.headers)

        except Exception as e:
            self.ErrorPrint(f'Abiko Error, Error message : {e}')
            self.logger.loginfo(f"Searching Done {search_url}")
            return url_list

        if (res.status_code < 200 or res.status_code >= 300):
            self.ErrorPrint(f'Abiko status code is {res.status_code}')
            self.logger.loginfo(f"Searching Done {search_url} {res}")
            return url_list

        soup = Soup(res.text, 'html.parser')
        redirect_url = soup.find('meta', {"http-equiv": "refresh"}).get('content')[7:]

        for page in range(1, 31):
            page_url = f"{redirect_url}&page={str(page)}"
            try:
                self.logger.logInfo(f'Searching ... {page_url}')
                res = requests.get(page_url, proxies=self.proxies, headers=self.headers)
                self.logger.logInfo(f"Searching Done {search_url} {res}")

            except Exception as e:
                self.ErrorPrint(f'Abiko Error, Error message : {e}')
                print(f'request count check {page}')
                time.sleep(2)
                continue

            else:
                if (res.status_code < 200 or res.status_code >= 300):
                    msg = f'Abiko status code is {res.status_code}'
                    self.ErrorPrint(msg)
                    time.sleep(2)
                    continue

                soup = Soup(res.text, 'html.parser')

                searchResults = soup.find_all('div', {"class": "result__title"})

                for search_result in searchResults:
                    search_result_link = search_result.find('a').get('href')
                    pull_url = search_result_link[
                               search_result_link.find("http"):search_result_link.find(f"&q={self.keyword}")]
                    pull_url = parse.unquote(pull_url)
                    url_list.append(pull_url)

                if soup.find('div', {'class': 'page__hint'}):
                    break

        self.logger.loginfo(f"Searching Done {search_url} {res}")
        return list(set(url_list))

    def Torch(self):
        url = 'http://cnkj6nippubgycuj.onion'
        res = requests.get(url, proxies=self.proxies, headers=self.headers)
        url = res.url
        url_list = []
        search_url = f"{url}/search?query={self.keyword}&action=search"

        try:
            self.logger.logInfo(f'Searching ... {search_url}')
            res = requests.get(search_url, proxies=self.proxies, headers=self.headers)


        except Exception as e:
            msg = f'Torch Error, Error message : {e}'
            self.ErrorPrint(msg)
            self.logger.loginfo(f"Searching Done {search_url} {res}")
            return url_list

        soup = Soup(res.text, 'html.parser')

        if res.text.find("returned <b>0</b> results.</p>") >= 0:
            return url_list

        if (res.status_code < 200 or res.status_code >= 300):
            msg = f'Torch status code is {res.status_code}'
            self.ErrorPrint(msg)
            self.logger.loginfo(f"Searching Done {search_url} {res}")
            return url_list

        pageObj = soup.find_all("a", {"class": "page-link"})

        if (pageObj):
            max_page = int(pageObj[-1].get_text())
        else:
            max_page = 1

        for page in range(1, max_page + 1):
            page_url = f"{search_url}&page={str(page)}"

            try:
                self.logger.logInfo(f'Searching ... {page_url}')
                res = requests.get(page_url, proxies=self.proxies, headers=self.headers)
                self.logger.logInfo(f'Searching Done {page_url} {res}')

            except Exception as e:
                msg = f'Torch Error, Error message : {e}'
                self.ErrorPrint(msg)
                time.sleep(2)
                continue

            else:
                if (res.status_code < 200 or res.status_code >= 300):
                    msg = f'Torch status code is {res.status_code}'
                    self.ErrorPrint(msg)
                    time.sleep(2)
                    continue
                soup = Soup(res.text, 'html.parser').find_all('div', {"class": "row"})[-1]

                for smallObj in soup.find_all("small"):
                    url_list.append(smallObj.find('a').get('href'))

        return list(set(url_list))

    def Tor66(self):
        url = self.urls.get('Tor66')
        url_list = []
        search_url = f"{url}/search?q={self.keyword}"
        try:
            self.logger.logInfo(f'Searching ... {search_url}')
            res = requests.get(search_url, proxies=self.proxies, headers=self.headers)
            self.logger.logInfo(f"Searching Done {search_url} {res}")

        except Exception as e:
            msg = f'Tor66 Error, Error message : {e}'
            self.ErrorPrint(msg)
            return url_list

        if (res.status_code < 200 or res.status_code >= 300):
            msg = f'Tor66 status code is {res.status_code}'
            self.ErrorPrint(msg)
            return url_list

        soup = Soup(res.text, 'html.parser')
        page_string = (str)(soup.find('div', {'class': 'sresults'}).get_text)
        page_count_check = (int)(page_string[page_string.find('.Onion sites found') + 21: -13])
        max_page = (int)((page_count_check - 1) / 20 + 1)

        for page in range(1, max_page + 1):
            page_url = f"{search_url}&sorttype=rel&page={str(page)}"
            try:
                self.logger.logInfo(f'Searching ... {page_url}')
                res = requests.get(page_url, proxies=self.proxies, headers=self.headers)
                self.logger.logInfo(f"Searching Done {page_url} {res}")

            except Exception as e:
                msg = f'Tor66 Error, Error message : {e}'
                self.ErrorPrint(msg)
                print(f'request count check {page}')
                time.sleep(2)
                continue

            else:
                if (res.status_code < 200 or res.status_code >= 300):
                    msg = f'Tor66 status code is {res.status_code}'
                    self.ErrorPrint(msg)
                    time.sleep(2)
                    continue

                soup = Soup(res.text, 'html.parser')
                for i in soup.find('div', {'class': 'sresults'}).find_all('a', href=True):
                    if (i.attrs.get('href').find("/serviceinfo/?service=") >= 0):
                        tmpHref = i.attrs.get('href')
                        realHref = parse.unquote(tmpHref[tmpHref.find("dom=") + 4:])
                        url_list.append('http://' + realHref)

        return list(set(url_list))

    def Quo(self):
        url = self.urls.get('Quo')
        url_list = []

        search_url = f'{url}/results?q={self.keyword}'

        try:
            self.logger.logInfo(f'Searching ... {search_url}')
            res = requests.get(search_url, proxies=self.proxies, headers=self.headers)
            self.logger.logInfo(f"Searching Done {search_url} {res}")

        except Exception as e:
            msg = f'Quo Error, Error message : {e}'
            self.ErrorPrint(msg)
            return url_list

        if (res.status_code < 200 or res.status_code >= 300):
            msg = f'Quo status code is {res.status_code}'
            self.ErrorPrint(msg)
            return url_list

        soup = Soup(res.text, 'html.parser')
        result_count_string = str(soup.find("span", {"class", "text-muted"}).get_text())

        if(result_count_string.find(f'No results for "{self.keyword}"')):
            return url_list
        else:
            result_count = (int)(result_count_string[result_count_string.find("Showing") + 8: result_count_string.find("results")].replace(" ", ""))

        max_page = (result_count - 1) // 10 + 1

        for page in range(1, max_page + 1):
            offset = (page - 1) * 10
            page_url = f'{search_url}&offset={offset}'

            try:
                self.logger.logInfo(f'Searching ... {page_url}')
                res = requests.get(page_url, proxies=self.proxies, headers=self.headers)
                self.logger.logInfo(f"Searching Done {page_url} {res}")

            except Exception as e:
                msg = f'Quo Error, Error message : {e}'
                self.ErrorPrint(msg)
                time.sleep(2)
                continue

            else:
                if (res.status_code < 200 or res.status_code >= 300):
                    msg = f'Quo status code is {res.status_code}'
                    self.ErrorPrint(msg)
                    time.sleep(2)
                    continue

                soup = Soup(res.html, 'html.parser')
                results = soup.find_all('div', {'class':'mb-2'})

                if not results:
                    break

                for row in results:
                    if (row.find('h2', {'class': 'result-title'})):
                        link = row.find('h2', {'class': 'result-title'}).find('a').get('href')
                        url_list.append(link)

                next_btn = soup.find('a', rel='next')

                if not (next_btn):
                    break

        return list(set(url_list))

    def Haystak(self):
        url = self.urls.get('Haystak')
        url_list = []
        search_url = f'{url}/?q={self.keyword}'

        try:
            self.logger.logInfo(f'Searching ... {search_url}')
            res = requests.get(search_url, proxies=self.proxies, headers=self.headers)
            self.logger.logInfo(f"Searching Done {search_url} {res}")

        except Exception as e:
            msg = f'Haystak Error, Error message : {e}'
            self.ErrorPrint(msg)
            return url_list

        if (res.status_code < 200 or res.status_code >= 300):
            msg = f'Haystak status code is {res.status_code}'
            self.ErrorPrint(msg)
            return url_list

        # max page = 999 , offset= 9990
        max_page = 999

        for page in range(1, max_page + 1):
            offset = (page - 1) * 10
            page_url = f'{search_url}&offset={offset}'
            try:
                self.logger.logInfo(f'Searching ... {page_url}')
                res = requests.get(page_url, proxies=self.proxies, headers=self.headers)
                self.logger.logInfo(f"Searching Done {page_url} {res}")

            except Exception as e:
                msg = f'Haystak Error, Error message : {e}'
                self.ErrorPrint(msg)
                time.sleep(2)
                continue

            else:
                if (res.status_code < 200 or res.status_code >= 300):
                    msg = f'Haystak status code is {res.status_code}'
                    self.ErrorPrint(msg)
                    time.sleep(2)
                    continue

                soup = Soup(res.text, 'html.parser')
                results = soup.find_all('div', {'class': 'result'})

                if not results:
                    break

                for row in results:
                    link = row.find('i').get_text()
                    url_list.append(link)

        return list(set(url_list))

    '''def Onionland(self):
        url = self.urls.get('OnionLand')
        MAX_PAGE = 10
        offset = 0

        search_url = f'{url}/search?q={self.keyword}'
        res = requests.get(search_url, proxies=self.proxies, headers=self.headers)

        if(res.status_code < 200 or res.status_code >= 300 ):
            return {}

        soup = Soup(res.text, 'html.parser')
        result_count = (str)(soup.find('div', {'class' : 'col-sm-12'}).get_text)
        print(result_count)
        return {}

        url_list = []
        for page in range(1, MAX_PAGE):
            offset += 1
            next_url = f'{search_url}"&page={offset}'
            soup = Soup(requests.get(next_url, proxies=self.proxies, headers=self.headers).text, 'html.parser')
            results = soup.find_all('div',{'class' : 'result-block'})

            # 검색 결과 없으면 종료
            if not results:
                break

            count = 0
            for row in results:
                count += 1
                # 광고이면 저장 안함
                if (row.find('div', {'class' : 'title'}).find('a').get('data-category') == "sponsored-text"):
                    continue

                if (row.find('div', {'class', 'link'})):
                    link = row.select_one('div.link').text.strip()

                url_list.append(link)

            if (count < 23):
                break

        return set(url_list)'''

    def OnionSearchEngine(self):
        url = self.urls.get('OnionSearchEngine')
        url_list = []
        search_url = f'{url}/search.php?search={self.keyword}&submit=Search'

        try:
            self.logger.logInfo(f'Searching ... {search_url}')
            res = requests.get(search_url, proxies=self.proxies, headers=self.headers)
            self.logger.logInfo(f"Searching Done {search_url} {res}")

        except Exception as e:
            msg = f'OnionSearchEngine Error, Error message : {e}'
            self.ErrorPrint(msg)
            return url_list

        if(res.status_code < 200 or res.status_code >= 300):
            msg = f'OnionSearchEngine status code is {res.status_code}'
            self.ErrorPrint(msg)
            return url_list

        max_page = 99

        for page in range(1, max_page + 1):
            page_url = f'{search_url}&page={page}'

            try:
                self.logger.logInfo(f'Searching ... {page_url}')
                res = requests.get(page_url, proxies=self.proxies, headers=self.headers)
                self.logger.logInfo(f"Searching Done {page_url} {res}")

            except Exception as e:
                msg = f'OnionSearchEngine Error, Error message : {e}'
                self.ErrorPrint(msg)
                print(f'request count check {page}')
                time.sleep(2)
                continue

            else:
                if(res.status_code < 200 or res.status_code >= 300):
                    msg = f'OnionSearchEngine status code is {res.status_code}'
                    self.ErrorPrint(msg)
                    time.sleep(2)
                    continue

                soup=Soup(res.text,'html.parser')
                links = soup.find_all('a', target='_blank', style='color:green')

                # 검색 결과 없으면 종료
                if not links:
                    break

                for link in links:
                    result_link = link.text
                    url_list.append(result_link)

        return list(set(url_list))

    def DarkSearch(self):
        url = self.urls.get('DarkSearch')
        url_list = []
        search_url = f"{url}/api/search?query={self.keyword}"

        try:
            self.logger.logInfo(f'Searching ... {search_url}')
            res = requests.get(search_url)
            self.logger.logInfo(f"Searching Done {search_url} {res}")

        except Exception as e:
            msg = f"DarkSearch Error, Error message : {e}"
            self.ErrorPrint(msg)
            return url_list

        if (res.status_code < 200 or res.status_code > 300):
            msg = f'Darksearch status code is {res.status_code}'
            self.ErrorPrint(msg)
            return url_list

        # test -> json(dic)
        json_text = res.text
        json_dic = json.loads(json_text)

        # max_page get
        max_page = (int)(json_dic['last_page'])

        for page in range(1, max_page):
            page_url = f'{search_url}&page={page}'
            try:
                self.logger.logInfo(f'Searching ... {page_url}')
                res = requests.get(page_url, proxies=self.proxies, headers=self.headers)
                self.logger.logInfo(f"Searching Done {page_url} {res}")

            except Exception as e:
                msg = f"DarkSearch Error, Error message : {e}"
                self.ErrorPrint(msg)
                time.sleep(2)
                continue

            else:
                json_text = res.text
                json_dic = json.loads(json_text)

                for data_dics in json_dic['data']:
                    links = data_dics['link']
                    url_list.append(links)

        return url_list

if __name__ == "__main__":

    # keyword list
    keyword_list = ['abcd', 'sex', 'kakao', 'gun', 'drug', 'kakao']
    crawler = Crawler(keyword_list[0])
    result = crawler.Phobos()

    print(result)

    # for keyword in keyword_list:
    #     print(keyword)
    #     crawller = Crawler(keyword)
    #
    #     start_time = time.time()
    #
    #     for engine in crawller.urls.keys():
    #         print("CALL", engine)
    #         callMethod = getattr(Crawler, engine)
    #         result = callMethod(crawller)
    #         print(result)
    #
    #     end_time = time.time()
    #
    #     print(f'Check the operate time {end_time - start_time}')

    print("DONE")
