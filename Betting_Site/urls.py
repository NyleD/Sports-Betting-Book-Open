"""django_project URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from sportsNews import views as sportsNews_views 
from betting import views as betting_views
from chat import views as chat_views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', include('users.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # path('games/'), 
    path('chat/', include('blog.urls')),
    path('chat-rooms/', chat_views.AllRoomsView.as_view(),name='chat-rooms'),
    path('room/<int:id>/', chat_views.RoomDetailView.as_view(),name='room'),
    path('token', chat_views.token, name="token"), 
    path('betting/', betting_views.GroupsView.as_view(), name='groups'),
    path('mybets/', betting_views.BetDetailsView.as_view(), name='mybets'),
    path('betmatch/<int:id>/', betting_views.BetMatchView.as_view(), name='betmatch'),
    path('league/<int:id>/', betting_views.LeagueView.as_view(), name='league'),
    path('group/<int:id>/',  betting_views.GroupView.as_view(), name='group'), 
    path('', sportsNews_views.headings, name='news-headings'), 
    
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +  staticfiles_urlpatterns()

