from rest_framework.serializers import ModelSerializer
from api.models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'content_raw', 'account', 'created', 'tweet_id', 'media_link', 'article_url', 'generated_text', 'isPosted', 'isDraft']