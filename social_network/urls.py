from django.urls import path
from social_network import views

urlpatterns = [
    path('send-friend-request/<int:id>', views.sendFriendRequest, name='send-friend-request'),
    path('friend-request-action/<int:id>', views.friendRequestAction, name='friend-request-action'),
    path('friends', views.friendList, name='friends'),
    path('pending-friend-requests', views.pendingFriendRequests, name='pending-friend-requests')
]
