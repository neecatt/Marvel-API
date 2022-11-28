from django.shortcuts import render
from marvelapi.models import Marvel
import requests
import hashlib
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dotenv import load_dotenv
import os

#environement variables
load_dotenv()
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
PUBLIC_KEY = os.getenv('PUBLIC_KEY')


# Creating hash for API
timestamp = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')
def hash_params():
    hash_md5 = hashlib.md5()
    hash_md5.update(f'{timestamp}{PRIVATE_KEY}{PUBLIC_KEY}'.encode('utf-8'))
    hashed_params = hash_md5.hexdigest()
    return hashed_params

params = {'ts': timestamp, 'apikey': PUBLIC_KEY, 'hash': hash_params()}

# Getting data from Marvel API
def get_characters():
    url = f'https://gateway.marvel.com:443/v1/public/characters'
    response = requests.get(url, params=params).json()
    character = response['data']['results']
    return character


# Seed data from API to sqlite database
@api_view(['POST'])
def seed_characters(request):
    for i in get_characters():
        character = Marvel.objects.create(character=i['name'])
        character.save()
    return Response({'message': 'Characters seeded successfully'})


# Get data from sqlite database
@api_view(['GET'])
def get_from_database(request):
    for i in Marvel.objects.all():
        return Response({'name': i.character}) 
    characters = Marvel.objects.all()
    return characters
    