"""
This module is used to map urls path with view method
"""

from django.urls import path
from system_report import views

urlpatterns = [
    path('system-data/',views.system_report,name="system-data"),
    path('get-server-uptime/',views.get_server_uptime,name="get-server-uptime"),
]
