# -*- coding: utf-8 -*-
from datetime import timedelta
import os
from pprint import pprint
import psutil
from django.db import connections,models
import math
from django.utils.timezone import now
# import pytz
import xmlrpc.client
from login_app.methods import xmlrpc_connection
from login_app.models import OdooSetup


DB_SETTING_NAME = 'postgresql'
ODOO_DATA_DIR = "/var/lib/odoo/filestore/"


class DatabaseMetrics(models.Model):
    """Class representing the database metrics"""
    _name = 'database.metrics'
    _description = 'Database Metrics'

    def collect_database_metrics(self):
        """Collect database performance metrics"""
        database_metrics =xmlrpc_connection("database.metrics.package", "collect_metrics")
        return database_metrics

    def odoo_file_health(self):
        """Fetch Odoo's file health from PostgreSQL"""
        odoo_file_health = xmlrpc_connection(model_name="database.metrics.package",function_name="odoo_file_health")
        return odoo_file_health
    
    def get_concurrent_session_count(self):
        """Fetch Concurrent sesssions"""
        session_count = xmlrpc_connection(model_name="database.metrics.package",function_name="get_concurrent_session_count")
        return session_count 