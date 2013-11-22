from django.conf import settings
from django.core.urlresolvers import reverse
from social.backends.utils import load_backends
from social.p3 import urlparse, urlunparse, parse_qs
from social.strategies.django_strategy import DjangoStrategy
from tenant_schemas.utils import get_tenant_model


class DjangoTenantStrategy(DjangoStrategy):
    """
    django-social-auth strategy for applications based on
    django-tenant-schemes.

    Changes the way social auth generates the redirect urls:
    - changes the redirect url to the root domain
    - adds a 'tenant' state variable to the redirect url, so the view on the
      root domain can redirect back to the correct tenant

    Google OAuth2 (and probably others too) require that you specify
    redirect urls explicitly, without any wildcards. In a scenario
    where tenants are created dynamically it's not possible.
    """

    state_key = "tenant_oauth2_state"

    def __init__(self, *args, **kwargs):
        backends_by_name = load_backends(settings.AUTHENTICATION_BACKENDS)

        self.social_state_keys = []
        self.auth_complete_paths = []
        for backend_name in backends_by_name.keys():
            self.social_state_keys.append(
                "{}_state".format(backend_name)
            )

            self.auth_complete_paths.append(
                reverse("social:complete", kwargs={'backend': backend_name})
            )

        super(DjangoTenantStrategy, self).__init__(*args, **kwargs)

    def generate_state(self):
        csrf_token = self.random_string(32)
        return csrf_token, self.request.tenant

    def get_state_value(self):
        state_value = self.session.get(self.state_key, None)
        if state_value is None:
            csrf, tenant = self.generate_state()
            state_value = "{}-{}".format(csrf, tenant.pk)
            self.session[self.state_key] = state_value

        return state_value

    @classmethod
    def tenant_from_state(cls, state):
        _, tenant_pk = state.rsplit("-", 1)
        return get_tenant_model().objects.get(pk=tenant_pk)

    def session_get(self, name, default=None):
        if name == self.state_key or name in self.social_state_keys:
            return self.get_state_value()

        return super(DjangoTenantStrategy, self).session_get(name, default)

    @classmethod
    def _replace_domain(cls, url, new_domain):
        parsed_url = urlparse(url)
        url_parts = list(parsed_url)
        new_netloc = new_domain

        if ":" not in new_domain and ":" in parsed_url.netloc:
            _, port = parsed_url.netloc.split(":")
            new_netloc = "{}:{}".format(new_domain, port)

        url_parts[1] = new_netloc
        return urlunparse(url_parts)

    @classmethod
    def get_tenant_url(cls, url):
        parsed_url = urlparse(url)
        url_parts = list(parsed_url)
        query = parse_qs(parsed_url.query)
        state_value = (query.get('state', None)
                       or query.get('redirect_state', None))

        if not state_value:
            return None

        if isinstance(state_value, list):
            state_value = state_value[0]

        tenant = cls.tenant_from_state(state_value)
        tenant_domain = tenant.domain_url

        if ":" in settings.TENANT_AUTH_COMPLETE_URL:
            _, port = settings.TENANT_AUTH_COMPLETE_URL.split(":")
            tenant_domain = ":".join((tenant_domain, port))

        url_parts[1] = tenant_domain
        return urlunparse(url_parts)

    def build_absolute_uri(self, path=None):
        url = super(DjangoTenantStrategy, self).build_absolute_uri(path)
        auth_domain = settings.TENANT_AUTH_COMPLETE_URL

        if path and path in self.auth_complete_paths:
            parsed_url = urlparse(url)
            url_parts = list(parsed_url)
            url_parts[1] = auth_domain
            return urlunparse(url_parts)

        return url
