#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Author: Alessandro Pomponio
#

from flask import jsonify
from flask_restx import Namespace, Resource

import utils.envvars

api = Namespace("settings", description="Registry UI-related settings")


@api.route("/")
class SettingsList(Resource):
    @api.doc("get_settings")
    def get(self):
        """Get all settings"""
        response = utils.envvars.get_settings_env_vars()
        return jsonify(response)
