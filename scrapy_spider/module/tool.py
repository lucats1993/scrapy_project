# -*- coding: utf-8 -*-

import re
import json
from urlparse import urlparse

with open('category.json', 'r') as f:
    maps = json.load(f)

def check_list(li):
    return (li and li[0].encode('utf-8').strip()) or ''

def check_str(li):
    return (li and li.encode('utf-8').replace('\n','').strip()) or ''

def get_coName(name):
    if not name:
        return ''
    res = re.sub(r'\s{2,}',' ',name[0])
    return name[0] if not res else res.strip()

def get_realType(key):
    return ["",""] if not maps.get(key) else maps.get(key)

def extractDomainFromURL(url):
    """Get domain name from url"""
    if not url:
        return ''
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain
