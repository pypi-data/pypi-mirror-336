from django.shortcuts import render

# Create your views here.
from website_report.models import WebsiteSeoDetails
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_seo_details(request):
    seo_details = WebsiteSeoDetails().seo_details()
    return Response(seo_details)

@api_view(['GET'])
def get_social_media_links(request):
    check_social_media_links = WebsiteSeoDetails().check_internal_external_social_media_links()
    return Response(check_social_media_links)

@api_view(['GET'])
def get_check_robots_txt(request):
    check_robots_txt = WebsiteSeoDetails().check_robots_txt()
    return Response(check_robots_txt)

@api_view(['GET'])
def get_check_redirects(request):
    check_redirects = WebsiteSeoDetails().check_redirects()
    return Response(check_redirects)

@api_view(['GET'])
def get_seo_friendly(request):
    is_url_seo_friendly = WebsiteSeoDetails().is_url_seo_friendly()
    return Response(is_url_seo_friendly)

@api_view(['GET'])
def get_website_grading(request):
    website_grading = WebsiteSeoDetails().website_grading()
    return Response(website_grading)

