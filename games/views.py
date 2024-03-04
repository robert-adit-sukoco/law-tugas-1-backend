from django.db.models import Q
from rest_framework import generics
from .models import *
from .serializers import *
from custom_auth.utils import get_user_from_request


# Create your views here.
class GameList(generics.ListAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        queryset = Game.objects.all()
        title_query = self.request.query_params.get('title', None)
        genre_query = self.request.query_params.getlist('genre', None)

        if title_query:
            queryset = queryset.filter(title__icontains=title_query)

        if genre_query:
            genre_filter = Q(genre__id__in=genre_query[0])
            for genre_id in genre_query[1:]:
                genre_filter |= Q(genre__id=genre_id)
            queryset = queryset.filter(genre_filter)

        return queryset


class GameDetail(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'slug'


class GameReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        game_slug = self.kwargs['slug'] 
        return Review.objects.filter(game_fk__slug=game_slug)


    def perform_create(self, serializer):
        get_user_data = get_user_from_request(self.request)
        game_slug = self.kwargs['slug']
        print(get_user_data)
        user = CustomUser.objects.get(username=get_user_data['username'])
        game = Game.objects.get(slug=game_slug)
        serializer.save(game_fk=game, user_fk=user)


