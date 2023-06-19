#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Authors: Philip Burrows, Laith Al Mofty
#
import requests
from flask import jsonify, request
from flask_restx import Namespace, Resource

from utils.config import settings
from utils.decorators import disable_on_global_instances, disable_with_env_var
from utils.st4sd_api_helper import get_authorization_headers

api = Namespace('canvas', description='Canvas related operations')


@api.route("/<pvep>")
class PVEPDsl(Resource):
    @api.param('pvep', 'The pvep identifier')
    @api.doc("get_dsl_for_pvep")
    @disable_with_env_var("ST4SD_REGISTRY_UI_SETTINGS_DISABLE_CANVAS")
    def get(self, pvep: str):
        """Get dsl for pvep"""
        authorization_headers = get_authorization_headers()
        response = requests.get(f"{settings.runtime_service_endpoint}experiments/{pvep}/dsl",
                                headers=authorization_headers)

        if response.status_code != 200:
            api.logger.warning(msg=f"{request} returned error code {response.status_code}")
            return None, response.status_code

        return jsonify(response.json().get('dsl', None))


@api.route("/<pvep>/relationships")
class PVEPRelationships(Resource):
    @api.param('pvep', 'The pvep identifier')
    @api.doc("get_relationships_for_pvep")
    @disable_on_global_instances
    def get(self, pvep: str):
        """Get relationships for pvep transforms"""

        authorization_headers = get_authorization_headers()
        payload = {"transform": {"outputGraph": {"identifier": f"{pvep}:latest"}}}
        response = requests.post(f"{settings.runtime_service_endpoint}query/relationships/",
                                 headers=authorization_headers, json=payload)

        if response.status_code != 200:
            api.logger.warning(msg=f"{request} returned error code {response.status_code}")
            return {}, response.status_code

        ui_formatted_response = []
        for relationship in response.json():
            ui_formatted_response.append({'label': relationship["description"], 'id': relationship["identifier"]})

        return jsonify(ui_formatted_response)


@api.route("/preview/<relationship_id>/dsl")
class PreviewDSL(Resource):
    @api.param('relationship_id', 'The id for the transform relationship')
    @api.doc("get_preview_dsl_for_transformed_experiment")
    @disable_on_global_instances
    def get(self, relationship_id: str):
        """Get preview dsl for a transformed pvep"""
        authorization_headers = get_authorization_headers()
        response = requests.get(
            f"{settings.runtime_service_endpoint}relationships/{relationship_id}/preview/synthesize/dsl/",
            headers=authorization_headers)

        if response.status_code != 200:
            return response.json(), response.status_code

        return jsonify(response.json().get('dsl', None))


@api.route("/preview/<relationship_id>/inputs")
class PreviewExperiment(Resource):
    @api.param('relationship_id', 'The id for the transform relationship')
    @api.doc("get_preview_for_transformed_experiment")
    @disable_on_global_instances
    def get(self, relationship_id: str):
        """Get preview for a transformed pvep"""
        authorization_headers = get_authorization_headers()
        response = requests.get(
            f"{settings.runtime_service_endpoint}relationships/{relationship_id}/preview/synthesize/dsl/",
            headers=authorization_headers)

        if response.status_code != 200:
            api.logger.warning(msg=f"{request} returned error code {response.status_code}")
            return response.json(), response.status_code

        data = response.json()
        return jsonify({"entry": data.get('experiment', None), "problems": data.get('problems', None)})


@api.route("/relationships/<relationship_id>/synthesize/<new_package_name>", methods=['POST'])
class NewExperiment(Resource):
    @api.doc("post_transformed_experiment_from_edit_canvas")
    @disable_on_global_instances
    def post(self, relationship_id: str, new_package_name: str):
        """Post new experiment from edit canvas"""
        authorization_headers = get_authorization_headers()
        response = requests.post(
            f"{settings.runtime_service_endpoint}relationships/{relationship_id}/synthesize/{new_package_name}/",
            headers=authorization_headers, json={})

        if response.status_code != 200:
            api.logger.warning(msg=f"{request} returned error code {response.status_code}")

        return response.json(), response.status_code
