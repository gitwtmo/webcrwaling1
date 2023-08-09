import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .speech_service import SpeechService as sps

url = "https://www.melon.com/chart/index.htm"

class Searching:
    def __init__(
        self, 
        url, 
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    ) -> None:
        self.url = url
        self.header = header

    def bs_search(self, query):
        response = requests.get(self.url, headers=self.header)
        soup = bs(response.text, 'html.parser')
        html = soup.select_one("#content > div.kr_dic_section.search_result.dic_kr_entry > ul > li:nth-child(1) > p:nth-child(1) > a:nth-child(1) > span > strong")
        if html.text == query:
            html = soup.select_one("#content > div.kr_dic_section.search_result.dic_kr_entry > ul > li:nth-child(1) > p:nth-child(2)")
            sps.tts(f"{query}의 검색 결과는 다음과 같습니다.")
            sps.tts(html.text)
        else:
            sps.tts(f"{query} 검색 결과가 없습니다.")

    def selenium_search(self):
        pass