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
from utils.decorators import disable_on_global_instances
from utils.st4sd_api_helper import get_api
from utils.st4sd_api_helper import get_authorization_headers

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
        experiment_name = pvep
        if ":" in pvep:
            experiment_name = pvep[:pvep.index(":")]
            pvep_def = st4sd_api.api_get_experiment(pvep)
            digest = pvep_def['metadata']['registry']['digest']
            identifier = '@'.join([experiment_name, digest])
            query = {'metadata.userMetadata.experiment-id': identifier}
        elif "@" in pvep:
            experiment_name = pvep[:pvep.index("@")]
            query = {'metadata.userMetadata.experiment-id': pvep}
        else:
            query = {'metadata.userMetadata.st4sd-package-name': pvep}

        # The runtime will register runs in the database automatically
        cdb_runs = st4sd_api.cdb_get_document_experiment(query=query)

        # For the runs that still haven't been registered to the DB yet
        # we need to query the runtime service.
        rs_instances = requests.get(
            f"{settings.runtime_service_endpoint}instances/", headers=get_authorization_headers())
        if rs_instances.status_code != 200:
            api.logger.warning(msg=f"{request} returned error code {rs_instances.status_code}")
            return {}, rs_instances.status_code

        # The instance endpoint is not pvep-specific, so we need to filter them manually.
        # As the contents of rs_instances will never be less than the ones in cdb_runs
        # we create a set of UIDs from the latter to quickly filter them out.
        cdb_rest_uids = {run['metadata']['userMetadata']['rest-uid'] for run in cdb_runs}

        for instance in rs_instances.json():
            if instance['id'] in cdb_rest_uids or instance['experiment']['metadata']['package']['name'] != experiment_name:
                continue

            # Convert rs_instances to the CDB data model and add it
            # to cdb_runs
            cdb_runs.append({
                "metadata": {
                    "userMetadata": {
                        "rest-uid": instance['id'],
                        "st4sd-package-digest": instance['experiment']['metadata']['registry']['digest']
                    },
                    "version": None
                },
                "status": {
                    "experiment-state": "Initialising",
                    "exit-status": None,
                    "created-on": None,
                }
            })

        return jsonify(cdb_runs)


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
