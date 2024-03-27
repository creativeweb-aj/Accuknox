from django.urls import path
from users import views

urlpatterns = [
    path('', views.userList, name='users-list'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
]
