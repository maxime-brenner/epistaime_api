from django.contrib import admin
from scraper.models import StreamModel, ArticleScraperModel, CategoryArticle

# Register your models here.
class CatgoryArticleAdmin(admin.ModelAdmin):
    list_display=["name", "emoji"]

    def name(self, obj):
        return obj.name
    
    def emoji(self, obj):
        return "%s" % obj.emoji
    
class ArticleScraperModelAdmin(admin.ModelAdmin):
    list_display=["titre", "time"]

    def titre(self, obj):
        return obj.titre
    
    def time(self, obj):
        return obj.time

admin.site.register(StreamModel)
admin.site.register(ArticleScraperModel, ArticleScraperModelAdmin)
admin.site.register(CategoryArticle, CatgoryArticleAdmin)