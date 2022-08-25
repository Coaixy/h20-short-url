# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import make_response
from modular import auxiliary

def get_request_parameter(request):
    data = {}
    if request.method == 'GET':
        data = request.args
    elif request.method == 'POST':
        data = request.form
        if not data:
            data = request.get_json()
    return dict(data)

def generate_response_json_result(information, state=200):
    data = {
        'state': state,
        'information': information
    }
    data = auxiliary.json_to_text(data, False)
    response = make_response(data)
    response.mimetype = 'application/json; charset=utf-8'
    return response