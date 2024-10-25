from django.contrib import admin

from .forms import ArticleCreateForm
from .models import *


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleCreateForm


admin.site.register(Category)
admin.site.register(Response)
