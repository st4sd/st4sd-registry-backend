#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Author: Alessandro Pomponio
#
import requests
from flask import jsonify, request
from flask_restx import Namespace, Resource

from utils.config import settings
from utils.st4sd_api_helper import get_authorization_headers

api = Namespace('experiments', description='Experiment-related operations')

@api.route('/')
class PVEPList(Resource):
    @api.doc('get_pveps')
    def get(self):
        """Get all PVEPS"""
        authorization_headers = get_authorization_headers()
        response = requests.get(f"{settings.runtime_service_endpoint}experiments/", headers=authorization_headers)
        assert response.status_code == 200, f"Response code was {response.status_code}"
        return jsonify(response.json())


@api.route("/<pvep>")
class PVEP(Resource):
    @api.param('pvep', 'The pvep identifier')
    @api.doc('get_pvep')
    def get(self, pvep: str):
        """Get a PVEP"""
        authorization_headers = get_authorization_headers()
        if request.query_string is None:
            response = requests.get(f"{settings.runtime_service_endpoint}experiments/{pvep}", headers=authorization_headers)
        else:
            query_string = bytes.decode(request.query_string)
            response = requests.get(f"{settings.runtime_service_endpoint}experiments/{pvep}?{query_string}", headers=authorization_headers)
        assert response.status_code == 200, f"Response code was {response.status_code}"
        return jsonify(response.json())


@api.route("/<pvep>/history")
class PVEPHistory(Resource):
    @api.param('pvep', 'The pvep identifier')
    @api.doc('get_pvep_history')
    def get(self, pvep: str):
        """Get the history of a PVEP"""
        authorization_headers = get_authorization_headers()
        response = requests.get(f"{settings.runtime_service_endpoint}experiments/{pvep}/history", headers=authorization_headers)
        assert response.status_code == 200, f"Response code was {response.status_code}"
        return jsonify(response.json())
