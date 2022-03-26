from . import views
from django.urls import path, re_path

app_name = 'elections'
urlpatterns = [
  path('', views.index, name= 'home'), #위의 urls.py와는 달리 include가 없습니다.
  re_path(r'^areas/(?P<area>[가-힣]+)/$', views.areas),
  re_path(r'^areas/(?P<area>[가-힣]+)/results$', views.results),
  re_path(r'^polls/(?P<poll_id>\d+)/$',views.polls),
  re_path(r'^candidates/(?P<name>[가-힣]+)/$', views.candidates)
]
