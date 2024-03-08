from django.db.models import Q
from rest_framework import generics
from .models import *
from .serializers import *
from django.db.models import Avg
from custom_auth.utils import get_user_from_request
from rest_framework.response import Response


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

        queryset = queryset.annotate(avg_rating=Avg('review__star'))

        return queryset


class GameDetail(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        queryset = Game.objects.filter(slug=instance.slug).annotate(avg_rating=Avg('review__star'))
        
        instance.avg_rating = queryset.values_list('avg_rating', flat=True).first()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GameReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    

    def get_queryset(self):
        game_slug = self.kwargs['slug'] 
        print(game_slug)
        return Review.objects.filter(game_fk__slug=game_slug)


    def perform_create(self, serializer):
        game_slug = self.kwargs['slug']
        get_user_data = get_user_from_request(self.request)
        user = CustomUser.objects.get(username=get_user_data['username'])
        game = Game.objects.get(slug=game_slug)
        serializer.save(game_fk=game, user_fk=user)


