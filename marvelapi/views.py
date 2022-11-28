from django.shortcuts import render
from marvelapi.models import Marvel
import requests
from .keys import PUBLIC_KEY, PRIVATE_KEY
import hashlib
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

timestamp = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')


def hash_params():
    hash_md5 = hashlib.md5()
    hash_md5.update(f'{timestamp}{PRIVATE_KEY}{PUBLIC_KEY}'.encode('utf-8'))
    hashed_params = hash_md5.hexdigest()
    return hashed_params

params = {'ts': timestamp, 'apikey': PUBLIC_KEY, 'hash': hash_params()}

def get_characters():
    url = f'https://gateway.marvel.com:443/v1/public/characters'
    response = requests.get(url, params=params).json()
    character = response['data']['results']
    return character

@api_view(['POST'])
def seed_characters(request):
    for i in get_characters():
        character = Marvel.objects.create(character=i['name'])
        character.save()
    return Response({'message': 'Characters seeded successfully'})

@api_view(['GET'])
def get_from_database(request):
    for i in Marvel.objects.all():
        return Response({'name': i.character}) 
    #list all characters to response

    characters = Marvel.objects.all()
    return characters
    
@api_view(['GET'])
def get_from_marvel(request):
    for i in get_characters():
        return Response({'name': i['name']}) 
    #list all characters to response

    characters = get_characters()
    return characters

# def get_characters(request):
#       url = f'https://gateway.marvel.com:443/v1/public/characters?name={char_name}'
    
    # all_characters = {}
    # if 'char_name' in request.GET:
    #     char_name = request.GET['char_name']
      
    #     response = requests.get(url, params=params)
    #     data = response.json()
    #     characters = data['data']['results']
        
    #     for character in characters:
    #         char_data = Marvel(
    #             char_name = character['name'],
    #         )
    #         char_data.save()
    #         all_characters = Marvel.objects.all().order_by('-id')
    
    # return render(request, 'marvel/characters.html', {'all_characters': all_characters})        
            