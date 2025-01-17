import requests # request 라이브러리
from bs4 import BeautifulSoup # BeautifulSoup 라이브러리
import time # sleep을 사용하기 위한 time 라이브러리리

# User-Agent를 설정하여 웹 브라우저에서의 요청인 것처럼 설정
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# 마지막으로 작성된 공지사항의 제목을 저장 (처음만 임의로 작성해줌)
last_notice = '(★2022.1학기부터 변경) 동일교과목 배제 신청 업무처리 절차 변경 안내'

# 소프트웨어공학과 학과 홈페이지 (프로토콜, 도메인 네임)
base_link = 'https://sw.jnu.ac.kr'

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
        print("새로운 공지사항 제목:", title.text)
        print("링크:", base_link + link)
        
        
    # 새로 작성된 게시글을 모두 알림으로 보낸 후, 마지막으로 작성된 게시글을 last_notice에 저장
    recently_notice = soup.select_one('tr:not(.notice) > td > a > strong')
    last_notice = recently_notice.text
    print("현재 마지막 공지사항: ", last_notice)
    
    time.sleep(1800)