from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import BillBoard, Category


def index(request) -> HttpResponse:
    billboards = BillBoard.objects.all()

    context = {
        'billboards': billboards
    }

    return render(
        request,
        'billboard/index.html',
        context,
    )


def category_list(request, category_name) -> HttpResponse:
    category_nm = get_object_or_404(
        Category,
        name__exact=category_name,
    )
    billboards = BillBoard.objects.filter(
        category__name__exact=category_name,
    )
    context = {
        'category_name': category_nm,
        'billboards': billboards,
    }
    return render(
        request,
        'billboard/category.html',
        context,
    )
