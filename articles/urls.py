from django.urls import path
from .views import *

urlpatterns = [
    path('' ,ArticleListCreateView.as_view(), name='article_list_and_create'),
    path('<slug:slug>', ArticleDetailView.as_view(), name='article_detail'),
]