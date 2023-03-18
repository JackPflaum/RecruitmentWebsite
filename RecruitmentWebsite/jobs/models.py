from django.db import models
from accounts.models import User

def use_directory_path(instance, filename):
    """returns the directory path where the media file will be stored"""
    # file will be uploaded to MEDIA_ROOT/JobId_number/filename
    return 'JobID#{0}_{1}/user#{2}_{3}-{4}_covering_letter'.format(instance.job.id, instance.job, instance.applicant.id, instance.applicant.first_name, instance.applicant.last_name)
    

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
    applicant = models.ForeignKey(User, related_name='applied_applicant', on_delete=models.CASCADE)
    covering_letter = models.FileField(blank=False, upload_to=use_directory_path)
    applied_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.applicant

    class Meta:
        # specifies that the 'applicant' (user) and 'job' fields must be unique in the Applied model.
        # if an applicant applies twice, it will raise a 'django.db.IntegrityError' exception.
        unique_together = ('applicant', 'job')
