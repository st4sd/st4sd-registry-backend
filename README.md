# ST4SD Registry Backend

The ST4SD Registry backend is a proxy to the
[ST4SD Runtime Service](https://github.com/st4sd/st4sd-runtime-service) for the
[ST4SD Registry UI](https://github.com/st4sd/st4sd-registry-ui). It is a simple
REST API written in Python.

## Quick links

- [Getting started](#getting-started)
- [Development](#development)
- [Help and Support](#help-and-support)
- [Contributing](#contributing)
- [License](#license)

## Getting started

### Requirements

#### Python

Running and developing this project requires a recent Python version, it is
suggested to use Python 3.7 or above. You can find instructions on how to
install Python on the [official website](https://www.python.org/downloads/).

## Development

### Creating a virtual environment (optional)

Ensure you have `virtualenv` installed with:

```shell
virtualenv --version
```

If you don't have it installed, run:

```shell
pip install virtualenv
```

Create a virtual environment called with:

```shell
virtualenv venv
```

This will create a Python virtual environment called **venv**. Activate it with:

```shell
source venv/bin/activate
```

To deactivate it, simply use:

```shell
deactivate
```

### Installing dependencies

Install the dependencies for this project with:

```bash
pip install -r requirements.txt
```

### Developing locally

To spin up a local development build of the ST4SD Registry Backend you will need
to have a working OpenShift deployment of ST4SD, as it will have to connect to
other components (the Runtime Service and the Datastore).

#### Getting a token to access ST4SD

As the backend will have to authenticate to ST4SD, you will need to provide a
token that has sufficient authorizations. The safest option is to use the
`workflow-operator` token.

1. Log into your cluster from the command line (using `oc login`) and ensure
   you're in the project where you have installed ST4SD (using `oc project`).
2. List the secrets available in the namespace you are in and look for ones
   related to the `workflow-operator` as follows (your output should be
   similar):

   ```bash
   oc get secrets | grep workflow-operator
   workflow-operator-dockercfg-jnlx9                   kubernetes.io/dockercfg               1      168d
   workflow-operator-token-28qgm                       kubernetes.io/service-account-token   4      168d
   workflow-operator-token-g6594                       kubernetes.io/service-account-token   4      168d
   ```

   In this example we will use `workflow-operator-token-28qgm`.

3. Get the Service Account token and save it to a file:

   ```bash
   oc get secret workflow-operator-token-28qgm -o jsonpath='{.data.token}' | base64 -d > $HOME/.st4sd_serviceaccount_token
   ```

   This will store the token in a file called `.st4sd_serviceaccount_token` in
   your home directory.

#### Creating a development entry in settings.toml

The backend stores its configuration in the `settings.toml` file. By default it
will use the `production` configuration, which uses internal OpenShift DNS
routing. As these routes won't work outside of the cluster, we will need to
provide the external ones.

You can get the external base route for your cluster with:

```bash
ST4SD_AUTH_ROUTE=$(oc get route st4sd-authentication -o jsonpath='{.spec.host}')
```

We can then extend the toml configuration file with:

```bash
echo -e "\n\n[development]
runtime_service_endpoint = \"https://${ST4SD_AUTH_ROUTE}/rs/\"
datastore_registry_endpoint = \"https://${ST4SD_AUTH_ROUTE}/ds-registry/\"
datastore_rest_endpoint = \"https://${ST4SD_AUTH_ROUTE}/ds-mongodb-proxy/\"
token_path=\"$HOME/.st4sd_serviceaccount_token\"
" >> settings.toml
```

#### Using the development configuration

To ensure the Backend uses the development configuration we need to set the
`ENV_FOR_DYNACONF` environment variable:

```bash
export ENV_FOR_DYNACONF=development
```

#### Spinning up the backend locally

We can start the local backend with:

```bash
python app.py
```

### Lint and fix files

Coming soon.

## Help and Support

Please feel free to reach out to one of the maintainers listed in the
[MAINTAINERS.md](MAINTAINERS.md) page.

## Contributing

We always welcome external contributions. Please see our
[guidance](CONTRIBUTING.md) for details on how to do so.

## License

This project is licensed under the Apache 2.0 license. Please
[see details here](LICENSE.md).
