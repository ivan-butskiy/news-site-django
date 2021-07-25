from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации.')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', context={'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', context={'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def contact(request):
    """Send e-mail function"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'butskiy95@ukr.net',
                      ['butskiy1795@gmail.com'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо успешно отправлено :)')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки.')
        else:
            messages.error(request, 'Ошибка отправки.')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {"form": form})


class HomeNews(MyMixin, ListView):
    # По-умолчанию данные из модели передаются в шаблон директивой object_list
    model = News    # будут получены все данные из этой модели
    template_name = 'news/home_news_list.html'    # по-умолчанию ищет шаблон news/news_list.html
    context_object_name = 'news'    # название объекта вместо object_list
    # extra_context = {'title': 'Главная страница'}    # передача других данных в контекст шаблона.
    # Желательно для статичных данных. Для списков и динамичных данных не рекомендуется
    # queryset = News.objects.select_related('category')   # атрибут для оптимизации SQL запроса вместо метода .select_related()
    mixin_prob = 'hello, world'
    paginate_by = 2

    # Переопределим родительский метод для динамичных данных
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        # context['title'] = self.get_upper('Главная страница')
        # context['mixin_prob'] = self.get_prob()
        return context

    # переопределим родительский метод для кастомного/отфильтрованного запроса
    def get_queryset(self):
        # select_related() метод используется для оптимизации SQL запроса
        # со связью ForeignKey. Для ManyToMany используется другой метод
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False    # не разрешаем показ пустых списков, вместо 500 ошибки
    paginate_by = 2

    # url параметр находится в self (у него есть соответствующий атрибут в виде словаря)
    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class ViewNews(DetailView):
    # шаблон по-умолчанию должен именоваться news/news_detail.html
    model = News
    # pk_url_kwarg = 'news_id'    # наш pk приходит в виде параметра news_id
    # template_name = 'news/news_detail.html'
    # по-умолчанию в контекст шаблона передается object
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    # По сути надо только связать данный класс с формой
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # по-умолчанию редирект на созданную новость происходит благодаря функции get_absolute_url() в модели News
    # success_url = '/'    # кастомное перенаправление. Можно указывать либо адрес в формате '/url'
    # либо функцию reverse_lazy, но не reverse
    # success_url = reverse_lazy('home')
    login_url = '/admin/'    # Перенаправить на вход в админку для неавторизованых
    # raise_exception = True    # Выбросить исключение для неавторизованых

    # Тест
    # def get_context_data(self, **kwargs):
    #     context = super(ViewNews, self).get_context_data()
    #     context['title'] = 'Новость'
    #     return context


# def index(request):
#     news = News.objects.all()
#     context = {'news': news, 'title': 'Список новостей'}
#     return render(request=request, template_name='news/index.html', context=context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request=request, template_name='news/category.html', context={'news': news, 'category': category})


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, template_name='news/view_news.html', context={'news_item': news_item})


# Функция-контроллер для формы, не связанной с моделью
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             news = News.objects.create(**form.cleaned_data)
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, template_name='news/add_news.html', context={'form': form})


# Функция-контроллер для формы, связанной с моделью
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
