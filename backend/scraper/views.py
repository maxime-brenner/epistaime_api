from django.shortcuts import render
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from scraper.scraper_logic import bfmtv, trends24, links_from_google_search
from scraper.models import StreamModel
import json
from api.models import Post
from api.views import PostView
from generator.views import Generator, generate_text_from_url
from twitter.views import TwitterManager
from scraper.models import ArticleScraperModel
from scraper.serializer import ArticleScraperModelSerializer

# Create your views here.
class ArticleStreaming(APIView):
    def get(self, request, *args, **kwargs):
        datas=bfmtv()

        return Response(datas)
    
class RetrieveArticleStream(APIView):
    def get (self, request, *args, **kwargs):
        return Response(json.loads(StreamModel.objects.get(brand_name="bfmtv").stream))
    
    def delete(self, request, *args, **kwargs):
        ArticleScraperModel.objects.all().delete()
        """ stream.stream=json.dumps({'articles':[]})
        stream.save() """

        return Response("Stream nettoyé")
    
class UpdateItemFromStream(APIView):
    def post(self, request, *args, **kwargs):
        id = request.data["id"]
        stream = StreamModel.objects.get(brand_name='bfmtv')
        stream_list = json.loads(stream.stream)
        print(stream_list)

        retrieve_element_index=next((index for (index, item) in enumerate(stream_list["articles"]) if item["id"] == id), None)
        print(retrieve_element_index)

        if stream_list["articles"][retrieve_element_index]["posted"] == False:
            stream_list["articles"][retrieve_element_index]["posted"] = True
        else:
            stream_list["articles"][retrieve_element_index]["posted"] = False

        stream.stream=json.dumps(stream_list)
        stream.save()
        
        return Response("Objet mis à jour")
    
class CreatePostFromStream(APIView):
    def post(self, request, *args, **kwargs):
        new_post = Post.objects.create(**request.data["post"])

        stream_article = ArticleScraperModel.objects.get(id=request.data["stream"]["id"])
        stream_article.post = new_post
        stream_article.save()

        return Response("Nouvel article posté")

class CreatePostAndGenerateTextFromStream(APIView):
    def post(self, request, *args, **kwargs):
        print(type(request))
        new_post = Post.objects.create(**request.data["post"]) 
        generated_text=generate_text_from_url(request.data["post"]["article_url"])
        
        new_post.content_raw='\U0001F4F0'+'generated_text'+'\n'+request.data["post"]["article_url"]
        new_post.generated_text=generated_text
        new_post.save()

        stream_article = ArticleScraperModel.objects.get(id=request.data["stream"]["id"])
        stream_article.post=new_post
        stream_article.save() 


        new_request = HttpRequest()
        new_request.META=request.META
        new_request.method = 'POST'
        new_request.POST.update={"id":77}      
        converted_request=Request(new_request, parsers=[JSONParser()])
        converted_request.POST.update["id"]=77
        converted_request.data.update["id"]=77

        print(type(converted_request), converted_request.data)
        TwitterManager().post(request=converted_request, content_type="application/json")

        return Response("Nouvel article et texte générer posté")
    
class RetrieveArticleView(ModelViewSet):
    queryset=ArticleScraperModel.objects.all()
    serializer_class = ArticleScraperModelSerializer

    def get_queryset(self):
        print(self.request.GET.dict())
        return self.queryset.filter(**self.request.GET.dict())
    
    @action(methods=['DELETE'], detail=False,)
    def delete(self, request:Request):
        self.queryset.delete()

        return Response("Articles supprimés")

class ScrapFetchTrends(APIView):

    def get(self, request, *args, **kwargs):
        trends = trends24()

        return Response({"trends":trends})
    
class GoogleNewsSearch(APIView):
    def post(self, request):

        search=request.data["search"]

        links = links_from_google_search(search=search)

        return Response({"links":links})

    


