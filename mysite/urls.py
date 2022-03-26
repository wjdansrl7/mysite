from django.contrib import admin
from django.urls import  include
from django.urls import path

urlpatterns = [
  path('', include('elections.urls')), #localhost:8000으로 요청이 들어오면 elections.urls로 전달
  path('admin/', admin.site.urls), #app 접속을 위해 include를 씁니다.
]

