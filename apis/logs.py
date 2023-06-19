#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Author: Alessandro Pomponio
#
from flask import jsonify
from flask_restx import Namespace, Resource

from utils.decorators import disable_on_global_instances
from utils.st4sd_api_helper import get_api

api = Namespace('logs', description='Log-related operations')


@api.route('/<rest_uid>')
class ExperimentLogs(Resource):
    @api.param('rest_uid', 'The experiment instance identifier')
    @api.doc('get_experiment_logs')
    @disable_on_global_instances
    def get(self, rest_uid: str):
        """Get the logs of an experiment instance"""
        st4sd_api = get_api()
        metadata = st4sd_api.cdb_get_document_user_metadata_for_rest_uid(rest_uid)
        try:
            response = st4sd_api.cdb_get_file_from_instance_uri(metadata['instance'], "output/experiment.log").decode(
                "utf-8")
        except ValueError:
            response = ""
        return jsonify(response)


@api.route('/<rest_uid>/<component_id>')
class ExperimentComponentLogs(Resource):
    @api.param('rest_uid', 'The experiment instance identifier')
    @api.param('component_id', 'The component identifier')
    @api.doc('get_experiment_component_logs')
    @disable_on_global_instances
    def get(self, rest_uid: str, component_id: str):
        """Get the logs of an experiment component"""
        st4sd_api = get_api()
        metadata = st4sd_api.cdb_get_document_user_metadata_for_rest_uid(rest_uid)

        try:
            retrieved = st4sd_api.cdb_get_components_last_stdout(metadata['instance'], component=component_id)
            if len(retrieved.keys()) > 0:
                response = retrieved[list(retrieved.keys())[0]][1].decode("utf-8")
            else:
                response = ""
        except ValueError:
            response = ""
        return jsonify(response)
