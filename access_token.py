from PyKakao import Message

# 메시지 API 인스턴스 생성

API= Message(service_key = "API 키 입력")

# 카카오 인증코드 발급 URL 생성
auth_url = API.get_url_for_generating_code() 
print(auth_url)
url = "인증 URL 입력"

# 액세스 토큰 발급 받기
access_token = API.get_access_token_by_redirected_url(url)

# 리프레쉬 토큰 발급 받기
import requests

url = "https://kauth.kakao.com/oauth/token"

headers = {
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
}

data = {
    "grant_type": "authorization_code",
    "client_id": "API 키 입력",  # REST API 키
    "redirect_uri": "Redirect URI 입력",  # Redirect URI
    "code": "인증 코드 입력"  # Authorization Code
}

response = requests.post(url, headers=headers, data=data)

# 응답 출력
print("Status Code:", response.status_code)
print("Response Body:", response.json())