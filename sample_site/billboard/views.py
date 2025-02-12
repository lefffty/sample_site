from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.conf import settings
from django.core.paginator import Paginator
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
    UserForm,
)


User = get_user_model()


def search_form_function(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    if request.method == 'POST':
        search_form = BillBoardSearchForm(request.POST)
        if search_form.is_valid():
            bb_category = search_form.cleaned_data['billboard_category']
            price_min = search_form.cleaned_data['price_min']
            price_max = search_form.cleaned_data['price_max']
            bb_kind = search_form.cleaned_data['billboard_kind']
            category = Category.objects.get(
                title=bb_category,
            )
            billboards = BillBoard.objects.filter(
                price__range=(price_min, price_max),
                category__slug__exact=category.slug,
                kind__exact=bb_kind,
            )
            categories = Category.objects.all()
            paginator = Paginator(
                billboards,
                settings.PAGINATE_NUMBER,
            )
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
            context['form'] = search_form
            return render(
                request,
                'billboard/index.html',
                context,
            )
    else:
        billboards = BillBoard.objects.all()
        search_form = BillBoardSearchForm()
        paginator = Paginator(
            billboards,
            settings.PAGINATE_NUMBER,
        )
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['form'] = search_form
    return render(
        request,
        'billboard/index.html',
        context,
    )


def profile(request: HttpRequest, username):
    user = get_object_or_404(
        User,
        username=username,
    )

    categories = Category.objects.all()

    billboards = BillBoard.objects.filter(
        author=user
    )

    context = {
        'profile': user,
        'categories': categories,
        'billboards': billboards,
    }

    return render(
        request,
        'billboard/profile.html',
        context
    )


class CategoryListView(ListView):
    paginate_by = 2
    template_name = 'billboard/category.html'

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

    def get_queryset(self):
        billboards = BillBoard.objects.annotate(
            comment_count=Count('comments'),
        )
        return billboards

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

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        title = form.cleaned_data['title']
        send_mail(
            subject='Создание объявления',
            message=f'Вы создали объявление "{title}"!',
            recipient_list=[f'{title}@sample_site.ru'],
            from_email='publish_billboard@sample_site.ru'
        )
        return super().form_valid(form)


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
            'billboard:index',
        )


class UserCreateView(UpdateView):
    model = User
    template_name = 'billboard/user.html'

    def get_object(self, queryset=User.objects.all()):
        username = self.kwargs['username']
        user = User.objects.get(
            username=username,
        )
        return user

    def get_form(self, form_class=UserForm):
        instance = self.get_object()
        form = UserForm(
            self.request.POST or None,
            instance=instance,
        )
        return form

    def get_success_url(self):
        return reverse_lazy(
            'billboard:profile',
            kwargs={
                'username': self.kwargs['username'],
            }
        )


class CommentCreate(CreateView):
    model = Comment
    template_name = 'billboard/detail.html'

    def get_success_url(self):
        return reverse_lazy(
            'billboard:billboard_detail',
            kwargs={
                'pk': self.kwargs['pk'],
            }
        )

    def get_form(self, form_class=CommentForm):
        form = CommentForm(
            self.request.POST or None
        )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.billboard_id = self.kwargs['pk']
        form.save()
        return super().form_valid(form)


class CommentUpdate(UpdateView):
    model = Comment
    template_name = 'billboard/comment.html'

    def get_object(self, queryset=Comment.objects.all()):
        comment = queryset.get(
            pk=self.kwargs['comment_id']
        )
        return comment

    def get_form(self, form_class=CommentForm):
        comment_id = self.kwargs['comment_id']
        instance = Comment.objects.get(
            pk=comment_id,
        )
        form = CommentForm(
            self.request.POST or None,
            instance=instance,
        )
        return form

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

    def get_object(self, queryset=Comment.objects.all()):
        comment = queryset.get(
            pk=self.kwargs['comment_id']
        )
        return comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy(
            'billboard:billboard_detail',
            kwargs={
                'pk': self.kwargs['pk']
            }
        )
