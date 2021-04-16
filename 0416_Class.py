import sys
import csv
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
    return BeautifulSoup(r,"lxml")


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
    r = get_resource(url)
    soup = parse_html(r.text)
    words = get_word(soup)
    book_list = book_list + words
    return book_list 

if __name__ == "main":
    if len(sys.argv) > 1:
        urlx = generate_search_url(URL, sys.argv[1])
        book_list = web_scraping_bot(urlx)
    for item in book_list:
        print(item)








