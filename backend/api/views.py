from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Post
from api.serializer import PostSerializer
from twitter.views import TwitterManager
import pandas as pd

# Create your views here.
class PostView(ModelViewSet):
    serializer_class=PostSerializer

    def get_queryset(self):
        return Post.objects.all()
    
class ExportToCSV(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        df = pd.DataFrame(serializer.data)
        df.to_csv(f"export/posts/test.csv", encoding="UTF-8", index=False)
        return Response({'status': 200})


class TweetRandomPost(APIView):
    def post(self, request, *args, **kwargs):
        post=Post.objects.filter(isPosted=False).order_by('?').first()
        view = TwitterManager.as_view()
        print(request._request)

        return view(request._request, data={'id':post.id, 'account':post.account}) 
