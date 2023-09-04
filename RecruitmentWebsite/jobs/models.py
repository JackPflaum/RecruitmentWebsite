from django.db import models
from accounts.models import User
from django.template.defaultfilters import slugify

def use_directory_path(instance, filename):
    """returns the directory path where the media file will be stored"""
    # file will be uploaded to MEDIA_ROOT/JobId_number/filename
    return 'JobID#{0}_{1}/user#{2}_{3}-{4}_covering_letter'.format(instance.job.id, instance.job, instance.applicant.id, instance.applicant.first_name, instance.applicant.last_name)
    

class JobPositions(models.Model):
    job_title = models.CharField(max_length=255)
    job_summary = models.TextField(default='Job details to come.')
    job_details = models.TextField(default='Job details to come.')
    salary = models.CharField(max_length=255,blank=True)
    skills = models.TextField(blank=True)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    posted = models.DateField(auto_now_add=True)
    closing_date = models.DateField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.job_title
    
    def format_skills_dot_points(self):
        """splits skills into separate lines so it they can be rendered as dot points on the page"""
        return self.skills.split('\n')
    
    def slugify_job(self):
        """slugify job position slug field using title and company"""
        if not self.slug:
            job_title_slug = slugify(self.job_title)
            company_slug = slugify(self.company)

            # create unique slug
            unique_slug = f'{job_title_slug}_{company_slug}'
            num = 2

            # if slug already exists then add incremental number to the end
            while JobPositions.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{job_title_slug}_{company_slug}-{num}'
                num += 2
                
            self.slug = unique_slug

    def save(self, *args, **kwargs):
        """slugify job position"""
        self.slugify_job()

        super().save(*args, **kwargs)
    

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
