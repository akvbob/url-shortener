import requests
import hashlib
import random
import re

from .models import ShortLink

ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
SHORT_URL_LENGTH = 8

BASE62_CONVERSION_ALGORITHM = 'Base62'
RANDOM_URL_ALGORITHM = 'Random'
MD5_HASH = 'MD5'

AlGORITHMS = [
    (RANDOM_URL_ALGORITHM, 'Random URL '),
    (BASE62_CONVERSION_ALGORITHM, 'Base62 conv'),
    (MD5_HASH, 'MD5 hash')
]

USED_ALGORITHM = MD5_HASH

def given_url_exists(user_url):
    try:
        response = requests.get(user_url)
    except:
        return False

    if response.status_code != 200:
        return False
    return True


def format_user_url(user_url):
    regex = '^https?\:\/\/'
    has_http = re.search(regex, user_url)
    if not has_http:
        return '{}{}'.format('http://', user_url)
    return user_url


def print_timelapse_table(algorithm, end, start):
    time_lapsed = calc_time_lapse(end, start)
    short_url_count = ShortLink.objects.count()
    print('|-----------------------------------------------------|')
    print('|    ALGORITHM     | DB ROWS |    TIME                |')
    print('|-----------------------------------------------------|')
    print('|    {algorithm}    |   {rows}    | {time} '.format(algorithm=algorithm.algorithm_name, rows=short_url_count, time=time_lapsed))


def calc_time_lapse(end, start):
    return end - start
    

def get_algorithm():
    if USED_ALGORITHM == RANDOM_URL_ALGORITHM:
        return RandomUrlGenerator()
    
    if USED_ALGORITHM == BASE62_CONVERSION_ALGORITHM:
        return Base62Conversion()

    if USED_ALGORITHM == MD5_HASH:
        return MD5Hash()



class RandomUrlGenerator(object):
    algorithm_name = AlGORITHMS[0][1]


    def generate_random_url(self):
        return ''.join(random.choices(ALPHABET, k=SHORT_URL_LENGTH))

    
    def get_short_url(self, long_url):
        short_url_key = ''

        while True:
            short_url_key = self.generate_random_url()
            if not ShortLink.short_url_exists(ShortLink, short_url_key):
                return short_url_key



class Base62Conversion(object):
    algorithm_name = AlGORITHMS[1][1]
    

    def update_short_url_length(self, short_url):
        
        while len(short_url) < SHORT_URL_LENGTH:
            short_url = '0{}'.format(short_url)
        return short_url


    def get_short_url(self, long_url):
        short_url = ''
        id = ShortLink.objects.count() + 1

        # for each digit find the base 62
        while(id > 0):
            short_url += ALPHABET[id % 62]
            id //= 62
    
        # reversing the shortURL
        url = short_url[len(short_url): : -1]
        return self.update_short_url_length(url)
 



class MD5Hash(object):
    algorithm_name = AlGORITHMS[2][1]


    def get_url_hash(self, long_url):
        id = ShortLink.objects.count() + 1
        string_to_hash = '{}{}'.format(str(id), long_url)
        result = hashlib.md5(string_to_hash.encode())
        
        # get encoded data in hexadecimal format
        return result.hexdigest()


    def get_short_url(self, long_url):
        short_url_key = ''
        hash = self.get_url_hash(long_url)

        hash_length = len(hash)
        counter = 0

        while counter < hash_length - SHORT_URL_LENGTH:
            short_url_key = hash[counter: counter + SHORT_URL_LENGTH]
            if not ShortLink.short_url_exists(ShortLink, short_url_key):
                return short_url_key
            counter += 1