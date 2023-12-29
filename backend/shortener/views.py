from django.shortcuts import render, redirect
from shortener.models import Shortener

# Create your views here.
def redirect_url(request, key):
    obj = Shortener.objects.get(key=key)
    url = obj.url
    obj.clic_count += 1

    obj.save()
    response = redirect(url)
    return response