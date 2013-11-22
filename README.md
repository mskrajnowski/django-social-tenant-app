django-social-tenant-app
========================

A proof-of-concept app pairing python-social-auth with django-tenant-schemas


Setup
-----

1. Install all the requirements:

    ```
    pip install -r requirements/base.txt
    ```

2. Create a Google OAuth2 API project through the Google APIs console: <http://code.google.com/apis/console/>.
   More info: <https://developers.google.com/console/help/>

3. Set the Redirect URIs to: http://auth.localhost.com:8001/auth/complete/google-oauth2/

4. Create social_tenant.local_common_settings, eg:
    ```python
    # you need to import everything from common settings
    from .common_settings import *

    # setup the root urls for the main app and the tenant app, ports are there
    # for local development setups
    MAIN_ROOT_URL = "localhost.com:8000"
    TENANT_ROOT_URL = "localhost.com:8001"

    # on an actual server those values will probably be the same, eg.:
    # MAIN_ROOT_URL = "myappdomain.com"
    # TENANT_ROOT_URL = MAIN_ROOT_URL

    # specify the database to be used by both apps
    DATABASES = {
        'default': {
            'ENGINE': 'tenant_schemas.postgresql_backend',
            'NAME': 'social_tenant_db',
            'USER': 'user',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = '#################################################'
    ```
5. Create social_tenant.main.local_settings, eg:
    ```python
    # you need to import * from social_tenant.main.settings
    from .settings import *

    # nothing else required here
    ```
6. Create social_tenant.tenant.local_settings, eg:
    ```python
    # you need to import * from social_tenant.tenant.settings
    from .settings import *

    # specify the auth tenant url, which google will redirect to
    TENANT_AUTH_COMPLETE_URL = ".".join(("auth", TENANT_ROOT_URL))

    # specify the google cliend id (key) and the client secret (secret)
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '############.apps.googleusercontent.com'
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '#######################'
    ```
7. Sync shared apps:

    ```
    python manage.py main sync_schemas --shared
    python manage.py tenant sync_schemas --shared
    ```
8. Create the root, auth and some sample tenants through the django shell
   (python manage.py main shell, you might need to create each tenant
    in a new shell):
    ```python
    from tenant.models import Tenant

    Tenant.objects.create(name="main", domain_url="example.com", schema_name="public")
    Tenant.objects.create(name="auth", domain_url="auth.example.com", schema_name="public")

    Tenant.objects.create(name="tenant1", domain_url="client1.example.com", schema_name="tenant1")
    Tenant.objects.create(name="tenant2", domain_url="client2.example.com", schema_name="tenant2")
    ```
9. Add localhost.com entries to /etc/hosts (google doesn't support auth.localhost/... redirect urls):
    ```
    127.0.0.1       auth.localhost.com
    127.0.0.1       localhost.com

    127.0.0.1       client1.localhost.com
    127.0.0.1       client2.localhost.com
    ```
10. Start both apps:

    ```
    python manage.py main runserver 8000
    python manage.py tenant runserver 8001
    ```
11. With any luck, if you now open http://client1.example.com it will redirect
    you to a google oauth2 page and when you authorize the site it should
    show some basic info about the tenant and the logged in user.

Enjoy!
------