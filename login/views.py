import requests
from django.shortcuts import redirect
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from rest_framework import status
from rest_framework.response import Response
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.naver import views as naver_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from .models import User

# Create your views here.
state = getattr(settings, 'STATE')
BASE_URL = 'http://127.0.0.1:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback/'
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/callback/'
NAVER_CALLBACK_URI = BASE_URL + 'accounts/naver/callback/'

"""
카카오 로그인
"""
def kakao_login(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code")

def kakao_callback(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    code = request.GET.get('code')
    redirect_uri = KAKAO_CALLBACK_URI
    
    """
    Access Token Request
    """
    token_req = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}")
    token_req_json = token_req.json()
 
    error = token_req_json.get("error")
 
    if error is not None:
        return JsonResponse(token_req_json, status=status.HTTP_400_BAD_REQUEST)
    access_token = token_req_json.get("access_token")
    
    """
    Email Request
    """
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    print(profile_json)
    error = profile_json.get("error")
    
    if error is not None:
        return JsonResponse(token_req_json, status=status.HTTP_400_BAD_REQUEST)
    kakao_account = profile_json.get('kakao_account')
    
    """
    kakao_account에서 이메일 외에
    카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 참고
    """
    # print(kakao_account)

    email = kakao_account.get('email')
    
    """
    Signup or Signn Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        
        if social_user.provider != 'kakao':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        
        accept_status = accept.status_code
        
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        
        accpet_json = accept.json()
        accpet_json.pop('user', None)
        
        return JsonResponse(accpet_json)
    
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token' : access_token, 'code' : code}
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    
    
class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
    
    
"""
구글 로그인
"""
def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

def google_callback(request):
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        return JsonResponse(token_req_json, status=status.HTTP_400_BAD_REQUEST)
    access_token = token_req_json.get('access_token')
    
    """
    Email Request
    """
    
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    email_req_json = email_req.json()
    email = email_req_json.get('email')
    
    """
    Signup or Signin Request
    """
    
    try:
        user = User.objects.get(email=email)
        
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        print(data)
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    
class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
    


"""
네이버 로그인
"""
def naver_login(request):
    """
    Code Request
    """
    client_id = getattr(settings, "SOCIAL_AUTH_NAVER_CLIENT_ID")
    return redirect(f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={NAVER_CALLBACK_URI}&state={state}")

def naver_callback(request):
    client_id = getattr(settings, "SOCIAL_AUTH_NAVER_CLIENT_ID")
    client_secret = getattr(settings, "SOCIAL_AUTH_NAVER_SECRET")
    code = request.GET.get('code')
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        return JsonResponse(token_req_json, status=status.HTTP_400_BAD_REQUEST)
    access_token = token_req_json.get('access_token')
    
    """
    Email Request
    """
    profile_request = requests.get("https://openapi.naver.com/v1/nid/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    print(profile_json)
    error = profile_json.get("error")
    
    if error is not None:
        return JsonResponse(token_req_json, status=status.HTTP_400_BAD_REQUEST)
    kakao_account = profile_json.get('response')
    
    """
    kakao_account에서 이메일 외에
    카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 참고
    """
    # print(kakao_account)

    email = kakao_account.get('email')
    
    """
    Signup or Signn Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        
        if social_user.provider != 'naver':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/naver/login/finish/", data=data)
        
        accept_status = accept.status_code
        
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        
        accpet_json = accept.json()
        accpet_json.pop('user', None)
        
        return JsonResponse(accpet_json)
    
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token' : access_token, 'code' : code}
        accept = requests.post(f"{BASE_URL}accounts/naver/login/finish/", data=data)
        accept_status = accept.status_code
        
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    
    
class NaverLogin(SocialLoginView):
    adapter_class = naver_view.NaverOAuth2Adapter
    client_class = OAuth2Client
    callback_url = NAVER_CALLBACK_URI
    
    