import requests # request 라이브러리
from bs4 import BeautifulSoup # BeautifulSoup 라이브러리
import time # sleep을 사용하기 위한 time 라이브러리리
from PyKakao import Message 
from datetime import datetime

# 리프레쉬 토큰으로 새로운 액세스 토큰 발급 받기
API = Message(service_key = "API 키 입력")

url = "https://kauth.kakao.com/oauth/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
}
data = {
    "grant_type": "refresh_token",
    "client_id": "API 키 입력", 
    "refresh_token": "refresh token 입력"
}

# POST 요청 보내기
response = requests.post(url, headers=headers, data=data)
response_data = response.json()
access_token = response_data.get("access_token")

API.set_access_token(access_token)

# 카카오톡 나에게 보내기 기능 (공지사항 제목과 링크를 보냄)
def send_message(title, new_link, site_name):
    
    # 메시지 유형 - 텍스트
    message_type = "text"
    # 파라미터
    text = f"[{site_name} 새 공지사항]\n\n{title}\n\n{new_link}"

    link = {
                "web_url": "www.naver.com",
                "mobile_web_url": "www.naver.com"
            }
    button_title = "바로 확인"

    API.send_message_to_me(
        message_type=message_type, 
        text=text,
        link=link,
        button_title=button_title,
    )
    

def crawling():
    # User-Agent를 설정하여 웹 브라우저에서의 요청인 것처럼 설정
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

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
        "공학교육혁신센터": {
            "url": "https://icee.jnu.ac.kr/icee/17915/subview.do",
            "base_link": "https://icee.jnu.ac.kr"
        }
        
    }
    today = datetime.today() # 현재날짜
    
    # 각 사이트를 순회하며 크롤링
    for site_name, site_info in sites.items():
        print(f"{site_name} 공지사항 확인")
        count = 0
        # HTML 데이터 가져오기
        data = requests.get(site_info['url'], headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        # 공통된 부분: tr:not(.notice) > td:nth-of-type(2)
        notice_list = soup.select('tbody > tr:not(.notice)')

        for i in notice_list:
            # 첫 번째 시도: a > strong
            title = i.select_one('td:nth-of-type(2) > a > strong') # 공지사항 제목
            link = i.select_one('td:nth-of-type(2) > a')['href'] # 공지사항 링크
            date = i.select_one('td:nth-of-type(4)') # 공지사항 작성 날짜
            
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
            
            if (diff_date.days == 0):
                send_message(title.text, new_link, site_name)
                count = count + 1
        if count == 0:
            print(f"{site_name}에 새로운 공지사항 없습니다.")
        print("\n")
    
crawling()



