#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Authors: Philip Burrows, Andy Mair
#

from flask import jsonify
from flask_restx import Namespace, Resource

from utils.st4sd_api_helper import get_api

api = Namespace('properties', description='Measured Property related operations')


@api.route("/<pvep>")
class RunProperties(Resource):
    @api.param('pvep', 'The experiment identifier')
    @api.doc("get_all_properties_for_VE")
    def get(self, pvep: str):
        """Get all properties for a PVEP"""
        st4sd_api = get_api()
        query = {'$or': [{'metadata.userMetadata.st4sd-package-name': pvep}, {'metadata.userMetadata.package-name': pvep}]}
        matching_experiments = st4sd_api.cdb_get_document_experiment(pvep, query, include_properties=['*'], stringify_nan=True)
        properties = {}

        for experiment in matching_experiments:
            if "interface" in experiment and "propertyTable" in experiment["interface"]:
                rest_uid = experiment["metadata"]["userMetadata"]["rest-uid"]
                properties[rest_uid] = experiment["interface"]["propertyTable"]
        return properties


@api.route('/<pvep>/<rest_uid>')
class RunProperties(Resource):
    @api.param('pvep', 'The experiment identifier')
    @api.param('rest_uid', 'The run identifier')
    @api.doc('get_properties_for_rest_uid')
    def get(self, pvep: str, rest_uid: str):
        st4sd_api = get_api()
        response = st4sd_api.cdb_get_document_experiment_for_rest_uid(rest_uid, include_properties=['*'],
                                                                      stringify_nan=True)
        properties = {}
        if 'interface' in response and 'propertyTable' in response['interface']:
            properties[response['metadata']['userMetadata']['rest-uid']] = response['interface']['propertyTable']
        return jsonify(properties)
