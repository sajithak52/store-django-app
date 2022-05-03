

def get_env():
    import os

    dir_name = os.path.dirname(__file__)
    path = os.path.join(dir_name, '.env')
    print(path)
    if not os.path.exists(path):
        raise SystemExit(
            "The environment file is missing. Please create .env and specify the development environment")

    fp = open(path)
    mode = fp.read()
    mode = mode.strip()
    fp.close()

    if mode in ('dev', 'pg_test', 'live', 'uat'):
        return mode


ENV = get_env()

print("The Environment is :", ENV)

if ENV == 'dev':
    from .dev import *

elif ENV == 'pg_test':
    from .pg_test import *

else:
    raise SystemExit("Invalid Application Environment")