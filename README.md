# Allauth와 JWT를 이용한 소셜 로그인 구현(구글, 카카오, 네이버)
DRF를 이용하여 소셜 로그인과 일반 회원가입을 구현한 레포지터리입니다. 정상적으로 회원가입, 로그인이 진행되면 <br/> 회원정보와 access_token, refresh_token을 발급합니다.

### 사용법
requirements.txt
```
asgiref==3.5.2
certifi==2022.6.15
cffi==1.15.1
charset-normalizer==2.1.0
cryptography==37.0.4
defusedxml==0.7.1
dj-rest-auth==2.2.5
Django==4.1
django-allauth==0.51.0
djangorestframework==3.13.1
djangorestframework-simplejwt==5.2.0
idna==3.3
oauthlib==3.2.0
pycparser==2.21
PyJWT==1.7.1
python3-openid==3.2.0
pytz==2022.1
requests==2.28.1
requests-oauthlib==1.3.1
sqlparse==0.4.2
urllib3==1.26.11
```
```bash
pip install requirements.txt
```

## API 명세서
### 카카오 로그인
- 요청방식 : get
- 기능 : 카카오 로그인 창으로 이동한다.
- url : http://127.0.0.1:8000/accounts/kakao/login
#### response
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5ODUwNTQ1LCJpYXQiOjE2NTk4NDMzNDUsImp0aSI6IjY5NTg5YzU0MDEzNDQxNjc4NWMzMjFkZmM5ZTllNWNjIiwidXNlcl9pZCI6OH0.zZGG9ZU3iohA8BlMsWlguGICWcrHxjjqrjQfqTWibi0",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MDQ0ODE0NSwiaWF0IjoxNjU5ODQzMzQ1LCJqdGkiOiJhZGRmNjMyZjZjZDY0MWM5OGZmMzY1OWUwZTIwNTdhZSIsInVzZXJfaWQiOjh9.ZJP6gNFOPGmK5Fh2teuNjPkbswv37P1r4cKCSNakuyI"
}
```
---
### 구글 로그인
- 요청방식 : get
- 기능 : 구글 로그인 창으로 이동한다.
- url : http://127.0.0.1:8000/accounts/google/login
#### response
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5ODUwNTQ1LCJpYXQiOjE2NTk4NDMzNDUsImp0aSI6IjY5NTg5YzU0MDEzNDQxNjc4NWMzMjFkZmM5ZTllNWNjIiwidXNlcl9pZCI6OH0.zZGG9ZU3iohA8BlMsWlguGICWcrHxjjqrjQfqTWibi0",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MDQ0ODE0NSwiaWF0IjoxNjU5ODQzMzQ1LCJqdGkiOiJhZGRmNjMyZjZjZDY0MWM5OGZmMzY1OWUwZTIwNTdhZSIsInVzZXJfaWQiOjh9.ZJP6gNFOPGmK5Fh2teuNjPkbswv37P1r4cKCSNakuyI"
}
```
---
### 네이버 로그인
- 요청방식 : get
- 기능 : 네이버 로그인 창으로 이동한다.
- url : http://127.0.0.1:8000/accounts/naver/login
#### response
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5ODUwNTQ1LCJpYXQiOjE2NTk4NDMzNDUsImp0aSI6IjY5NTg5YzU0MDEzNDQxNjc4NWMzMjFkZmM5ZTllNWNjIiwidXNlcl9pZCI6OH0.zZGG9ZU3iohA8BlMsWlguGICWcrHxjjqrjQfqTWibi0",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MDQ0ODE0NSwiaWF0IjoxNjU5ODQzMzQ1LCJqdGkiOiJhZGRmNjMyZjZjZDY0MWM5OGZmMzY1OWUwZTIwNTdhZSIsInVzZXJfaWQiOjh9.ZJP6gNFOPGmK5Fh2teuNjPkbswv37P1r4cKCSNakuyI"
}
```
---
### 일반 로그인
- 요청방식 : POST
- 기능 : 네이버 로그인 창으로 이동한다.
- url : http://127.0.0.1:8000/accounts/registration/
- 예시 
#### request
```json
{
    "email" : "thduf0623@naver.com",
    "password1" : "abcdefufufu",
    "password2" : "abcdefufufu"
}
```
#### response
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5ODQ4Mzg3LCJpYXQiOjE2NTk4NDExODcsImp0aSI6ImUyNDBmYjIzZmFkODQ2NTJiNjA3ODcyNGRiZWZkMzc2IiwidXNlcl9pZCI6N30.Mr8beIrylDNchytOeh-6vc31-B2zMriHZedvn3Xfu2A",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MDQ0NTk4NywiaWF0IjoxNjU5ODQxMTg3LCJqdGkiOiIyZTJmNWZhNDAwM2E0YTk4ODhmZjkyNDFiMzJmMjU2YyIsInVzZXJfaWQiOjd9.IiDHSTZtO4ykrguXaCdn9DR_pLcUbIG0Q8NkrSo03U8",
    "user": {
        "pk": 7,
        "email": "thduf0623@naver.com",
        "first_name": "",
        "last_name": ""
    }
}
```
