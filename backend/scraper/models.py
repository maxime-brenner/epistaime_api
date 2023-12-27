from django.db import models
from django.db.models import CharField, BooleanField,OneToOneField, CASCADE, DateField
# Create your models here.
class StreamModel(models.Model):
    brand_name= models.CharField(blank=False, max_length=30)
    stream = models.JSONField(blank=True, null=True)

class ArticleScraperModel(models.Model):
    titre = CharField(blank=True, null=True, max_length=1000)
    created = DateField(auto_now=True)
    time = CharField(blank=True, null=True, max_length=10)
    category = CharField(blank=True, null=True, max_length=30)
    url = CharField(blank=True, null=True)
    article_id = CharField(blank=True, null=True)
    posted = BooleanField(default=False)

class CategoryArticle(models.Model):
    name = CharField(blank=True, null=True,unique=False)
    brand_name=CharField(blank=True, null=True)
    emoji = CharField(blank=True, null=True)
    
    