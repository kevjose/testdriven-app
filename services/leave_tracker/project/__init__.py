import os
import json
import datetime
from bson.objectid import ObjectId

from flask import Flask  # new
from flask_cors import CORS
from flask_pymongo import PyMongo

cors = CORS()
mongo = PyMongo()


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


# new
def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    cors.init_app(app)
    mongo.init_app(app)
    app.json_encoder = JSONEncoder

    # register blueprints
    from project.api.leave_tracker import leave_tracker_blueprint
    app.register_blueprint(leave_tracker_blueprint)
    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app}

    return app
