from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from board.models import Article


class IsAuthorMixin(LoginRequiredMixin):

    def get_pk_list(self, dict_):
        pks = []
        for pk in dict_:
            pks.append(pk.get('pk'))
        return pks

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        article_pk = kwargs.get('article_pk')
        response_pk = kwargs.get('response_pk')

        if article_pk:
            pks_dict = request.user.article_set.all().values('pk')
            if article_pk not in self.get_pk_list(pks_dict):
                return self.handle_no_permission()

            return super().dispatch(request, *args, **kwargs)

        elif response_pk:
            pks_dict = request.user.response_set.all().values('pk')

            if response_pk not in self.get_pk_list(pks_dict):
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()


class NotIsAuthorMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        article = Article.objects.filter(pk=kwargs.get('article_pk')).first()

        if article:
            if article in request.user.article_set.all():
                return redirect('board:article_list')
        return super().dispatch(request, *args, **kwargs)