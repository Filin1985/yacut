import re
from urllib.parse import urlparse


from .constants import SHORT_ID_REGEXP, MAX_ORIGINAL_SIZE, MAX_SHORT_ID_SIZE


def check_validity_shirt_id(short_link):
    if len(short_link) > MAX_SHORT_ID_SIZE or not bool(re.match(SHORT_ID_REGEXP, short_link)):
        return False
    return True

def validate_url(original):
    parsed_url = urlparse(original)
    return bool(parsed_url.scheme and parsed_url.netloc)

def check_original_url(original):
    return len(original) < MAX_ORIGINAL_SIZE and validate_url(original)