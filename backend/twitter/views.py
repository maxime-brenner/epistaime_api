from django.shortcuts import render
import requests
from io import BytesIO
from rest_framework.response import Response
import environ
import tweepy
from rest_framework.views import APIView
from api.models import Post
import json
import os
from django.conf import settings

# Create your views here.
def auth_to_twitter(account):
        env = environ.Env()
        environ.Env.read_env(str(settings.BASE_DIR)+'\.env.'+account)

        twitter_auth={
            "API_KEY": env("API_KEY"),
            "API_KEY_SECRET": env("API_KEY_SECRET"),
            "BEARER_TOKEN": env("BEARER_TOKEN"),
            "ACCESS_TOKEN": env("ACCESS_TOKEN"),
            "ACCESS_TOKEN_SECRET": env("ACCESS_TOKEN_SECRET"),
        }

        auth=tweepy.OAuthHandler(
            twitter_auth["API_KEY"],
            twitter_auth["API_KEY_SECRET"]
        )
        
        auth.set_access_token(
            twitter_auth["ACCESS_TOKEN"],
            twitter_auth["ACCESS_TOKEN_SECRET"]
        )

        api=tweepy.API(auth)
        
        return api
    
def client_to_twitter(account):
    env = environ.Env()
    environ.Env.read_env(str(settings.BASE_DIR)+'\.env.'+account)

    twitter_auth={
        "API_KEY": env("API_KEY"),
        "API_KEY_SECRET": env("API_KEY_SECRET"),
        "BEARER_TOKEN": env("BEARER_TOKEN"),
        "ACCESS_TOKEN": env("ACCESS_TOKEN"),
        "ACCESS_TOKEN_SECRET": env("ACCESS_TOKEN_SECRET"),
        "CLIENT_ID": env("CLIENT_ID"),
        "CLIENT_SECRET": env("CLIENT_SECRET"),
    }

    auth=tweepy.OAuthHandler(
        twitter_auth["API_KEY"],
        twitter_auth["API_KEY_SECRET"]
    )
    
    auth.set_access_token(
        twitter_auth["ACCESS_TOKEN"],
        twitter_auth["ACCESS_TOKEN_SECRET"]
    )

    client=tweepy.Client(consumer_key=twitter_auth["API_KEY"],
                    consumer_secret=twitter_auth["API_KEY_SECRET"],
                    access_token=twitter_auth["ACCESS_TOKEN"],
                    access_token_secret=twitter_auth["ACCESS_TOKEN_SECRET"])
    
    return client


class TwitterManager(APIView):

    def upload_image(self, url, account):
        api=self.auth_to_twitter(account)
        img=requests.request("GET", url).content

        with open (str(settings.MEDIA_ROOT)+'/test', "wb") as handler:
            handler.write(img)

        media_id=api.simple_upload(str(settings.MEDIA_ROOT)+'/test').media_id_string
        
        """ os.remove('test') """
        print(settings.MEDIA_ROOT)
        return media_id

    def get(self, request, *args, **kwargs):
        api=auth_to_twitter()
        user=api.get_user(screen_name='epistaime_off')
        print(user)
        #to_validate=json.dumps(user._json)
        #datas = TwitterSerializer(to_validate, many=True)

        return Response({'data': user._json})

    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            request.data["id"]
            toPost=request.data["id"]
            tweet_account=request.data["account"]
            print(tweet_account)
        except KeyError:
            toPost=kwargs["data"]["id"]
            tweet_account=kwargs["data"]["account"]
            print(tweet_account)
        
        client=client_to_twitter(tweet_account)
        print(tweet_account)
        
        post=Post.objects.get(id=toPost)
        try:
            post.content_raw != None
            content=post.content_raw
            """ data=json.loads(post.content)
            content=''
            for part in data['blocks']:
                content = content + ' \n' + part['text'] """
        except:
            content=post.article_url

        

        if post.media_link!=None:
            media_id=self.upload_image(post.media_link, tweet_account)
            status=client.create_tweet(
            media_ids=[media_id],
            text=content,
            )
            post.tweet_id=status[0]["id"]
            post.isPosted=True
            post.save()
            return Response({'data':'Tweet publié', 'tweet':status[0]["id"]})
        else:
            status=client.create_tweet(
            text=content,
            )
            post.tweet_id=status[0]["id"]
            post.isPosted=True
            post.save()
            return Response({'data':'Tweet publié', 'tweet':status[0]["id"]})
        
class FetchTrends(APIView):

    def get(self, request, *args, **kwargs):
        api = auth_to_twitter("EPM")
        trends = api.available_trends()

        return Response({'trends':trends})
    



    
