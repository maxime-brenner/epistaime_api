from rest_framework.serializers import ModelSerializer
from scraper.models import StreamModel, ArticleScraperModel, CategoryArticle

class StreamModelSerializer(ModelSerializer):
    class Meta:
        model = StreamModel
        fields = ["brand_name", "stream"]

class ArticleScraperModelSerializer(ModelSerializer):
    class Meta:
        model = ArticleScraperModel
        fields = "__all__"

class CategoryArticleSerializer(ModelSerializer):
    class Meta:
        model = CategoryArticle
        fields = "__all__"


    