from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.views import LoginView

from .forms import *
from .models import *
from .utils import *


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # extra_context = {'title': 'Главная страица'}  # для статического контекста

    def get_context_data(self, *, object_list=None, **kwargs):  # для динамического и статического контекста
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True)  # отображаем только опубликованные статьи


# def index(request):
#     posts = Women.objects.all()
#     context = {'posts': posts,
#                'menu': menu,
#                'title': 'Главная страница',
#                'cat_selected': 0,
#                }
#     return render(request, 'women/index.html', context=context)

# @login_required  # теперь о сайте доступно только для зареганных
def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


def categories(request, catid):
    print(request.POST)
    return HttpResponse(f"<h1>Статьи по категориям<h1><p>{catid}</p>")


def archive(request, year):
    if int(year) > 2020:
        return redirect('home', permanent=False)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')  # eсли нет метода get_absolute_url
    # login_url = '/admin/'  # адрес перенаправления для незареганных пользователей
    login_url = reverse_lazy('home')
    raise_exception = True  # незареганным даступ запрещен

    def get_context_data(self, *, object_list=None, **kwargs):  # для динамического и статического контекста
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     context = {
#         'menu': menu,
#         'title': 'Дoбавление статьи',
#         'form': form
#     }
#     return render(request, 'women/addpage.html', context)


def contact(request):
    return HttpResponse("Обратная связь")


# def login(request):
#     return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):  # для динамического и статического контекста
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {'post': post,
#                'menu': menu,
#                'title': post.title,
#                'cat_selected': post.cat_id,
#                }
#     return render(request, 'women/post.html', context,)


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False  # при переходе на несуществующую категорию будет выдавать 404

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):  # для динамического и статического контекста
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, slug):
#     posts = Women.objects.filter(cat__slug=slug)
#     if len(posts) == 0:
#         raise Http404()
#     context = {'posts': posts,
#                'menu': menu,
#                'title': 'Отображение по рубрикам',
#                'cat_selected': posts[0].cat_id,
#                }
#     return render(request, 'women/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    #  Автоматическая авторизация после регистрации
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
