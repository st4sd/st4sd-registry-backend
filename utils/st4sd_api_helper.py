#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Author: Alessandro Pomponio
#
import experiment.service.db

from utils.config import settings


def get_api_token():
    with open(settings.token_path, "r") as f:
        token = f.readlines()[0].strip()
    return token


def get_api():
    api = experiment.service.db.ExperimentRestAPI(
        settings.runtime_service_endpoint,
        cdb_registry_url=settings.datastore_registry_endpoint,
        cdb_rest_url=settings.datastore_rest_endpoint,
        cc_bearer_key=get_api_token(),
        test_cdb_connection=False,
        validate_auth=False,
        discover_cdb_urls=False,
    )

    return api


def get_authorization_headers():
    headers = {}
    if settings.ENV_FOR_DYNACONF != "production":
        headers["Authorization"] = f"Bearer {get_api_token()}"
    return headers
