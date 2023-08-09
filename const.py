def LOGIN():
    return ["티모", "티모야"]

def LOGOUT():
    return ["종료", "잘가"]

def MENUS():
    return ["검색", "날씨", "미세먼지", "게임", "조사"]

def location_number(data):
    if data == "서울":
        return "02"
    elif data == "인천":
        return "032"
    elif data == "대전":
        return "042"
    elif data == "세종":
        return "044"
    elif data == "부산":
        return "051"
    elif data == "울산":
        return "052"
    elif data == "대구":
        return "053"
    elif data == "광주":
        return "062"
    elif data == "경기":
        return "031"
    elif data == "강원":
        return "033"
    elif data == "충북":
        return "043"
    elif data == "충남":
        return "041"
    elif data == "경북":
        return "054"
    elif data == "경남":
        return "055"
    elif data == "전북":
        return "063"
    elif data == "전남":
        return "061"
    elif data == "제주":
        return "064"
    else:
        return 0

def location_shortner(data):
    if data == "서울특별시":
        return "서울"
    elif data == "인천광역시":
        return "인천"
    elif data == "대전광역시":
        return "대전"
    elif data == "세종특별자치시":
        return "세종"
    elif data == "부산광역시":
        return "부산"
    elif data == "울산광역시":
        return "울산"
    elif data == "대구광역시":
        return "대구"
    elif data == "광주광역시":
        return "광주"
    elif data == "경기도":
        return "경기"
    elif data == "강원도":
        return "강원"
    elif data == "충청북도":
        return "충북"
    elif data == "충청남도":
        return "충남"
    elif data == "경상북도":
        return "경북"
    elif data == "경상남도":
        return "경남"
    elif data == "전라북도":
        return "전북"
    elif data == "전라남도":
        return "전남"
    elif data == "제주특별자치도":
        return "제주"
    else:
        return 0

def damList():
    return {
        "2403201": "감포댐",
        "2011602": "강정고령보",
        "1007601": "강천보",
        "3012601": "공주보",
        "1001210": "광동댐",
        "2009602": "구미보",
        "2503220": "구천댐",
        "1021701": "군남댐",
        "2008101": "군위댐",
        "2010101": "김천부항댐",
        "2009601": "낙단보",
        "2022510": "낙동강하굿둑",
        "2018110": "남강댐",
        "1302210": "달방댐",
        "2014601": "달성보",
        "2201231": "대곡댐",
        "2201230": "대암댐",
        "3008110": "대청댐",
        "3008611": "대청조정지",
        "2021110": "밀양댐",
        "3012602": "백제보",
        "3203110": "보령댐",
        "3303110": "부안댐",
        "2201220": "사연댐",
        "2007601": "상주보",
        "2301210": "선암댐",
        "4001110": "섬진강댐",
        "3010601": "세종보",
        "1012110": "소양강댐",
        "4105210": "수어댐",
        "5004601": "승촌보",
        "2101210": "안계댐",
        "2001110": "안동댐",
        "2001611": "안동조정지",
        "1007602": "여주보",
        "2503210": "연초댐",
        "2012210": "영천댐",
        "3001110": "용담댐",
        "2021210": "운문댐",
        "1007603": "이포보",
        "2002110": "임하댐",
        "2002610": "임하조정치",
        "5101110": "장흥댐",
        "4007110": "주암댐",
        "4204612": "주암역조정치",
        "4104610": "주암조절지댐",
        "5004602": "죽산보",
        "2017601": "창녕함안보",
        "1003110": "충주댐",
        "1003611": "충주조정지",
        "2011601": "칠곡보",
        "5002201": "평림댐",
        "1009710": "평화의댐",
        "2015110": "합천댐",
        "2018611": "합천조정지",
        "2014602": "합천창녕보",
        "1006110": "횡성댐",
        "2002111": "성덕댐",
        "2012101": "보현산댐",
        "1022701": "한탄강댐",
        "2004101": "영주댐",
        "5001701": "담양홍수조절지",
        "5003701": "화순홍수조절지",
        "1019901": "경인아라뱃길",
        "1024801": "귤현보"
    }
# 2403201 감포댐
# 2011602 강정고령보
# 1007601 강천보
# 3012601 공주보
# 1001210 광동댐
# 2009602 구미보
# 2503220 구천댐
# 1021701 군남댐
# 2008101 군위댐
# 2010101 김천부항댐
# 2009601 낙단보
# 2022510 낙동강하굿둑
# 2018110 남강댐
# 1302210 달방댐
# 2014601 달성보
# 2201231 대곡댐
# 2201230 대암댐
# 3008110 대청댐
# 3008611 대청조정지
# 2021110 밀양댐
# 3012602 백제보
# 3203110 보령댐
# 3303110 부안댐
# 2201220 사연댐
# 2007601 상주보
# 2301210 선암댐
# 4001110 섬진강댐
# 3010601 세종보
# 1012110 소양강댐
# 4105210 수어댐
# 5004601 승촌보
# 2101210 안계댐
# 2001110 안동댐
# 2001611 안동조정지
# 1007602 여주보
# 2503210 연초댐
# 2012210 영천댐
# 3001110 용담댐
# 2021210 운문댐
# 1007603 이포보
# 2002110 임하댐
# 2002610 임하조정치
# 5101110 장흥댐
# 4007110 주암댐
# 4204612 주암역조정치
# 4104610 주암조절지댐
# 5004602 죽산보
# 2017601 창녕함안보
# 1003110 충주댐
# 1003611 충주조정지
# 2011601 칠곡보
# 5002201 평림댐
# 1009710 평화의댐
# 2015110 합천댐
# 2018611 합천조정지
# 2014602 합천창녕보
# 1006110 횡성댐
# 2002111 성덕댐
# 2012101 보현산댐
# 1022701 한탄강댐
# 2004101 영주댐
# 5001701 담양홍수조절지
# 5003701 화순홍수조절지
# 1019901 경인아라뱃길
# 1024801 귤현보