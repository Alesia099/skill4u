from .models import User
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from registration.serializer import UserSerializer
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email, password=password)
    except User.DoesNotExist:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def create(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def example_view(request, format=None):
    return Response('Hello')


