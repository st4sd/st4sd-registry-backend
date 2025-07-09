FROM mirror.gcr.io/python:3.10-alpine
RUN apk update && \
    apk add gcc linux-headers musl-dev && \
    apk cache clean && apk cache purge

COPY requirements.txt .
COPY *.py ./
COPY apis ./apis
COPY utils ./utils
COPY settings.toml ./settings.toml
RUN pip install -r requirements.txt
EXPOSE 8085

ENTRYPOINT ["python", "app.py"]
