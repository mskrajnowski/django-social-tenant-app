from social_tenant.local_common_settings import *

ROOT_URLCONF = 'social_tenant.tenant.urls'
WSGI_APPLICATION = 'social_tenant.tenant.wsgi.application'

PUBLIC_SCHEMA_URLCONF = 'social_tenant.tenant.auth_urls'

AUTH_USER_MODEL = "users.User"

# SHARED_APPS += (
#
# )

TENANT_APPS += (
    "django.contrib.auth",
    "social.apps.django_app.default",
    "users",
)

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',

    'social.pipeline.social_auth.associate_by_email',

    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

LOGIN_URL          = '/auth/login/google-oauth2/'
LOGIN_REDIRECT_URL = '/'
# LOGIN_ERROR_URL    = '/auth/error'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

SOCIAL_AUTH_CREATE_USERS = True
SOCIAL_AUTH_USER_MODEL = 'users.User'
SOCIAL_AUTH_INACTIVE_USER_URL = '/inactive/'
SOCIAL_AUTH_SESSION_EXPIRATION = False
SOCIAL_AUTH_STRATEGY = "tenant.strategy.DjangoTenantStrategy"

TENANT_AUTH_COMPLETE_URL = ".".join(("auth", TENANT_ROOT_URL))
