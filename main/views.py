from django.http.response import HttpResponse
from tenant_schemas.utils import get_tenant_model


def index(request):
    tenant_info = get_tenant_model().objects.values(
        "schema_name", "domain_url"
    )

    return HttpResponse(
        u"Main website. <br>"
        u"User: {user.username}. <br>"
        u"Tenants: {tenants}. <br>"
        .format(user=request.user, tenants=tenant_info)
    )