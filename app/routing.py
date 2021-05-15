from channels.routing import ProtocolTypeRouter, URLRouter
from room import routing as core_routing
from .token_auth import TokenAuthMiddleware



application = ProtocolTypeRouter({
    "websocket": 
    TokenAuthMiddleware(
        URLRouter(
           
             core_routing.websocket_urlpatterns
        )
    ),
})


