from rest_framework import serializers
from custom_auth.serializers import CustomUserSerializer
from .models import *


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class GameSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    avg_rating = serializers.FloatField(read_only=True)


    class Meta:
        model = Game
        fields = ['slug', 'title', 'genre', 'description', 'price', 'avg_rating', 'header_image_src']
    
    def to_representation(self, instance):
        # Round the avg_rating field to one number after the comma
        representation = super().to_representation(instance)
        if representation['avg_rating'] is not None:
            representation['avg_rating'] = round(representation['avg_rating'], 1)
        else:
            representation['avg_rating'] = 0
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'star', 'description', 'username']

    def get_username(self, obj):
        return obj.user_fk.username