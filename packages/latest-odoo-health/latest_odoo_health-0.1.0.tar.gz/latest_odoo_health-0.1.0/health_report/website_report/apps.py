from django.apps import AppConfig


class WebsiteReportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website_report'

    def ready(self):
        from health_report.urls import path,urlpatterns,include
        urlpatterns.append(
            path('',include('website_report.urls'))
        )
        return super().ready()
