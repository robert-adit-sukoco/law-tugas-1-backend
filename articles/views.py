from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Article
from custom_auth.models import CustomUser
from .serializers import ArticleSerializer
from custom_auth.utils import get_user_from_request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt

# API view to list all articles
class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        get_user_data = get_user_from_request(self.request)
        user_obj = CustomUser.objects.get(username=get_user_data['username'])
        serializer.save(author=user_obj)


# API view to view article detail
class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

# API view to create a new article
class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]  # Example permission class, modify as needed

