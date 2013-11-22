from social_tenant.local_common_settings import *

ROOT_URLCONF = 'social_tenant.main.urls'
WSGI_APPLICATION = 'social_tenant.main.wsgi.application'

AUTH_USER_MODEL = "users.Administrator"

SHARED_APPS += (
    "django.contrib.auth",
    "main.users",
)

TENANT_APPS += (
)

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)