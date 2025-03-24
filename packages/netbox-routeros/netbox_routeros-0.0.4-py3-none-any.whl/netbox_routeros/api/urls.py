from netbox.api.routers import NetBoxRouter

from netbox_routeros.api import views
from netbox_routeros.api.views import proxy as proxy_views
from netbox_routeros.models import proxy

router = NetBoxRouter()
# Core
router.register("routeros/instances", views.RouterosInstanceViewSet)
router.register("routeros/types", views.RouterosTypeViewSet)
# Proxy
router.register(
    "proxy/dcim/interfaces",
    proxy_views.InterfaceViewSet,
    basename=proxy.Interface._meta.object_name.lower(),
)
# Interfaces
router.register("interfaces/interface-lists", views.InterfaceListViewSet)
# CapsMan
router.register("capsman/instances", views.CapsmanInstanceViewSet)
router.register("capsman/server-configs", views.CapsmanServerConfigViewSet)
router.register("capsman/channels", views.CapsmanChannelViewSet)
router.register("capsman/datapaths", views.CapsmanDatapathViewSet)
router.register("capsman/access-list-items", views.CapsmanAccessListItemViewSet)

urlpatterns = router.urls
