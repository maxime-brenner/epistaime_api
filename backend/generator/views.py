from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import openai
import environ
# Create your views here.

def generate_text_from_url(url):
        env=environ.Env()
        environ.Env.read_env()

        openai.api_key=env('OPENAI_KEY')

        prompt = f"Ecris un résumé de 150 caractères de cet article: {url}"

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

        return completion['choices'][0]['message']['content']

class Generator(APIView):

    def post(self, request, *args, **kwargs):
        env=environ.Env()
        environ.Env.read_env()

        openai.api_key=env('OPENAI_KEY')

        url = request.data["article_url"]

        prompt = f"Ecris un résumé en français de 150 caractères de cet article, en evitant les formulations du type \"cet article parle de..\": {url}"

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

        return Response({"message":completion['choices'][0]['message']['content']})