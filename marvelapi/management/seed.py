import requests
from django.core.management.base import BaseCommand
from ..models import Marvel
import datetime
import hashlib
from ..keys import PUBLIC_KEY, PRIVATE_KEY



timestamp = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')


def hash_params():
    hash_md5 = hashlib.md5()
    hash_md5.update(f'{timestamp}{PRIVATE_KEY}{PUBLIC_KEY}'.encode('utf-8'))
    hashed_params = hash_md5.hexdigest()
    return hashed_params

params = {'ts': timestamp, 'apikey': PUBLIC_KEY, 'hash': hash_params()}


def get_characters():
    url = 'https://gateway.marvel.com:443/v1/public/characters?name='
    r = requests.get(url)
    character = r.json()
    return character


def seed_characters():
    for i in get_characters():
        character = Marvel.objects.create(char_name=i['name'])
        character.save()
    

class Command(BaseCommand):
    help = 'Seeds the database with characters'

    def handle(self, *args, **options):
        seed_characters()
        self.stdout.write(self.style.SUCCESS('Characters have been seeded'))

    
    