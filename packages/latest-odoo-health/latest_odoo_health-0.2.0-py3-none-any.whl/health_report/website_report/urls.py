from django.urls import path
from website_report import views

urlpatterns = [
    path('get-seo-details/',views.get_seo_details,name='get-seo-details'),
    path('get-social-media-links/',views.get_social_media_links,name='get-social-media-links'),
    path('get-robots-txt/',views.get_check_robots_txt,name='get-robots-txt'),
    path('get-redirects/',views.get_check_redirects,name='get-redirects'),
    path('get-seo-friendly/',views.get_seo_friendly,name='get-seo-friendly'),
    path('get-website-grading/',views.get_website_grading,name='get-website-grading'),
]
