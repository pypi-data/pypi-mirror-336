

from django.shortcuts import render
from system_report.models import SystemMetrics
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def system_report(request):
    system_metrics = SystemMetrics()
    get_system_metrics_data = system_metrics.get_system_metrics_data()
    return Response (get_system_metrics_data)

@api_view(['GET'])
def get_server_uptime(request):
    system_metrics = SystemMetrics()
    get_server_uptime = system_metrics.get_server_uptime()
    
    return Response (get_server_uptime)
    