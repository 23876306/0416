import sys
import csv
import time
import requests
from bs4 import BeautifulSoup
URL = "https://search.books.com.tw/search/query/key{0}/cat/all"     

def generate_search_url(url,keyword):                              #產生每一個關鍵字的url
    url = url.format(keyword)
    return url


def get_resource(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Window NT 10.0; Win64; x64) ApplWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    return requests.get(url, headers = headers)


def parse_html(r):    
    if r.status_code == requests.codes.ok:
        r,encoding = "utf-8"
        soup = BeautifulSoup(r,"lxml")    
    else:
        print("HTTP request Error")                                   
    return soup


def get_word(soup):
    words = []
    for wordlist_table in soup.find_all("td"):
        new_word = []                                           
        text1 = wordlist_table.text.replace("\n","")                #run之後的內容中"\n"替換成""
        if len(text1) > 0:                                          #""還是會出現且長度=0 所以只列印出長度>0的地方
            new_word.append(text1)                                  #把替換後的內容存到new_word內
            words.append(new_word)                                
    return words

def web_scraping_bot(url):
    book_list = []
    print("retrive data from InterNet....")
    soup = parse_html(get_resource(url)) 
    if soup != None:
        tag_item = soup.find_all(class_="box_1")
    for item in tag_item:
        book = []
        book.append(item.find("img")["alt"])                          #找圖片跟書名
        [isbn, price] = get_ISBN_Price(item.find("a")["href"])        #ISBN是出現在第一頁典籍下去後才會出現的
        print(book)
        print("wait 2 sec")
        time.sleep(2)


def get_ISBN_Price(url):                                                            #找ISBN碼 並且跟連結拆開 
    url_1 = "https:" + url
    soup = parse_html(get_resource(url_1))
    isbnStr = ""
    if soup != None:
        bd = soup.find(class_="bd")
        lilist = bd.find_all("li")
        print("lilist")
        price = 0 
        priceUl = soup.find("ul",{"class" : "price"})
        for liData in lilist:
            print("liData")
            if "ISBN" in liData.text:
                isbnStr = liData.text[5:]                                           #找書名,5: 抓前面數過來第5個後面
        price = priceUl.find_all("li").text[3:-1]                                   #找價錢,3:-1  抓前面數過來第3個後面到最後一個
        return [isbnStr, price]
    else:
        return[None, None]
    print(url_1)
    print(url_1 +"1000")    

if __name__ == "main":
    if len(sys.argv) > 1:
        urlx = generate_search_url(URL, sys.argv[1])
        book_list = web_scraping_bot(urlx)
    for item in book_list:
        print(item)