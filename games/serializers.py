from rest_framework import serializers
from .models import *


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class GameSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ['slug', 'title', 'genre']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['star', 'description']