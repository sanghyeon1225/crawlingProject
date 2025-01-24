from PyKakao import Message
import requests
from bs4 import BeautifulSoup
import time
import schedule
from datetime import datetime

API = Message(service_key="4a0e5f8b36abbbc192082ccb4ebbcf59")

url = "https://kauth.kakao.com/oauth/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
}
data = {
    "grant_type": "refresh_token",
    "client_id": "4a0e5f8b36abbbc192082ccb4ebbcf59",
    "refresh_token": "IEaFaMn6sZVFmPnFNsTPcDd2_SXYHFLgAAAAAgo8I-cAAAGUk7RUzLbGP5Eb7W-4"
}

# POST 요청 보내기
response = requests.post(url, headers=headers, data=data)
response_data = response.json()
access_token = response_data.get("access_token")

API.set_access_token(access_token)

item = []

# 카카오톡 나에게 보내기 기능 (공지사항 제목과 링크를 보냄)
def send_message(site_name,title, link):
    # 메시지 유형 - 텍스트
    message_type = "text"
    # 파라미터
    text = f"{site_name} 새 공지사항\n{title}"

    link = {
        "web_url": link,
        "mobile_web_url": link
    }
    button_title = "바로 확인"

    API.send_message_to_me(
        message_type=message_type,
        text=text,
        link=link,
        button_title=button_title,
    )

# 소공단은 html 구조가 조금 달라 함수를 따로 구현
def software():
    global item
    # User-Agent 설정
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    # 웹페이지 요청 및 데이터 가져오기
    res = requests.get('https://www.sojoong.kr/www/notice/', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 공지사항 제목과 날짜 추출
    title_elements = soup.find_all(class_="alignLeft")

    # 오늘 날짜
    today = datetime.today().date()

    # 공지사항 출력 (오늘 올라온 공지만 필터링)
    for title_element in title_elements:
        title_text = title_element.get_text(strip=True)
        date_text = title_text[-10:]
        # 추출된 날짜를 datetime 객체로 변환
        notice_date = datetime.strptime(date_text, "%Y.%m.%d").date()
        # 날짜 비교
        if today == notice_date:
          if "선착순" in title_text:
            send_message("소공단",title_text,"https://www.sojoong.kr/www/notice/")
          else:
            item[5].append(["소중단",title_text,"https://www.sojoong.kr/www/notice/"])
            



def crawling():
    global item
    # 크롤링할 사이트 리스트
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
    today = datetime.today()  # 현재날짜

    # 각 사이트를 순회하며 크롤링
    for site_name, site_info in sites.items():
        print(f"{site_name} 새로운 공지사항")

        # HTML 데이터 가져오기
        data = requests.get(site_info['url'], headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        # 공통된 부분: tr:not(.notice) > td:nth-of-type(2)
        notice_list = soup.select('tbody > tr:not(.notice)')

        for i in notice_list:
            # 첫 번째 시도: a > strong
            title = i.select_one('td:nth-of-type(2) > a > strong')  # 공지사항 제목
            link = i.select_one('td:nth-of-type(2) > a')['href']  # 공지사항 링크
            date = i.select_one('td:nth-of-type(4)')  # 공지사항 작성 날짜

            notice_date = date.text
            if '.' in notice_date:
                notice_date = notice_date.replace('.', '-')
            notice_date = datetime.strptime(notice_date, "%Y-%m-%d")

            diff_date = today - notice_date

            if title:
                pass
            else:
                # 두 번째 시도: a
                title = i.select_one('td:nth-of-type(2) > a')
            new_link = site_info['base_link'] + link

            if diff_date.days == 0:
              if "선착순" in title.text:
                send_message(site_name,title.text, new_link)
              elif site_name == "소프트웨어공학과":
                item.append([site_name,title.text, new_link])
              elif site_name == "인공지능학부":
                item.append([site_name,title.text, new_link])
              elif site_name == "전자컴퓨터공학부":
                item.append([site_name,title.text, new_link])
              elif site_name == "학교 포털1":
                item.append([site_name,title.text, new_link])
              elif site_name == "학교 포털2":
                item.append([site_name,title.text, new_link])



def send_scheduled_messages():
    global item
    if item:
        for item in item:
          send_message(item[0], item[1],item[2])
        item.clear()


def final_crawling():
  global item
  crawling()
  software()

#저녁 12시에 실행

while True:
  for i in range(16):
    final_crawling()
    time.sleep(1800) #30분에 한번씩 크롤링
  send_scheduled_messages() #오전 8시에 전송
  for i in range(20):
    final_crawling()
    time.sleep(1800) #30분에 한번씩 크롤링
  send_scheduled_messages() # 오후 6시에 전송
  for i in range(12):
    final_crawling()
    time.sleep(1800) #30분에 한번씩 크롤링
    
