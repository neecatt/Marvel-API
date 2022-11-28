import datetime
# from keys import PUBLIC_KEY,PRIVATE_KEY
import requests
import hashlib
from pprint import pprint as pp
import environ

env = environ.Env()
env.read_env()

PRIVATE_KEY = env('PRIVATE_KEY')
PUBLIC_KEY = env('PUBLIC_KEY')





timestamp = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')


def hash_params():
    hash_md5 = hashlib.md5()
    hash_md5.update(f'{timestamp}{PRIVATE_KEY}{PUBLIC_KEY}'.encode('utf-8'))
    hashed_params = hash_md5.hexdigest()
    return hashed_params

params = {'ts': timestamp, 'apikey': PUBLIC_KEY, 'hash': hash_params()}


response = requests.get('https://gateway.marvel.com/v1/public/characters?nameStartsWith=' + 'spi' , params=params)
data = response.json()
pp(data)

