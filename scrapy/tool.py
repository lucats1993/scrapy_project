# -*- coding: utf-8 -*-

import re
import urllib
import json
from urlparse import urlparse

def format_array(li):
    return (li and li[0].encode('utf-8').strip()) or ''

def format_str(li):
    return (li and li.encode('utf-8').replace('\n','').strip()) or ''

def get_coName(name):
    if not name:
        return
    res = re.sub(r'\s{2,}',' ',name[0])
    return name[0] if not res else res.strip()

def get_realType(key):
    with open('./a.json', 'r') as f:
        maps = json.load(f)
    return  ["",""] if not maps.get(key) else maps.get(key)



def extractDomainFromURL(url):
    """Get domain name from url"""
    if not url:
        return ''
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain
# print extractDomainFromURL('http://www.kanguowai.com/zhongwen/list_2.html')
# proto, rest = urllib.splittype('http://www.kanguowai.com/zhongwen/list_2.html')
# res, rest = urllib.splithost(rest)
# print "unkonw" if not res else res