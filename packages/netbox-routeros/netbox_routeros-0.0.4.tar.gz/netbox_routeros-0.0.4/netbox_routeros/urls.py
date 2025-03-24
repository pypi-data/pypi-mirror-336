from django.urls import include, path
from netbox.views.generic import ObjectChangeLogView
from utilities.urls import get_model_urls

from . import views  # noqa: F401 must be imported
from . import models

urlpatterns = [
    # --- Core ---
    path(
        "routeros/types/",
        include(get_model_urls("netbox_routeros", "routerostype", detail=False)),
    ),
    path(
        "routeros/types/<int:pk>/",
        include(get_model_urls("netbox_routeros", "routerostype")),
    ),
    path(
        "routeros/types/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="routerostype_changelog",
        kwargs={"model": models.RouterosType},
    ),
    path(
        "routeros/instances/",
        include(get_model_urls("netbox_routeros", "routerosinstance", detail=False)),
    ),
    path(
        "routeros/instances/<int:pk>/",
        include(get_model_urls("netbox_routeros", "routerosinstance")),
    ),
    path(
        "routeros/instances/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="routerosinstance_changelog",
        kwargs={"model": models.RouterosInstance},
    ),
    # --- Iterfaces ---
    # interface list
    path(
        "interfaces/interface-lists/",
        include(get_model_urls("netbox_routeros", "interfacelist", detail=False)),
    ),
    path(
        "interfaces/interface-lists/<int:pk>/",
        include(get_model_urls("netbox_routeros", "interfacelist")),
    ),
    path(
        "interfaces/interface-lists/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="interfacelist_changelog",
        kwargs={"model": models.InterfaceList},
    ),
    # --- CapsMan ---
    # instance
    path(
        "capsman/instances/",
        include(get_model_urls("netbox_routeros", "capsmaninstance", detail=False)),
    ),
    path(
        "capsman/instances/<int:pk>/",
        include(get_model_urls("netbox_routeros", "capsmaninstance")),
    ),
    path(
        "capsman/instances/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="capsmaninstance_changelog",
        kwargs={"model": models.CapsmanInstance},
    ),
    # server config
    path(
        "capsman/server-configs/",
        include(get_model_urls("netbox_routeros", "capsmanserverconfig", detail=False)),
    ),
    path(
        "capsman/server-configs/<int:pk>/",
        include(get_model_urls("netbox_routeros", "capsmanserverconfig")),
    ),
    path(
        "capsman/server-configs/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="capsmanserverconfig_changelog",
        kwargs={"model": models.CapsmanServerConfig},
    ),
    # channel
    path(
        "capsman/channels/",
        include(get_model_urls("netbox_routeros", "capsmanchannel", detail=False)),
    ),
    path(
        "capsman/channels/<int:pk>/",
        include(get_model_urls("netbox_routeros", "capsmanchannel")),
    ),
    path(
        "capsman/channels/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="capsmanchannel_changelog",
        kwargs={"model": models.CapsmanChannel},
    ),
    # datapath
    path(
        "capsman/datapaths/",
        include(get_model_urls("netbox_routeros", "capsmandatapath", detail=False)),
    ),
    path(
        "capsman/datapaths/<int:pk>/",
        include(get_model_urls("netbox_routeros", "capsmandatapath")),
    ),
    path(
        "capsman/datapaths/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="capsmandatapath_changelog",
        kwargs={"model": models.CapsmanDatapath},
    ),
    # access list
    path(
        "capsman/access-list-items/",
        include(
            get_model_urls("netbox_routeros", "capsmanaccesslistitem", detail=False)
        ),
    ),
    path(
        "capsman/access-list-items/<int:pk>/",
        include(get_model_urls("netbox_routeros", "capsmanaccesslistitem")),
    ),
    path(
        "capsman/access-list-items/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="capsmanaccesslistitem_changelog",
        kwargs={"model": models.CapsmanAccessListItem},
    ),
]
