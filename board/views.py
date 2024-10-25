from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
# from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView

from .forms import ArticleCreateForm, ResponseCreateForm
from .models import *
from .utils.permissions import IsAuthorMixin, NotIsAuthorMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'board/front.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ArticleList(ListView):
    model = Article
    context_object_name = 'article_list'
    queryset = Article.objects.order_by('dateCreation')


class ArticleDetail(DetailView):
    model = Article
    context_object_name = 'article'


class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'board/crud/article_create.html'

    def get_success_url(self):
        return reverse('board:article_list')

    def form_valid(self, form):
        article = form.save(commit=False)
        user = self.request.user
        article.author = user
        return super().form_valid(form)


class ArticleUpdate(IsAuthorMixin, UpdateView):
    model = Article
    pk_url_kwarg = 'Article_pk'
    form_class = ArticleCreateForm
    template_name = 'board/crud/article_create.html'

    def get_success_url(self):
        return reverse('board:article_list')

    def form_valid(self, form):
        messages.success(self.request, 'Success!')
        return super().form_valid(form)


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'board/crud/article_delete.html'
    success_url = '/board/'
    permission_required = 'board.article_delete'
    context_object_name = 'article'

    def get_object(self, **kwargs):
        article_id = self.kwargs.get('article_pk')
        article = Article.objects.get(pk=article_id)
        return article


class ResponseList(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        article_pk = kwargs['article_pk']
        article = Article.objects.get(pk=article_pk)
        rp = Response.objects.order_by('dateCreation').filter(article=article)

        context = {
            'response': rp,
            'article': article
        }

        return render(request, 'board/response_list.html', context)


class ResponseCreate(NotIsAuthorMixin, View):
    def get(self, request, **kwargs):
        form = ResponseCreateForm(request.ARTICLE or None)
        article = Article.objects.get(pk=kwargs['article_pk'])

        context = {
            'form': form,
            'article': article
        }

        return render(request, 'board/crud/response_create.html', context)

    def article(self, request, *args, **kwargs):
        form = ResponseCreateForm(request.ARTICLE)
        user = request.user
        article_pk = kwargs['article_pk']

        if form.is_valid():
            response = form.save(commit=False)
            response.author = user
            response.article = Article.objects.get(pk=article_pk)
            response.save()

        return redirect('board:article_list')


class ResponseAccept(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        response_pk = kwargs['response_pk']

        response = Response.objects.get(pk=response_pk)
        response.approved = True
        response.save()

        return redirect(request.META['HTTP_REFERER'])


class ResponseReject(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        response_pk = kwargs['response_pk']

        response = Response.objects.get(pk=response_pk)
        response.approved = False
        response.save()

        return redirect(request.META['HTTP_REFERER'])


class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'board/crud/response_delete.html'
    success_url = '/board/'
    permission_required = ('board.response_delete')
    context_object_name = 'response'

    def get_object(self, **kwargs):
        response_id = self.kwargs.get('response_pk')
        response = Response.objects.get(pk=response_id)
        return response


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'article': request.user.article_set.all(),
        }
        return render(request, 'board/dashboard.html', context)


class CategoryView(ListView):
    def get(self, request, *args, **kwargs):
        category = Category.objects.get(name=kwargs['name'])
        ar = Article.objects.order_by('dateCreation').filter(category=category)

        context = {
            'category': category,
            'article': ar,
        }

        return render(request, 'board/category_list.html', context)


class ByAuthorView(ListView):
    def get(self, request, *args, **kwargs):
        author = User.objects.get(username=kwargs['name'])
        ar = Article.objects.order_by('dateCreation').filter(author=author)

        context = {
            'author': author,
            'article': ar,
        }

        return render(request, 'board/by_author.html', context)