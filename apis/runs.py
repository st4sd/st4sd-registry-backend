#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Author: Alessandro Pomponio
#
from flask import jsonify
from flask_restx import Namespace, Resource

from utils.st4sd_api_helper import get_api
from utils.decorators import disable_on_global_instances

api = Namespace('runs', description='Run-related operations')


@api.route('/')
class RunList(Resource):
    @api.doc('get_all_runs')
    @disable_on_global_instances
    def get(self):
        """Get all runs"""
        st4sd_api = get_api()
        response = st4sd_api.cdb_get_document_experiment(query={})
        return jsonify(response)


@api.route("/<pvep>")
class PVEPRunList(Resource):
    @api.param('pvep', 'The PVEP identifier')
    @api.doc('get_runs_for_pvep')
    @disable_on_global_instances
    def get(self, pvep: str):
        """Get all runs for a PVEP"""
        st4sd_api = get_api()
        if ":" in pvep:
            experiment_name = pvep[:pvep.index(":")]
            pvep_def = st4sd_api.api_get_experiment(pvep)
            digest = pvep_def['metadata']['registry']['digest']
            identifier = '@'.join([experiment_name, digest])
            query = {'metadata.userMetadata.experiment-id': identifier}
        elif "@" in pvep:
            query = {'metadata.userMetadata.experiment-id': pvep}
        else:
            query = {'metadata.userMetadata.st4sd-package-name': pvep}

        response = st4sd_api.cdb_get_document_experiment(query=query)
        return jsonify(response)


@api.route("/<pvep>/<rest_uid>")
class PVEPRunList(Resource):
    @api.param('pvep', 'The PVEP identifier')
    @api.param('rest_uid', 'The PVEP rest_uid')
    @api.doc('get_runs_for_rest_uid')
    @disable_on_global_instances
    def get(self, pvep: str, rest_uid: str):
        """Get all runs for a rest_uid"""
        st4sd_api = get_api()
        doc = st4sd_api.cdb_get_document(query={'metadata.userMetadata.rest-uid': rest_uid})
        if len(doc) > 0:
            response = st4sd_api.cdb_get_document_component(instance=doc[0]['metadata']['instanceName'])
        else:
            response = {}
        return jsonify(response)
