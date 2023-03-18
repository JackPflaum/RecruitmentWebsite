from django.contrib import admin

from .models import JobPositions, Applied

class JobPositionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'job_title']

admin.site.register(JobPositions, JobPositionsAdmin,)


class AppliedAdmin(admin.ModelAdmin):
    list_display = ['id', 'job', 'applicant', 'covering_letter', 'applied_date']

admin.site.register(Applied, AppliedAdmin)
