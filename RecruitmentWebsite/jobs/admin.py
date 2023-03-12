from django.contrib import admin

from .models import JobPositions

class JobPositionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'job_title']

admin.site.register(JobPositions, JobPositionsAdmin)
