from django.db import models
from django.db.models import JSONField, DateField, IntegerField, BooleanField, CharField, Choices, ManyToManyField, OneToOneField
from scraper.models import CategoryArticle, ArticleScraperModel
# Create your models here.
class Post(models.Model):
    EPISTAIME="EPM"
    INFO="INFO"
    ACCOUNT = [
        (EPISTAIME, "epistaime"),
        (INFO, "1fo")
    ]

    content = JSONField(blank=True, null=True)
    content_raw = CharField(blank=True, null=True, max_length=600)
    account = CharField(choices=ACCOUNT, default="EPM")
    created = DateField(auto_now=True)
    tweet_id = CharField(blank=True, null=True)
    media_link = CharField(blank=True, null=True, max_length=1000)
    generated_text = CharField(blank=True, null=True, max_length=500)
    article_url = CharField(blank=True, null=True, max_length=1000)
    isPosted = BooleanField(default=False)
    isDraft =  BooleanField(default=True)
    category = ManyToManyField(CategoryArticle, blank=True, null=True)
    impressions = IntegerField(blank=True, null=True)

