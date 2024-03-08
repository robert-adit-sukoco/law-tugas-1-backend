from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['slug', 'author', 'title', 'content', 'published_at']

    def get_author(self, obj):
        if isinstance(obj, dict):
            # obj is an OrderedDict, likely when serializing a queryset
            author_username = obj.get('author', {}).get('username')
            return author_username
        else:
            # obj is an instance of the Article model
            return obj.author.username if obj.author else None

