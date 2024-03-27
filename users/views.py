from django.contrib.auth.hashers import check_password
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import SignupSerializer, UserSerializer, LoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = {
            "status": "SUCCESS",
            "data": {"refresh_token": str(refresh), "access_token": str(refresh.access_token)},
            "message": "You are signed up successfully!"
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
    data = {
        "status": "FAIL",
        "data": None,
        "message": "You are account creation failed!"
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # The validate method of the serializer will return the user instance
        user = serializer.validated_data
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        data = {
            "status": "SUCCESS",
            "data": {"refresh_token": str(refresh), "access_token": str(refresh.access_token)},
            "message": "You are logged-in successfully!"
        }
        return Response(data=data, status=status.HTTP_200_OK)
    data = {
        "status": "FAIL",
        "data": None,
        "message": "Invalid Credentials!"
    }
    return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userList(request):
    search = request.query_params.get('search', None)
    users = User.objects.all().order_by('-created_at')

    if search:
        # Check if the search is an exact email match
        if User.objects.filter(email__iexact=search).exists():
            users = users.filter(email__iexact=search)
        else:
            users = users.filter(Q(email__icontains=search) | Q(name__icontains=search))

    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)
