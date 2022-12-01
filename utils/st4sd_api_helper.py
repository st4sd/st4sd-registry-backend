#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Author: Alessandro Pomponio
#
import experiment.service.db

#
runtime_service_endpoint = "http://st4sd-runtime-service:4000/rs/experiments"
datastore_registry_endpoint = "http://st4sd-datastore-nexus:5001/ds-registry/"
datastore_rest_endpoint = "http://st4sd-authentication:5003/ds-mongodb-proxy/"


def get_api():
    token_path = '/var/run/secrets/tokens/rs-token'
    with open(token_path, 'r') as f:
        token = f.readlines()[0]

    api = experiment.service.db.ExperimentRestAPI(runtime_service_endpoint,
                                                  cdb_registry_url=datastore_registry_endpoint,
                                                  cdb_rest_url=datastore_rest_endpoint,
                                                  cc_bearer_key=token,
                                                  test_cdb_connection=False,
                                                  validate_auth=False,
                                                  discover_cdb_urls=False)
    return api
