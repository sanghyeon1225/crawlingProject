import requests # request 라이브러리
from bs4 import BeautifulSoup # BeautifulSoup 라이브러리
import time # sleep을 사용하기 위한 time 라이브러리리
from PyKakao import Message 

# User-Agent를 설정하여 웹 브라우저에서의 요청인 것처럼 설정
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# 마지막으로 작성된 공지사항의 제목을 저장 (처음만 임의로 작성해줌)
last_notice = '2025학년도 2학기 해외 파견 교환학생 선발 안내'

# 소프트웨어공학과 학과 홈페이지 (프로토콜, 도메인 네임)
base_link = 'https://sw.jnu.ac.kr'

# 액세스 토큰 할당
API = Message(service_key = "내 API 키 입력")
access_token = '액세스 토큰 입력'
API.set_access_token(access_token)

# 카카오톡 나에게 보내기 기능 (공지사항 제목과 링크를 보냄)
def send_message(title, new_link):
    
    # 메시지 유형 - 텍스트
    message_type = "text"
    # 파라미터
    text = f"[소프트웨어공학과 새 공지사항]\n{title}\n{new_link}"

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
    
while(1):
    # 주어진 URL에서 html 데이터를 추출하여 data에 저장
    data = requests.get('https://sw.jnu.ac.kr/sw/8250/subview.do',headers=headers)

    # BeautifulSoup 라이브러리를 활용하여 html 문서를 구조화
    soup = BeautifulSoup(data.text, 'html.parser')

    # BeautifulSoup의 select()를 활용하여 CSS 선택자로 필요한 HTML 요소를 선택함
    # <tr> 아래의 <td>의 두 번째 요소들을 notice_list에 저장
    notice_list = soup.select('tr:not(.notice) > td:nth-of-type(2)')

    # 마지막 공지사항 제목과 일치할 때까지 notice_list에서 공지사항을 하나씩 불러옴  
    for i in notice_list:
        title = i.select_one('a > strong')
        if title.text == last_notice: # last_notice와 title이 같다면 종료(새롭게 작성된 게시글을 모두 불러왔다는 의미)
            break
        link = i.select_one('a')['href'] # 공지사항에서 <a>태그의 href속성을 추출하여 링크 저장 
        # print("새로운 공지사항 제목:", title.text)
        # print("링크:", base_link + link)
        new_link = base_link + link
        send_message(title.text, new_link)
        
    # 새로 작성된 게시글을 모두 알림으로 보낸 후, 마지막으로 작성된 게시글을 last_notice에 저장
    recently_notice = soup.select_one('tr:not(.notice) > td > a > strong')
    last_notice = recently_notice.text
    print("현재 마지막 공지사항: ", last_notice)
    
    time.sleep(1800)