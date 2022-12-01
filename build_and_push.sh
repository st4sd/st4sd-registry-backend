#
#   Copyright IBM Inc. All Rights Reserved.
#   SPDX-License-Identifier: Apache-2.0
#
#   Author: Alessandro Pomponio
#

#!/bin/bash

#TODO: add validation on input params
docker login -u $DOCKER_USER -p $DOCKER_PASS $DOCKER_REGISTRY
docker run --privileged --rm tonistiigi/binfmt --install arm64,ppc64le
docker buildx create --use
docker buildx build --platform linux/amd64 --push -t $1 .