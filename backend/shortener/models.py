from django.db import models
from django.db.models import CharField, URLField, IntegerField
from shortener.utils import key_generator

# Create your models here.
class Shortener(models.Model):
    key = CharField(primary_key=True, default=key_generator, editable=False)
    url = URLField(blank=False, unique=False)
    clic_count = IntegerField(default=0, blank=False, unique=False)