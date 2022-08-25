# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import json
import re

def text_to_json(data):
    return json.loads(data)

def json_to_text(data, ascii=True):
    return json.dumps(data, ensure_ascii=ascii)

def empty(variable):
    if variable == None:
        return True
    elif type(variable) == int or type(variable) == float:
        if variable == 0:
            return True
        return False
    elif len(variable) == 0:
        return True
    return False

def empty_many(*variable):
    for variable_count in variable:
        if empty(variable_count):
            return True
    return False

def is_url(text):
    re_d = re.compile(r'^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+')
    return bool(re_d.search(text))

def base62_encode(num):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)