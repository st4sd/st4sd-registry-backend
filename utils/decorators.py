from functools import wraps

from flask import abort

from utils import envvars


def disable_on_global_instances(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if envvars.is_global_registry():
            # 405 - Method Not Allowed
            return abort(405)
        return f(*args, **kwargs)

    return decorated_function


def disable_with_env_var(var_name):
    def disabling_decorator(f):
        @wraps(f)
        def do_disable_with_env_var(*args, **kwargs):
            if envvars.get_settings_env_vars().get(var_name, "no") == "yes":
                # 405 - Method Not Allowed
                return abort(405)
            return f(*args, **kwargs)

        return do_disable_with_env_var

    return disabling_decorator


def enable_with_env_var(var_name):
    def enabling_decorator(f):
        @wraps(f)
        def do_enable_with_env_var(*args, **kwargs):
            if envvars.get_settings_env_vars().get(var_name, "no") == "yes":
                return f(*args, **kwargs)

            # 405 - Method Not Allowed
            return abort(405)

        return do_enable_with_env_var

    return enabling_decorator
