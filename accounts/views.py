from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample
)

from .serializers import RegisterSerializer


@extend_schema(
    request=RegisterSerializer,
    responses={201: dict},
    examples=[
        OpenApiExample(
            'Register Example',
            value={
                'username': 'patient1',
                'email': 'patient1@gmail.com',
                'password': 'Patient12345'
            },
            request_only=True
        )
    ]
)
@api_view(['POST'])
def register(request):

    serializer = RegisterSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            {
                'message': 'User created successfully'
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@extend_schema(
    request=dict,
    responses={200: dict},
    examples=[
        OpenApiExample(
            'Login Example',
            value={
                'username': 'patient1',
                'password': 'Patient12345'
            },
            request_only=True
        )
    ]
)
@api_view(['POST'])
def login(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(
        username=username,
        password=password
    )

    if user is not None:

        token, created = Token.objects.get_or_create(
            user=user
        )

        return Response(
            {
                'message': 'Login successful',
                'token': token.key
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {
            'error': 'Invalid username or password'
        },
        status=status.HTTP_401_UNAUTHORIZED
    )