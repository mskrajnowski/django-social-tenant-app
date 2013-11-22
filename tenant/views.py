from django.contrib.auth.decorators import login_required
from django.http.response import (HttpResponseRedirect, HttpResponseNotFound,
    HttpResponse)

from tenant.strategy import DjangoTenantStrategy


def redirect_auth_to_tenant(request):
    absolute_url = request.build_absolute_uri()
    tenant_url = DjangoTenantStrategy.get_tenant_url(absolute_url)

    if tenant_url:
        return HttpResponseRedirect(tenant_url)

    return HttpResponseNotFound()


@login_required
def index(request):
    return HttpResponse(
        u"Tenant: {tenant.domain_url}\n"
        u"Logged in as {user.username}, email: {user.email}"
        .format(user=request.user, tenant=request.tenant)
    )
