FROM mirror.gcr.io/python:3.12-alpine AS build_stage
RUN apk update && \
    apk add gcc linux-headers musl-dev
COPY requirements.txt .
RUN pip install --upgrade pip setuptools && pip install -r requirements.txt

FROM mirror.gcr.io/python:3.12-alpine
COPY --from=build_stage /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
RUN pip install --upgrade pip setuptools
COPY requirements.txt .
COPY *.py ./
COPY apis ./apis
COPY utils ./utils
COPY settings.toml ./settings.toml
EXPOSE 8085

ENTRYPOINT ["python", "app.py"]
