from django.shortcuts import render
from marvelapi.models import Marvel
import requests

char_name = 'spider'
characters = Marvel.objects.filter(character__icontains=char_name)
print(characters)
