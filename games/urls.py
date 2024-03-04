from django.urls import path
from .views import *

urlpatterns = [
    path('' ,GameList.as_view(), name='list'),
    path('<slug:slug>', GameDetail.as_view(), name='detail'),
    path('<slug:slug>/reviews', GameReviewListCreateAPIView.as_view(), name='game_reviews')
]

