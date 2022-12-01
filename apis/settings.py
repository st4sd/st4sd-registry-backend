#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Author: Alessandro Pomponio
#
import os

from flask import jsonify
from flask_restx import Namespace, Resource

api = Namespace('settings', description='Registry UI-related settings')


@api.route('/')
class SettingsList(Resource):
    @api.doc('get_settings')
    def get(self):
        """Get all settings"""
        env_vars = os.environ
        response = {}

        for k in env_vars.keys():
            if k.startswith("ST4SD_REGISTRY_UI_SETTINGS_"):
                response[k] = os.environ[k]

        return jsonify(response)
