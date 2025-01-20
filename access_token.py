from PyKakao import Message

# 메시지 API 인스턴스 생성

API= Message(service_key = "내 API 키 입력력")

# 카카오 인증코드 발급 URL 생성
auth_url = API.get_url_for_generating_code() 
print(auth_url)

url = "인증 url 입력"

# 액세스 토큰 발급 받기
access_token = API.get_access_token_by_redirected_url(url)
