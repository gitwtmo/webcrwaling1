import module.api as api
from module.speech_service import SpeechService as sps
from module.data_search import Searching as search
from const import LOGIN, LOGOUT, MENUS, location_shortner, location_number, damList
from datetime import datetime
import playsound
import pandas as pd
import requests

class Timo:
    def __init__(self) -> None:
        self.state = 'off'
        self.loop = 0
        self.results = []
        self.querys = []
        self.now = datetime.now() # 시간 작동시 고정

    def __call__(self):
        while True:
            print(self.state)
            self.waitInput(bip= False)
            if self.state == "logout":
                break
            
    def waitInput(self, bip=False):
        try:
            results_stt = sps.stt(bip= bip)
            if results_stt == None:
                self.results = []
                # 세부 사항에서 지침 변경 필요
                if (self.state == "login") & (self.loop == 3):
                    self.state = "off"
                    sps.tts("응답이 없어 휴면모드가 작동됩니다.")
            else:
                self.results = results_stt.split(" ")
                self.stt_classifier()
                # 다음단계
        except:
            print("tts 오류")

    def stt_classifier(self):
        if self.state == "off":
            for data in self.results:
                for i in LOGIN():
                    if i == data:
                        self.state = "login"
                        self.login()
                for i in LOGOUT():
                    if i == data:
                        self.state = "logout"
                        self.logout()
        elif self.state == "login":
            for result_index, result in enumerate(self.results):
                for index, menu in enumerate(MENUS()):
                    if menu == result:
                        if menu == MENUS()[0]: # 검색
                            # 네이버 검색 XX
                            if result_index == 1:
                                if self.results[0] == "네이버":
                                    self.querys = self.results[2:]
                                    self.state = "네이버 검색"
                                    self.naver_search()
                            else:
                                # xx 네이버 검색
                                if self.results[result_index-1] == "네이버":
                                    self.querys = self.results[:result_index-1]
                                    self.state = "네이버 검색"
                                    self.naver_search()
                                else:
                                    # 미구현 검색 엔진
                                    pass
                        elif menu == MENUS()[1]: # 날씨
                            # 날씨 XX
                            if result_index == 0:
                                self.querys = self.results[1:]
                                self.state = "날씨"
                                self.weather_search()
                            else:
                                # xx 날씨
                                self.querys = self.results[:result_index]
                                self.state = "날씨"
                                self.weather_search()
                        elif menu == MENUS()[2]: # 미세먼지
                            # 미세먼지 XX
                            if result_index == 0:
                                self.querys = self.results[1:]
                                self.state = "미세먼지"
                                self.pm_search()
                            else:
                                # xx 미세먼지
                                self.querys = self.results[:result_index]
                                self.state = "미세먼지"
                                self.pm_search()
                        elif menu == MENUS()[3]: # 게임
                            # 끝말잇기 게임 XX
                            if result_index == 1:
                                if self.results[0] == "끝말잇기":
                                    self.state = "끝말잇기"
                                    self.follow_up_game()
                            else:
                                # xx 끝말잇기 게임
                                if self.results[result_index-1] == "끝말잇기":
                                    self.state = "끝말잇기"
                                    self.follow_up_game()
                                else:
                                    # 미구현 게임
                                    pass
                        elif menu == MENUS()[4]: # 수위 조사
                            if self.results[result_index-1] == "수위":
                                self.state = "수위 조사"
                                self.dam_check()
                            else:
                                # 그외
                                pass
                        else:
                            pass
                    else:
                        pass
            print(self.state, "self.state")
            if self.state == "login":
                self.__sst_classifier_error()

    def __sst_classifier_error(self):
        self.loop = 0
        sps.tts("잘못 이해했어요.")

    def __sst_data_error(self):
        self.loop = 0
        self.state = "off"
        sps.tts("검색에 문제가 있어요.")

    def login(self):
        sps.tts("네 무엇을 도와드릴까요?")
        while self.state == "login":
            if self.loop == 0:
                self.waitInput(bip=True)
            else:
                self.waitInput(bip=False)
            self.loop += 1
            pass

    def logout(self):
        pass

    def naver_search(self):
        try:
            for query in self.querys:
                crawling = search(url=f"https://dict.naver.com/search.dict?dicQuery={query}")
                crawling.bs_search(query)
            self.state = "off"
        except:
            self.__sst_data_error()

    def weather_search(self):
        try:
            sgis_api = api.SgisApi()
            data = sgis_api.geoCoding(self.querys)
            x = data['x']
            y = data['y']
            data = sgis_api.transformation(x= x, y= y, src= 5179, dst= 4326)
            x = data["posX"]
            y = data["posY"]
            meteo_api = api.MeteoApi()
            result = meteo_api(url=f"https://api.open-meteo.com/v1/forecast?latitude={y}&longitude={x}&hourly=temperature_2m,rain,windspeed_10m,winddirection_10m&timezone=Asia%2FTokyo&forecast_days=1")
            temp = result['hourly']['temperature_2m'][self.now.hour]
            rain = result['hourly']['rain'][self.now.hour]
            wins = result['hourly']['windspeed_10m'][self.now.hour]
            wind = result['hourly']['winddirection_10m'][self.now.hour]
            sps.tts(f"현재 {self.querys}의 온도는 {temp} 강우량은 {rain} 풍량은 {wins} 풍향은 북향기준 {wind}도 입니다.")
            self.state = "off"
        except:
            self.__sst_data_error()

    def pm_search(self):
        try:
            location_num = ""
            sgis_api = api.SgisApi()
            data = sgis_api.geoCoding(self.querys)
            location_name_list = data['nm'].split(" ")
            print(location_name_list, "location_name_list")
            for index, i in enumerate(location_name_list):
                result = location_shortner(i)
                print(result,"result")
                if result != 0:
                    location_name_list[index] = result
                    print(location_name_list, "location_name_list")
                    location_num = location_number(result)
                    print(location_num, "location_num")

            date = self.now.strftime("%Y-%m-%d")
            url = f"https://www.airkorea.or.kr/web/pmRelaySub?strDateDiv=1&searchDate={date}&district={location_num}&itemCode=10007&searchDate_f={self.now.year}{self.now.month}"
            
            response = requests.get(url)
            data = pd.read_html(response.text)
            dd = pd.DataFrame(data=data[0])
            dd = pd.concat([data[0]["측정소명"], data[0][f"{self.now.hour}시"]], axis=1)
            if len(location_name_list) == 1:
                for i in dd.index:
                    inner_name = dd.loc[i][0].replace('[','').replace(']',' ')
                    inner_value = dd.loc[i][1]
                    sps.tts(inner_name)
                    sps.tts(inner_value)
                self.state = "off"
            else:
                name = " ".join(location_name_list)
                for i in dd.index:
                    inner_name = dd.loc[i][0].replace('[','').replace(']',' ')
                    inner_value = dd.loc[i][1]
                    if inner_name[:len(name)] == name:
                        sps.tts(inner_name)
                        sps.tts(inner_value)
                self.state = "off"
                pass
        except:
            self.__sst_data_error()

    def follow_up_game(self):
        try:
            start_with = None
            result = None
            dicList = []
            sps.tts("시작해주세요.")
            while True:
                playsound.playsound('bip.mp3',True)
                results = sps.stt()
                kor_dict_api = api.KorDictApi()
                if (start_with == None) & (results != None):
                    result = kor_dict_api(keyword=results, start=1, num=10, state="input", dicList=dicList)
                elif results == None:
                    sps.tts('시간초과 패배')
                    break
                else:
                    if start_with == results[0]:
                        result = kor_dict_api(keyword=results, start=1, num=10, state="input", dicList=dicList)
                    else:
                        sps.tts(f'{start_with}로 시작하는 단어가 아닙니다. 패배')
                        break # 시작단어 틀림
                if result == True:
                # if result["state"] == True:
                    result = kor_dict_api(keyword=results[-1], start=1, num=10, state="output", dicList=dicList)
                    
                    if result:
                        start_with = result[-1]
                        sps.tts(result)
                    else:
                        sps.tts(f'단어를 찾지 못했어요. 승리')
                        break # 컴퓨터 단어 실수
                else:
                    sps.tts(f'존재하지 않는 단어입니다. 패배')
                    break # 나의 단어 실수
            self.state = "off" 
        except:
            self.__sst_data_error()

    def dam_check(self):
        try:
            damDataList = []
            dam_api = api.DamApi()
            sps.tts("검색중입니다. 잠시만 기다려주세요.")
            for i in damList():
                damDataList.append(dam_api(i))
            for i in damDataList:
                print(i)
                name = damList()[i["DAM_CD"]]
                rsvwt = i["DAM_RSVWT_RT"]
                dqty = i["TOT_DQTY"]
                sps.tts(F"{name}의 저수율은 {rsvwt}% 이고 방류량은 {dqty}m^3/s 입니다")
            self.state = "off"
        except:
            self.__sst_data_error()
        pass

if __name__ == "__main__":
    main = Timo()
    main()