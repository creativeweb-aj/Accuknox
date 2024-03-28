from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.core.cache import cache
from users.models import User
from .models import FriendRequest
from .serializers import FriendRequestSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sendFriendRequest(request, id):
    # Custom rate limit key
    rate_limit_key = f"send_friend_request_{request.user.id}"
    rate_limit = cache.get(rate_limit_key, 0)

    # Check if rate limit exceeded 3 requests per minute
    if rate_limit >= 3:
        data = {
            "status": "FAIL",
            "data": None,
            "message": "Rate limit exceeded. Try again in a minute."
        }
        return Response(data=data, status=status.HTTP_429_TOO_MANY_REQUESTS)

    from_user = request.user
    to_user_id = id

    if not to_user_id:
        data = {
            "status": "FAIL",
            "data": None,
            "message": "Please provide id of user"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    if from_user.id == to_user_id:
        data = {
            "status": "FAIL",
            "data": None,
            "message": "You cannot send a friend request to yourself"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    try:
        to_user = User.objects.get(id=to_user_id)
    except User.DoesNotExist:
        data = {
            "status": "FAIL",
            "data": None,
            "message": "User not found!"
        }
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    friend = FriendRequest.objects.filter(from_user=from_user, to_user=to_user)
    if friend:
        if friend.status is "pending":
            data = {
                "status": "FAIL",
                "data": None,
                "message": "Friend request already sent!"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        elif friend.status is "accepted":
            data = {
                "status": "FAIL",
                "data": None,
                "message": "You are already friend!"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                "status": "FAIL",
                "data": None,
                "message": "Your friend request is rejected!"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    friendRequest = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
    serializer = FriendRequestSerializer(friendRequest)
    data = {
        "status": "SUCCESS",
        "data": serializer.data,
        "message": "Friend request is sent!"
    }

    # After successfully creating the friend request, increment the rate limit counter
    cache.set(rate_limit_key, rate_limit + 1, timeout=60)  # Increment and set a 60-second timeout
    return Response(data=data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def friendRequestAction(request, id):
    action = request.data.get('action', None)
    if action is None or action == "":
        data = {
            "status": "FAIL",
            "data": None,
            "message": "Please send action for friend request!"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        if action not in ["accepted", "rejected"]:
            data = {
                "status": "FAIL",
                "data": None,
                "message": "Please send right action for friend request!"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    friend = FriendRequest.objects.filter(id=id, to_user=request.user).first()
    if friend is None:
        data = {
            "status": "FAIL",
            "data": None,
            "message": "Friend request not found!"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        friend.status = action
        friend.save()
        if action == "accepted":
            data = {
                "status": "SUCCESS",
                "data": None,
                "message": "Friend request accepted!"
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = {
                "status": "SUCCESS",
                "data": None,
                "message": "Friend request rejected!"
            }
            return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friendList(request):
    friends = FriendRequest.objects.filter(from_user=request.user, status="accepted").order_by("-created_at")
    friendRequestSerializer = FriendRequestSerializer(friends, many=True)
    data = {
        "status": "SUCCESS",
        "data": {"friends": friendRequestSerializer.data},
        "message": "Friends list has been sent!"
    }
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pendingFriendRequests(request):
    friends = FriendRequest.objects.filter(to_user=request.user, status="pending").order_by("-created_at")
    friendRequestSerializer = FriendRequestSerializer(friends, many=True)
    data = {
        "status": "SUCCESS",
        "data": {"pending": friendRequestSerializer.data},
        "message": "Pending friend requests has been sent!"
    }
    return Response(data=data, status=status.HTTP_200_OK)
