from flask import Flask, render_template
from flask_login import login_required, current_user
from flask_restful import Api
import request_blueprint
import admin_blueprint
import api_blueprint
import auth_blueprint
from api_resources import HistoryResource, TenderResource, HistoryListResource
from data import db_session
from login import login_manager
import asyncio


HOST = '127.0.0.1'
PORT = 8000

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
login_manager.init_app(app)
app.register_blueprint(request_blueprint.blueprint)
app.register_blueprint(admin_blueprint.blueprint)
app.register_blueprint(api_blueprint.blueprint)
app.register_blueprint(auth_blueprint.blueprint)
app.config["SECRET_KEY"] = "qazwsxedcrfv"

api = Api(app)
api.add_resource(HistoryResource, '/api/queries/<int:history_id>')
api.add_resource(TenderResource, '/api/tenders/<int:tender_id>')
api.add_resource(HistoryListResource,'/api/queries')
api.app.config['RESTFUL_JSON'] = {'ensure_ascii': False}

@app.route('/')
@login_required
def index():
    return render_template("index.html", user=current_user)


if __name__ == '__main__':
    db_session.global_init()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app.run(HOST, port=PORT, debug=False)
