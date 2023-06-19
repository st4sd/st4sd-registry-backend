#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Author: Alessandro Pomponio
#
from flask_restx import Api

from .canvas import api as canvas_api
from .experiments import api as experiments_api
from .logs import api as logs_api
from .properties import api as properties_api
from .runs import api as runs_api
from .settings import api as settings_api

api = Api(
    title='ST4SD Registry Backend',
    version='0.1',
)

api.add_namespace(logs_api, path='/logs')
api.add_namespace(experiments_api, path='/experiments')
api.add_namespace(runs_api, path='/runs')
api.add_namespace(settings_api, path='/settings')
api.add_namespace(properties_api, path='/properties')
api.add_namespace(canvas_api, path='/canvas')
