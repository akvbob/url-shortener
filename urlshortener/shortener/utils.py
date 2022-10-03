import requests
import random
import re


ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def givenURLExists(user_url):
    try:
        response = requests.get(user_url)
    except:
        return False

    if response.status_code != 200:
        return False
    return True


def formatUserURL(user_url):
    regex = '^https?\:\/\/'
    has_http = re.search(regex, user_url)
    if not has_http:
        return '{}{}'.format('http://', user_url)
    return user_url


# generates a string of length 8
def generateUniqueUrlKey():
    return ''.join(random.choices(ALPHABET, k=8))
