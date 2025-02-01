from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import CreateView

from .models import BillBoard, Category
from .forms import BillBoardForm


def index(request) -> HttpResponse:
    categories = Category.objects.all()
    billboards = BillBoard.objects.all()

    context = {
        'categories': categories,
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
        slug__exact=category_name,
    ).title
    categories = Category.objects.all()
    billboards = BillBoard.objects.filter(
        category__slug__exact=category_name,
    )
    context = {
        'category_name': category_nm,
        'billboards': billboards,
        'categories': categories,
    }
    return render(
        request,
        'billboard/category.html',
        context,
    )


def billboard_detail(request, billboard_id):
    billboard = get_object_or_404(
        BillBoard,
        pk=billboard_id,
    )
    categories = Category.objects.all()
    context = {
        'billboard': billboard,
        'categories': categories,
    }
    return render(
        request,
        'billboard/detail.html',
        context,
    )


class BillBoardCreateView(CreateView):
    template_name = 'billboard/create.html'
    form_class = BillBoardForm
    success_url = reverse_lazy('billboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
