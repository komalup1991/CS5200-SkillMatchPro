# your_app_name/admin.py

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.shortcuts import render
from django.urls import path
from django.db import connection
from django.utils import timezone
from myProjects.models import Bid
from myProjects.models import Project

class CustomAdminSite(AdminSite):
    site_header = 'Your Custom Admin'
    site_title = 'Your Admin Portal'
    index_title = 'Welcome to Your Admin Dashboard'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='admin-dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        today = timezone.now().date()
        week_number = today.isocalendar()[1]

        # Call the stored procedure to get daily reports
        with connection.cursor() as cursor:
            cursor.callproc('GetReports', [str(today), week_number, 1])
            result = cursor.fetchall()
            columns = ["bid_id", "project_id", "user_id", "amount", "date", "status"]
            daily_reports = []
            for row in result:
                daily_reports.append(dict(zip(columns, row)))

            # Call the stored procedure to get weekly reports
            cursor.callproc('GetReports', [str(today), week_number, 2])
            result = cursor.fetchall()
            columns = ["project_id", "freelancer_id", "bidder_id","title", "budget", "status"]
            weekly_reports = []
            for row in result:
                weekly_reports.append(dict(zip(columns, row)))

        context = {
            'daily_reports': daily_reports,
            'weekly_reports': weekly_reports,
        }

        return render(request, 'adminHome/dashboard.html', context)

# Create an instance of the custom admin site
custom_admin_site = CustomAdminSite(name='custom-admin')

# Register models with the custom admin site
# custom_admin_site.register(Message)
# custom_admin_site.register(Bid)
# custom_admin_site.register(Project)
