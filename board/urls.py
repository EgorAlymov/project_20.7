from django.urls import path

from .views import *

app_name = 'board'
urlpatterns = [
    #article
    path('', ArticleList.as_view(), name='article_list'),
    path('<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('update/<int:article_pk>', ArticleUpdate.as_view(), name='article_update'),
    path('<int:article_pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    #response
    path('<int:article_pk>/response', ResponseList.as_view(), name='response_list'),
    path('<int:article_pk>/create_Response', ResponseCreate.as_view(), name='response_create'),
    path('<int:article_pk>/response/<int:response_pk>/accept', ResponseAccept.as_view(), name='response_accept'),
    path('<int:article_pk>/response/<int:response_pk>/reject', ResponseReject.as_view(), name='response_reject'),
    path('response/<int:response_pk>/delete', ResponseDelete.as_view(), name='response_delete'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    #views  
    path('category/<slug:name>', CategoryView.as_view(), name='category'),
    path('by_author/<slug:name>', ByAuthorView.as_view(), name='by_author'),

]