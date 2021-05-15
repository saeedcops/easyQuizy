
from . import consumer

from django.conf.urls import url

# websocket_urlpatterns = [
#     path('ws/room/<uri>/', consumer.RoomConsumer),
#     ]
websocket_urlpatterns = [
    url(r'^ws/room/(?P<pk>[^/]+)/$', consumer.RoomConsumer.as_asgi()),

]
