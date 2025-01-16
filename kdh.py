import requests
from bs4 import BeautifulSoup

res = requests.get('https://sw.jnu.ac.kr/sw/8250/subview.do')
soup=BeautifulSoup(res.text,'html.parser')
title_element=soup.find_all(class_="td-subject")
num_element=soup.find_all(class_="td-num")

item=[]

for title_element,num_element in zip(title_element,num_element):
  num_text = num_element.get_text(strip=True)
  if num_text.isdigit():  # 숫자라면 출력   
    title = title_element.find('strong').get_text(strip=True) #find('strong'): 각 <td> 태그 내에서 <strong> 태그를 찾기. get_text(strip=True): <strong> 태그의 텍스트를 추출하고, strip=True를 사용하여 앞뒤 공백을 제거합니다.
    item.append((num_text,title))
item

