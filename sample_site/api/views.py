from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import HttpRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .serializers import (
    BillBoardSerializer,
    CategorySerializer,
    CommentSerializer,
    UserSerializer,
)
from billboard.models import (
    Category,
    BillBoard,
    Comment,
)


User = get_user_model()


@api_view(['POST', 'GET'])
def api_categories(request: HttpRequest) -> Response:
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)
    else:
        serializer = CategorySerializer(
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_category_detail(request: HttpRequest, pk) -> Response:
    category = get_object_or_404(
        Category,
        pk=pk,
    )
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    else:
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'GET'])
def api_billboards(request: HttpRequest) -> Response:
    if request.method == 'GET':
        billboards = BillBoard.objects.all()
        serializer = BillBoardSerializer(
            billboards,
            many=True,
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
    else:
        serializer = BillBoardSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_billboard_detail(request: HttpRequest, pk) -> Response:
    billboard = get_object_or_404(
        BillBoard,
        pk=pk,
    )
    if request.method == 'GET':
        serializer = BillBoardSerializer(billboard)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = BillBoardSerializer(
            billboard,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_206_PARTIAL_CONTENT,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        billboard.delete()
        return Response(
            billboard.data,
            status=status.HTTP_202_ACCEPTED,
        )


@api_view(['GET', 'POST'])
def api_comments(request: HttpRequest) -> Response:
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
    serializer = CommentSerializer(
        data=request.data,
        many=True,
    )
    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['GET', 'POST'])
def api_users(request: HttpRequest) -> Response:
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
    serializer = UserSerializer(
        data=request.data,
        many=True,
    )
    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['GET', 'PATCH', 'PUT'])
def api_user(request: HttpRequest, pk) -> Response:
    user = User.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        user.delete()
        return Response(
            user.data,
            status=status.HTTP_202_ACCEPTED
        )
