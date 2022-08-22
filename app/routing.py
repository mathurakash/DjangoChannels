from django.urls import path
from . import consumers

websocket_urlpatterns=[
    path('ws/sc/<str:group_name>/',consumers.MySyncConsumer.as_asgi()),
    path('ws/ac/<str:group_name>/',consumers.MyAsyncConsumer.as_asgi()),
    path('ws/call/<str:group_name>', consumers.CallConsumer.as_asgi()),
]