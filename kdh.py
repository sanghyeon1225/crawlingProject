from PyKakao import Message
import requests
from bs4 import BeautifulSoup
import time
import schedule
from datetime import datetime

# PyKakao를 사용하여 메시지 전송 API를 초기화
API = Message(service_key="카카오톡 AIP키")

# Access Token 갱신을 위한 URL 및 요청 정보 설정
url = "https://kauth.kakao.com/oauth/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
}
data = {
    "grant_type": "refresh_token",
    "client_id": "4a0e5f8b36abbbc192082ccb4ebbcf59",  # REST API 키
    "refresh_token": "IEaFaMn6sZVFmPnFNsTPcDd2_SXYHFLgAAAAAgo8I-cAAAGUk7RUzLbGP5Eb7W-4"  # Refresh Token
}

# POST 요청으로 Access Token 갱신
response = requests.post(url, headers=headers, data=data)
response_data = response.json()
access_token = response_data.get("access_token")

# 갱신된 Access Token 설정
API.set_access_token(access_token)

# 공지사항 데이터를 저장할 리스트, 각 인덱스는 특정 사이트의 공지사항을 저장
item = [
   [], [], [], [], [], []
]

# 카카오톡 나에게 보내기 기능을 수행하는 함수 (공지사항 제목과 링크를 보냄)
def send_message(site_name, title, link):
    # 메시지 유형 - 텍스트
    message_type = "text"
    # 메시지 내용 구성
    text = f"{site_name} 새 공지사항\n{title}"

    # 링크 정보 설정
    link = {
        "web_url": link,
        "mobile_web_url": link
    }
    # 버튼 제목
    button_title = "바로 확인"

    # 메시지 전송
    API.send_message_to_me(
        message_type=message_type,
        text=text,
        link=link,
        button_title=button_title,
    )

# 소공단 공지사항 크롤링 함수 (html 구조가 달라 별도 구현)
def software():
    global item
    # User-Agent 설정
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    # 소공단 웹페이지 요청 및 데이터 가져오기
    res = requests.get('https://www.sojoong.kr/www/notice/', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 공지사항 제목 요소 가져오기
    title_elements = soup.find_all(class_="alignLeft")

    # 오늘 날짜 가져오기
    today = datetime.today().date()

    # 공지사항 필터링 (오늘 올라온 공지만)
    for title_element in title_elements:
        title_text = title_element.get_text(strip=True)  # 제목 텍스트 추출
        date_text = title_text[-10:]  # 날짜 추출 (마지막 10글자)
        
        # 날짜 문자열을 datetime 객체로 변환
        notice_date = datetime.strptime(date_text, "%Y.%m.%d").date()

        # 오늘 날짜와 비교
        if today == notice_date:
            if "선착순" in title_text:  # 제목에 "선착순"이 포함된 경우 즉시 메시지 전송
                send_message("소공단", title_text, "https://www.sojoong.kr/www/notice/")
            else:  # 그렇지 않으면 item 리스트에 저장
                item[5].append(["소공단", title_text, "https://www.sojoong.kr/www/notice/"])

# 다른 사이트의 공지사항을 크롤링하는 함수
def crawling():
    global item
    # 크롤링할 사이트 정보 (사이트명과 URL, 링크 베이스 경로 포함)
    sites = {
        "소프트웨어공학과": {
            "url": "https://sw.jnu.ac.kr/sw/8250/subview.do",
            "base_link": "https://sw.jnu.ac.kr"
        },
        "인공지능학부": {
            "url": "https://aisw.jnu.ac.kr/aisw/518/subview.do",
            "base_link": "https://aisw.jnu.ac.kr"
        },
        "전자컴퓨터공학부": {
            "url": "https://eceng.jnu.ac.kr/eceng/20079/subview.do",
            "base_link": "https://eceng.jnu.ac.kr"
        },
        "학교 포털1": {
            "url": "https://www.jnu.ac.kr/WebApp/web/HOM/COM/Board/board.aspx?boardID=5",
            "base_link": "https://www.jnu.ac.kr"
        },
        "학교 포털2": {
            "url": "https://www.jnu.ac.kr/WebApp/web/HOM/COM/Board/board.aspx?boardID=5&bbsMode=list&cate=0&page=2",
            "base_link": "https://www.jnu.ac.kr"
        },
        "소공단": {
            "url": "https://www.jnu.ac.kr/WebApp/web/HOM/COM/Board/board.aspx?boardID=10",
            "base_link": "https://www.jnu.ac.kr"
        }
    }
    today = datetime.today()  # 현재 날짜

    # 각 사이트를 순회하며 크롤링
    for site_name, site_info in sites.items():
        print(f"{site_name} 새로운 공지사항")

        # 사이트에서 HTML 데이터 가져오기
        data = requests.get(site_info['url'], headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        
        # 공지사항 리스트 요소 추출
        notice_list = soup.select('tbody > tr:not(.notice)')

        for i in notice_list:
            # 공지사항 제목, 링크, 작성 날짜 추출
            title = i.select_one('td:nth-of-type(2) > a > strong')
            link = i.select_one('td:nth-of-type(2) > a')['href']
            date = i.select_one('td:nth-of-type(4)')

            # 날짜 형식 변환 및 비교
            notice_date = date.text
            if '.' in notice_date:
                notice_date = notice_date.replace('.', '-')
            notice_date = datetime.strptime(notice_date, "%Y-%m-%d")

            diff_date = today - notice_date

            # 제목이 존재하면 처리
            if title:
                pass
            else:
                # 제목 추출 실패 시 다른 경로로 시도
                title = i.select_one('td:nth-of-type(2) > a')
            new_link = site_info['base_link'] + link

            # 오늘 올라온 공지만 처리
            if diff_date.days == 0:
                if "선착순" in title.text:  # 제목에 "선착순" 포함 여부 확인
                    send_message(site_name, title.text, new_link)
                elif site_name == "소프트웨어공학과":
                    item[0].append([site_name, title.text, new_link])
                elif site_name == "인공지능학부":
                    item[1].append([site_name, title.text, new_link])
                elif site_name == "전자컴퓨터공학부":
                    item[2].append([site_name, title.text, new_link])
                elif site_name == "학교 포털1":
                    item[3].append([site_name, title.text, new_link])
                elif site_name == "학교 포털2":
                    item[4].append([site_name, title.text, new_link])

# 저장된 공지사항 데이터를 메시지로 전송하는 함수
def send_scheduled_messages():
    global item
    if item:
        # 각 사이트별 공지사항을 순회하며 메시지 전송
        for item_row in item:
            for item_ in item_row:
                send_message(item_[0], item_[1], item_[2])
        # 전송 후 공지사항 리스트 초기화
        for sublist in item:
            sublist.clear()

# 최종 크롤링을 수행하는 함수
def final_crawling():
    global item
    crawling()
    software()

# 스케줄 설정 및 실행 루프
while True:
    for i in range(16):  # 30분 간격으로 16회 크롤링 (총 8시간)
        final_crawling()
        time.sleep(1800)  # 30분 대기
    send_scheduled_messages()  # 오전 8시에 메시지 전송

    for i in range(20):  # 30분 간격으로 20회 크롤링 (총 10시간)
        final_crawling()
        time.sleep(1800)
    send_scheduled_messages()  # 오후 6시에 메시지 전송

    for i in range(12):  # 30분 간격으로 12회 크롤링 (총 6시간)
        final_crawling()
        time.sleep(1800)
