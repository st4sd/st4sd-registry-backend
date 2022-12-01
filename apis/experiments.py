#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Author: Alessandro Pomponio
#
import requests
from flask import jsonify, request
from flask_restx import Namespace, Resource

from utils.st4sd_api_helper import runtime_service_endpoint

api = Namespace('experiments', description='Experiment-related operations')


@api.route('/')
class PVEPList(Resource):
    @api.doc('get_pveps')
    def get(self):
        """Get all PVEPS"""
        response = requests.get(f"{runtime_service_endpoint}/")
        assert response.status_code == 200, f"Response code was {response.status_code}"
        return jsonify(response.json())


@api.route("/<pvep>")
class PVEP(Resource):
    @api.param('pvep', 'The pvep identifier')
    @api.doc('get_pvep')
    def get(self, pvep: str):
        """Get a PVEP"""
        if request.query_string is None:
            response = requests.get(f"{runtime_service_endpoint}/{pvep}")
        else:
            query_string = bytes.decode(request.query_string)
            response = requests.get(f"{runtime_service_endpoint}/{pvep}?{query_string}")
        assert response.status_code == 200, f"Response code was {response.status_code}"
        return jsonify(response.json())


@api.route("/<pvep>/history")
class PVEPHistory(Resource):
    @api.param('pvep', 'The pvep identifier')
    @api.doc('get_pvep_history')
    def get(self, pvep: str):
        """Get the history of a PVEP"""
        response = requests.get(f"{runtime_service_endpoint}/{pvep}/history")
        assert response.status_code == 200, f"Response code was {response.status_code}"
        return jsonify(response.json())
