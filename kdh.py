import requests
from bs4 import BeautifulSoup
import time


recent_num=0

def function():

  global recent_num  # 함수 내에서 전역 변수 recent_num을 사용한다고 명시

  # User-Agent를 설정하여 웹 브라우저에서의 요청인 것처럼 설정
  headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

  #사용자 정의 헤더를 포함해 웹페이지에 get 요청
  res = requests.get('https://sw.jnu.ac.kr/sw/8250/subview.do',headers=headers) 

  # 답받은 HTML 내용을 BeautifulSoup을 사용해 데이터 추출
  # 'html.parser'는 파서의 종류로, HTML을 해석할 때 사용되는 방법
  soup=BeautifulSoup(res.text,'html.parser') 

  # class="td-subject"인 모든 HTML 요소를 찾아서 'title_element'에 저장
  title_element=soup.find_all(class_="td-subject")

  # class="td-num"인 모든 HTML 요소를 찾아서 'num_element'에 저장
  num_element=soup.find_all(class_="td-num")

  # 정보를 저장할 리스트
  item=[]
  #가장 최근에 전송한 공지사항의 번호를 저장

  # html 코드에서 게시물 번호와 제목을 찾는 과정
  for title_element,num_element in zip(title_element,num_element):
    # html 코드에서 text만 추출
    num_text = num_element.get_text(strip=True)

    # num_text가 숫자라면 아래 코드 실행
    if num_text.isdigit() and int(num_text)>recent_num:

      #get_text(strip=True): strip=True를 사용하여 앞뒤 공백을 제거 
      title = title_element.get_text(strip=True) 

      # 번호(num_text)와 제목(title)을 묶어서 item 리스트에 추가
      item.append([num_text,title])

      
  

  # item이 있다면 recent_num에 새로운 숫자 저장, item 내용 출력
  if item: 
    recent_num=item[0][0]
    print("최신 공지사항")
    # 카카오톡 보내는 코드 대신 일단 출력하는 코드 작성
    for item in item:
      print(f"공지사항 번호: {item[0]}, 공지사항 제목: {item[1]}")
    #list 비우기
    item.clear()
  

# 15분마다 실행
while True:
    function()        # 함수 호출
    time.sleep(900)