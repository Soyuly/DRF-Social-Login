from django.contrib import admin
from django.urls import path, include
from login import views

urlpatterns = [
    path('registration/', include('dj_rest_auth.registration.urls')),
    # 카카오 로그인
    path('kakao/login', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),  
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_to_django'),
    
    # 구글 로그인
    path('google/login', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),  
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_to_django'),
    
    # 네이버 로그인
    path('naver/login', views.naver_login, name='naver_login'),
    path('naver/callback/', views.naver_callback, name='naver_callback'),  
    path('naver/login/finish/', views.NaverLogin.as_view(), name='naver_login_to_django'),
    
]