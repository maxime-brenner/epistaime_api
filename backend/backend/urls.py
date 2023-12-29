"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import PostView, TweetRandomPost, ExportToCSV
from scraper.views import ArticleStreaming, RetrieveArticleStream, UpdateItemFromStream, CreatePostFromStream, RetrieveArticleView, CreatePostAndGenerateTextFromStream, ScrapFetchTrends, GoogleNewsSearch
from twitter.views import TwitterManager, FetchTrends
from generator.views import Generator
from shortener.views import redirect_url
from rest_framework import routers

#Post
post_path = routers.SimpleRouter()
post_path.register(r'post', PostView, basename="post")
post_path.register(r'streamarticle', RetrieveArticleView, basename="article_stream")

#Twitter
#twitter_path= routers.SimpleRouter()
#twitter_path.register(r'twitter', TwitterManager, basename="twitter")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(post_path.urls)),
    path('api/export/posts/', ExportToCSV.as_view()),
    path('api/random/', TweetRandomPost.as_view()),
    path('api/twitter/', TwitterManager.as_view()),
    path('api/twitter/trends/', FetchTrends.as_view()),
    path('api/scraper/bfmtv/', ArticleStreaming.as_view()),
    path('api/scraper/google/search/news/', GoogleNewsSearch.as_view()),
    path('api/scraper/retrieve/bfmtv/', RetrieveArticleStream.as_view()),
    path('api/scraper/update/bfmtv/', UpdateItemFromStream.as_view()),
    path('api/scraper/createtest/bfmtv/', CreatePostFromStream.as_view()),
    path('api/scraper/createandgenerate/bfmtv/', CreatePostAndGenerateTextFromStream.as_view()),
    path('api/scraper/trends/', ScrapFetchTrends.as_view()),
    path('api/generator/', Generator.as_view()),
    path('api/short/<str:key>/', redirect_url)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
