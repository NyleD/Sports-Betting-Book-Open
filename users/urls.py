from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    url('verify/', views.face_verification, name='user-verify-face'),
    url('webcam/', views.webcam, name='webcam'),
]


