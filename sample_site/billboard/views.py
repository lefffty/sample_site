from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.db.models import Count
from django.http import HttpRequest, HttpResponse

from .models import (
    BillBoard,
    Category,
    Comment,
)
from .forms import (
    BillBoardForm,
    CommentForm,
    BillBoardSearchForm,
)


def search_form_function(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        search_form = BillBoardSearchForm(request.POST)
        if search_form.is_valid():
            bb_kind = search_form.cleaned_data['billboard_kind']
            price_min = search_form.cleaned_data['price_min']
            price_max = search_form.cleaned_data['price_max']
            billboards = BillBoard.objects.filter(
                # price__range=(price_min, price_max),
                billboard_kind__exact=bb_kind,
            )
            context = {
                'billboards': billboards,
            }
            return render(
                request,
                'billboard/index.html',
                context,
            )
    else:
        billboards = BillBoard.objects.all()
        search_form = BillBoardSearchForm()
    categories = Category.objects.all()
    context = {
        'billboards': billboards,
        'categories': categories,
        'form': search_form,
    }
    return render(
        request,
        'billboard/index.html',
        context,
    )


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
        form = CommentForm()
        context['form'] = form
        comments = Comment.objects.filter(
            billboard__exact=self.kwargs['pk']
        )
        context['comments'] = comments
        return context

    def get_queryset(self):
        BillBoard.objects.annotate(
            comment_count=Count('comment'),
        )
        return super().get_queryset()


class BillBoardCreateView(CreateView):
    template_name = 'billboard/create.html'
    form_class = BillBoardForm
    success_url = reverse_lazy('billboard:index')
    initial = {
        'price': 0.0,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class BillBoardUpdateView(UpdateView):
    model = BillBoard
    template_name = 'billboard/create.html'
    form_class = BillBoardForm
    success_url = reverse_lazy('billboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class BillBoardDeleteView(DeleteView):
    model = BillBoard
    template_name = 'billboard/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['billboard'] = BillBoard.objects.get(
            pk=self.kwargs['pk'],
        )
        return context

    def get_success_url(self):
        return reverse_lazy(
            'billboard:create_billboard',
        )


class CommentCreate(CreateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy(
            'billboard:billboard_detail',
            kwargs={
                'pk': self.kwargs['pk'],
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.billboard_id = self.kwargs['pk']
        return super().form_valid(form)


class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'billboard/comment.html'

    def get_success_url(self):
        return reverse_lazy(
            'billboard:billboard_detail',
            kwargs={
                'pk': self.kwargs['pk'],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CommentDelete(DeleteView):
    model = Comment
    template_name = 'billboard/comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy(
            'billboard:create_billboard',
            kwargs={
                'pk': self.kwargs['pk']
            }
        )
