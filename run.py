# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from modular import database, core
from flask import Flask
import flask_cors
from view.page import PAGE_APP
from view.api import API_APP

app = Flask(__name__)
flask_cors.CORS(app, resources=r'/*')
app.register_blueprint(PAGE_APP)
app.register_blueprint(API_APP)

@app.errorhandler(404)
def errorhandler_404(error):
    return core.generate_response_json_result('未找到文件', 404)

@app.errorhandler(500)
def errorhandler_500(error):
    return core.generate_response_json_result('未知错误', 500)

def initialization():
    db = database.DataBase()
    if not db.existence_table('core'):
        db.create_core_table()
    if not db.existence_table('url'):
        db.create_url_table()

initialization()
'''
if __name__ == '__main__':
    initialization()
    app.run(host='0.0.0.0', port='5000', debug=True, processes=True)
'''