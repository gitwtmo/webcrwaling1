import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class Request:
    def get(url, data=None, params=None):
        response = requests.get(url, data=data, params=params)
        return json.loads(response.text)

class SgisApi:
    def __init__(self) -> None:
        body = {"consumer_key": "0aef396a09384b2a84c3", "consumer_secret": "288c246e17904e7a8c1f"}
        accessToken=""
        try:
            response = Request.get(url="https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json", data=body)
            accessToken = response["result"]["accessToken"]
        except:
            print(f"API ERROR (SgisApi__init__)")

        self.accessToken = accessToken

    def geoCoding(self, address):
        body = {"address": " ".join(address), "accessToken": self.accessToken}
        cd = ""
        nm = ""
        sgg = False
        try:
            response = Request.get(url="https://sgisapi.kostat.go.kr/OpenAPI3/addr/geocode.json", data=body)
            for i in list(response['result']['resultdata'][0].keys()):
                if i == "sgg_cd":
                    sgg = True
                    break

            if sgg:
                data = response['result']['resultdata'][0]
                if data['sgg_cd']:
                    cd = data['sgg_cd']
                    nm = data['sido_nm'] + " " + data['sgg_nm']
                    x = data['x']
                    y = data['y']
                    print("sgg_cd", data['sgg_cd'])
                    return {"cd":cd, "nm":nm, "x": x, "y": y}
                elif data['sido_cd'] != "null":
                    cd = data['sido_cd']
                    nm = data['sido_nm']
                    x = data['x']
                    y = data['y']
                    print("sido_cd", data['sido_cd'])
                    return {"cd":cd, "nm":nm, "x": x, "y": y}
            else:
                data = response['result']['resultdata'][0]
                if data['sido_cd'] != "null":
                    cd = data['sido_cd']
                    nm = data['sido_nm']
                    x = data['x']
                    y = data['y']
                    print("sido_cd", data['sido_cd'])
                    return {"cd":cd, "nm":nm, "x": x, "y": y}
        except:
            print("API ERROR (SgisApi_geocoding)")
    
    def transformation(self, x, y, src, dst):
        body = {"src": src, "dst": dst, "posX": x, "posY": y, "accessToken": self.accessToken}
        # cd = ""
        # nm = ""
        # sgg = False
        try:
            response = Request.get(url="https://sgisapi.kostat.go.kr/OpenAPI3/transformation/transcoord.json", data=body)
            print(response, "response")
            return response['result']
        except:
            print("API ERROR (SgisApi_transformation)")


class MeteoApi:
    def __init__(self) -> None:
        pass
    def __call__(self, url):
        try:
            response = Request.get(url= url)
            return response
        except:
            print("API ERROR")

class KorDictApi:
    def __init__(self) -> None:
        # self.dicList = []
        self.body_ori = {"key": "760D799E48CCC86A6594DDDB520689D0", "req_type": "json", "advanced": "y", "method": "start", "type1": "word", "pos": 1}
        self.body = {}
        pass
    def __call__(self, keyword, start=1, num=10, letter_s=2, letter_e=80, state="input", dicList=[]):
        if state == "input":
            self.body = {"q": keyword, "num": num, "start": start, "letter_s": len(keyword), "letter_e": len(keyword), **self.body_ori}
        elif state == "output":
            self.body = {"q": keyword, "num": num, "start": start, "letter_s": letter_s, "letter_e": letter_e, **self.body_ori}
        print(self.body)
        try:
            response = Request.get(url="http://opendict.korean.go.kr/api/search", params=self.body)
            print(dicList,"dicList")
            if (state == "input"):
                for i in dicList:
                    if i == keyword:
                        print("이미 입력한 단어")
                        return False

                if (response['channel']['total'] > 0):
                    dicList.append(keyword)
                    return True
                    # return {"state": True, "dicList": dicList}
                else:
                    print("없는 단어")
                    return False
            elif state == "output":
                if response['channel']['total'] < 1:
                    print('단어 검색결과 없음')
                    return False
                else: 
                    for item in response['channel']['item']:
                        item = item['word'].replace('-',"")
                        for i in dicList:
                            if i != item:
                                print(item, "okay")
                                dicList.append(item)
                                return item
                    print('X로 시작하는 새로운 단어 없음')
                    return False
                    # return {
                    #     "total": response['channel']['total'],
                    #     "num": response['channel']['num'],
                    #     "start": response['channel']['start'],
                    #     "item": response['channel']['item']
                    # }
        except:
            print("API ERROR")

class DamApi:
    def __init__(self) -> None:
        pass
    def __call__(self, damCd):
        mp_encoder = MultipartEncoder(
            fields={
                'mode': 'getHydrDetail',
                'damCd': damCd,
                'param1': 'M'
            }
        )
        
        r = requests.post(
            'https://www.water.or.kr/kor/realtime/sumun/ajaxProc.do',
            data=mp_encoder,
            headers={'Content-Type': mp_encoder.content_type}
        )
        data = json.loads(r.text)
        return {
            "DAM_RSVWT_RT": data["list"][0]['DAM_RSVWT_RT'],
            "TOT_DQTY": data["list"][0]['TOT_DQTY'],
            "RSVR_WAL": data["list"][0]['RSVR_WAL'],
            "DAM_CD": data["list"][0]['DAM_CD'],
        }

    # mp_encoder = MultipartEncoder(
    #     fields={
    #         'mode': 'getHydrDetail',
    #         'damCd': "1006110",
    #         'param1': 'M'
    #     }
    # )
    # r = requests.post(
    #     'https://www.water.or.kr/kor/realtime/sumun/ajaxProc.do',
    #     data=mp_encoder,
    #     headers={'Content-Type': mp_encoder.content_type}
    # )
    # data = json.loads(r.text)
    # print(data["successTitle"])