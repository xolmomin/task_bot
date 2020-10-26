from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from app.views import web_hook_view

urlpatterns = [
    path('api/', csrf_exempt(web_hook_view)),
]
