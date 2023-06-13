FROM quay.io/st4sd/official-base/st4sd-runtime-core:py310-latest
COPY requirements.txt .
COPY *.py ./
COPY apis ./apis
COPY utils ./utils
COPY settings.toml ./settings.toml
RUN pip install -r requirements.txt
EXPOSE 8085

ENTRYPOINT ["python", "app.py"]
