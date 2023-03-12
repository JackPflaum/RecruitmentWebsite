from django.db import models
from accounts.models import User, Profile, use_directory_path

class JobPositions(models.Model):
    job_title = models.CharField(max_length=255)
    job_details = models.TextField(default='Job details to come.')
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    posted = models.DateField(auto_now_add=True)
    closing_date = models.DateField()

    def __str__(self):
        return self.job_title
    

class Applied(models.Model):
    job = models.ForeignKey(JobPositions, related_name='applied_job', on_delete=models.CASCADE)
    applicant = models.ForeignKey(Profile, related_name='applied_applicant', on_delete=models.CASCADE)
    covering_letter = models.FileField(blank=False, upload_to=use_directory_path)
    applied_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.applicant)
