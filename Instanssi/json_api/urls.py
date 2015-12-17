# -*- coding: utf-8 -*-

from django.conf.urls import url, include

urlpatterns = [
    url(r'^kompomaatti/', include('Instanssi.json_api.kompomaatti.urls', namespace="api_km")),
    url(r'^screen/', include('Instanssi.json_api.screen.urls', namespace="api_screen")),
]
