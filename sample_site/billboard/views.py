from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpRequest
from django.views.generic import CreateView, ListView, DetailView

from .models import BillBoard, Category
from .forms import BillBoardForm


class BillBoardListView(ListView):
    template_name = 'billboard/index.html'
    context_object_name = 'billboards'
    model = BillBoard

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryListView(ListView):
    template_name = 'billboard/category.html'
    context_object_name = 'billboards'

    def get_queryset(self):
        return BillBoard.objects.filter(
            category__slug__exact=self.kwargs['category_name']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = Category.objects.get(
            slug=self.kwargs['category_name']
        )
        return context


class BillBoardDetailView(DetailView):
    template_name = 'billboard/detail.html'
    model = BillBoard

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class BillBoardCreateView(CreateView):
    template_name = 'billboard/create.html'
    form_class = BillBoardForm
    success_url = reverse_lazy('billboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
