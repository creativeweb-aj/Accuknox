from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from users.models import User
from .models import FriendRequest
from .serializers import FriendRequestSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendFriendRequest(request, id):
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
    return Response(data=data, status=status.HTTP_201_CREATED)
