# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Blueprint, redirect, request
from modular import core, auxiliary, database

API_APP = Blueprint('API_APP', __name__)

@API_APP.route('/api/generate', methods=['GET', 'POST'])
def generate():
    parameter = core.get_request_parameter(request)
    domain = parameter.get('domain')
    long_url = parameter.get('long_url')
    signature = parameter.get('signature')
    valid_time = parameter.get('valid_time')

    if auxiliary.empty_many(domain, long_url) or (auxiliary.empty(valid_time) and valid_time.isdigit()):
        return core.generate_response_json_result('参数错误', 100)
    
    if not auxiliary.is_url(long_url):
        return core.generate_response_json_result('长网址需要完整', 200)

    if auxiliary.empty(valid_time):
        valid_time = 0
    valid_time = int(valid_time)
    if valid_time < 0 or valid_time > 365:
        return core.generate_response_json_result('仅能填0-365的数,0代表永久')
    
    db = database.DataBase()

    if domain not in db.query_domain():
        return core.generate_response_json_result('域名不存在')
    
    if auxiliary.empty(signature):
        query = db.query_by_long_url(domain, long_url)
        if query:
            return core.generate_response_json_result(f'https://{domain}/{query.get("signature")}')
        
        id_d = db.insert('system', domain, long_url, valid_time)
        signature = auxiliary.base62_encode(id_d)
        if db.query_by_signature(domain, signature):
            signature += 'a'
            
        db.update(id_d, signature)
        return core.generate_response_json_result(f'https://{domain}/{signature}')
    else:
        if signature.lower() == 'api':
            return core.generate_response_json_result('特征码不能为api')
        elif signature.lower() == 'index':
            return core.generate_response_json_result('特征码不能为index')
        elif signature.lower() == 'query':
            return core.generate_response_json_result('特征码不能为query')
        elif signature.lower() == 'doc':
            return core.generate_response_json_result('特征码不能为doc')
        elif not signature.isdigit() and not signature.isalpha() and not signature.isalnum():
            return core.generate_response_json_result('特征码仅能填数字和字母')
        elif len(signature) < 1 or len(signature) > 5:
            return core.generate_response_json_result('特征码长度只能为1-5')

        if db.query_by_signature(domain, signature):
            return core.generate_response_json_result('特征码已存在')
        
        id_d = db.insert('custom', domain, long_url, valid_time)
        db.update(id_d, signature)
        return core.generate_response_json_result(f'https://{domain}/{signature}')

@API_APP.route('/api/get', methods=['GET', 'POST'])
def get():
    parameter = core.get_request_parameter(request)
    type_d = parameter.get('type')

    if type_d != 'domain' and type_d != 'information':
        return core.generate_response_json_result('参数错误', 100)

    if type_d == 'domain':
        db = database.DataBase()
        return core.generate_response_json_result(db.query_domain())

    domain = parameter.get('domain')
    signature = parameter.get('signature')

    if auxiliary.empty_many(domain, signature):
        return core.generate_response_json_result('参数错误', 100)
    
    db = database.DataBase()

    if domain not in db.query_domain():
        return core.generate_response_json_result('域名不存在')

    query = db.query_by_signature(domain, signature)
    if not query:
        return core.generate_response_json_result('特征码不存在')
    
    return core.generate_response_json_result(query)

@API_APP.route('/<signature>', methods=['GET', 'POST'])
@API_APP.route('/<signature>/', methods=['GET', 'POST'])
def short_url_redirect(signature):
    db = database.DataBase()

    if request.host not in db.query_domain():
        return redirect(request.host_url)
    
    query = db.query_by_signature(request.host, signature)
    if query:
        db.add_count(request.host, signature)
        return redirect(query.get('long_url'))
    return redirect(request.host_url)