from flask import Blueprint, jsonify, request

from project.api.utils import authenticate
from project import mongo


leave_tracker_blueprint = Blueprint('leave_tracker', __name__)


@leave_tracker_blueprint.route('/leave_tracker/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    }), 200

@leave_tracker_blueprint.route('/leave_tracker/employee/autofill/<search_string>', methods=['GET'])
@authenticate
def employee_autofill(resp, search_string):
    response_object = {
        'status': 'fail',
        'message': 'No Results found'
    }
    print(request.args)
    try:
        data = mongo.db.employees.find({'name': {'$regex': '^' + search_string, '$options': 'i'}})
        if not data:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'employees':list(data) ,
                    'current_user':resp['data']
                },
                'message': 'Matches Found'
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


