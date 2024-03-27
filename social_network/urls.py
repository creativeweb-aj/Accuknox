from django.urls import path
from social_network import views

urlpatterns = [
    path('send-friend-request/<id:int>', views.sendFriendRequest, name='send-friend-request')
]
