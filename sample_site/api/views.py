from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import HttpRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.shortcuts import get_object_or_404

from .serializers import BillBoardSerializer, CategorySerializer
from billboard.models import Category, BillBoard


@api_view(['POST', 'GET'])
def api_categories(request: HttpRequest):
    if request.method == 'GET':
        categories = Category.objects.all().order_by('published_at')
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
def api_category_detail(request: HttpRequest, pk):
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
        serializer = CategorySerializer(category, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    else:
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'GET'])
def api_billboards(request: HttpRequest):
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
def api_billboard_detail(request: HttpRequest, pk):
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
