#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Author: Alessandro Pomponio
#
import json

import experiment.service.errors
import requests
from flask import jsonify, request
from flask_restx import Namespace, Resource

from utils.config import settings
from utils.decorators import disable_on_global_instances
from utils.st4sd_api_helper import get_api
from utils.st4sd_api_helper import get_authorization_headers

api = Namespace('experiments', description='Experiment-related operations')

# TODO: use StrEnum when Python 3.11 is supported
supported_experiment_search_selectors = [
    "name", "description", "maintainer", "property_name"]


@api.route('/')
class PVEPList(Resource):
    @api.doc('get_pveps')
    def get(self):
        """Get all PVEPS"""
        authorization_headers = get_authorization_headers()
        response = requests.get(
            f"{settings.runtime_service_endpoint}experiments/", headers=authorization_headers)

        if response.status_code != 200:
            api.logger.warning(msg=f"{request} returned error code {response.status_code}")
            return {}, response.status_code

        search_query = request.args.get("searchQuery", "").lower()
        search_selector = request.args.get("searchSelector", "").lower()
        # No query
        if search_selector == "" or search_query == "":
            return jsonify(response.json())

        # Unsupported search selector
        if search_selector not in supported_experiment_search_selectors:
            return jsonify({})

        # Handle search
        experiments_matching_query = {"entries": []}
        for exp in response.json()["entries"]:
            # Search by property
            if search_selector == "property_name":
                for property in exp["metadata"]["registry"]["interface"].get("propertiesSpec", {}):
                    if search_query in property.get("name", "").lower():
                        experiments_matching_query['entries'].append(exp)
                        break
            # Search by metadata
            elif search_selector in ["description", "maintainer", "name"]:
                if search_query in exp["metadata"]["package"].get(search_selector, "").lower():
                    experiments_matching_query['entries'].append(exp)

        return jsonify(experiments_matching_query)


@api.route("/<pvep>", methods=['GET', 'POST'])
class PVEP(Resource):
    @api.param('pvep', 'The pvep identifier')
    @api.doc('get_pvep')
    def get(self, pvep: str):
        """Get a PVEP"""
        authorization_headers = get_authorization_headers()
        if request.query_string is None:
            response = requests.get(
                f"{settings.runtime_service_endpoint}experiments/{pvep}", headers=authorization_headers)
        else:
            query_string = bytes.decode(request.query_string)
            response = requests.get(
                f"{settings.runtime_service_endpoint}experiments/{pvep}?{query_string}", headers=authorization_headers)

        if response.status_code != 200:
            api.logger.warning(msg=f"{request} returned error code {response.status_code}")
            return {}, response.status_code

        return jsonify(response.json())

    @api.param('pvep', 'The pvep identifier')
    @api.doc('edit_parameterisation_options')
    @disable_on_global_instances
    def post(self, pvep: str):
        try:
            st4sd_api = get_api()
            parameterisation_options = request.json
            response = st4sd_api.api_experiment_push(parameterisation_options)
        except experiment.service.errors.InvalidHTTPRequest as e:
            api.logger.warning(msg=f"{request} returned error code {e.response.status_code}")
            return e.message, e.response.status_code

        return response


@api.route("/<pvep>/parameterisation")
class PVEPParameterisationOptions(Resource):
    @api.param('pvep', 'The pvep identifier')
    @api.doc('get_pvep_parameterisation_options')
    def get(self, pvep: str):
        """Get a pveps parameterisation options"""
        authorization_headers = get_authorization_headers()
        response = requests.get(
            f"{settings.runtime_service_endpoint}experiments/{pvep}?outputFormat=json&hideMetadataRegistry=n&hideNone=y&hideBeta=n",
            headers=authorization_headers)

        if response.status_code != 200:
            api.logger.warning(msg=f"{request} returned error code {response.status_code}")
            return {}, response.status_code

        return jsonify(response.json())


@api.route("/<pvep>/history")
class PVEPHistory(Resource):
    @api.param('pvep', 'The pvep identifier')
    @api.doc('get_pvep_history')
    def get(self, pvep: str):
        """Get the history of a PVEP"""
        authorization_headers = get_authorization_headers()
        response = requests.get(
            f"{settings.runtime_service_endpoint}experiments/{pvep}/history", headers=authorization_headers)

        if response.status_code != 200:
            api.logger.warning(msg=f"{request} returned error code {response.status_code}")
            return {}, response.status_code

        return jsonify(response.json())


@api.route("/<pvep>/start", methods=['POST'])
class RunPVEP(Resource):
    @api.param('pvep', 'The pvep identifier')
    @api.doc('edit_parameterisation_options')
    @disable_on_global_instances
    def post(self, pvep: str):
        payload = request.json
        authorization_headers = get_authorization_headers()
        response = requests.post(
            f"{settings.runtime_service_endpoint}experiments/{pvep}/start", headers=authorization_headers,
            json=json.loads(payload))

        if response.status_code != 200:
            api.logger.warning(msg=f"{request} returned error code {response.status_code}")
            return response.json(), response.status_code

        return {"run_id": response.json()}
