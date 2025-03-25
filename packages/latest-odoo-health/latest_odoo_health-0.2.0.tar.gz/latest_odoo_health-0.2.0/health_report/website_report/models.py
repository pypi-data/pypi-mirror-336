from django.db import models
from login_app.methods import xmlrpc_connection

# Create your models here.

class WebsiteSeoDetails(models.Model):

    def seo_details(self):
        seo_details = xmlrpc_connection(model_name='website.seo.details',function_name='seo_details')
        return seo_details

    def check_internal_external_social_media_links(self):
        check_internal_external_social_media_links = xmlrpc_connection(model_name='website.seo.details',function_name='check_internal_external_social_media_links')
        return check_internal_external_social_media_links
    
    def check_robots_txt(self):
        check_robots_txt = xmlrpc_connection(model_name='website.seo.details',function_name='check_robots_txt')
        return check_robots_txt
    
    def check_redirects(self):
        check_redirects = xmlrpc_connection(model_name='website.seo.details',function_name='check_redirects')
        return check_redirects
    
    def is_url_seo_friendly(self):
        is_url_seo_friendly = xmlrpc_connection(model_name='website.seo.details',function_name='is_url_seo_friendly')
        return is_url_seo_friendly
    
    def website_grading(self):
        website_grading = xmlrpc_connection(model_name='website.seo.details',function_name='website_grading')
        return website_grading
    
    