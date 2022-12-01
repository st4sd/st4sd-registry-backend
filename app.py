#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Author: Alessandro Pomponio
#
from flask import Flask
from flask_cors import CORS
from waitress import serve

from apis import api

app = Flask(__name__)
CORS(app)
api.init_app(app)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8085)
