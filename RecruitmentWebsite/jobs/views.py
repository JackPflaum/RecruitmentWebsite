from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import ContactUsForm, ApplicationForm
from .models import JobPositions, Applied
from accounts.views import login_user
from datetime import date
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'home.html', {})


def job_positions(request):
    """user can view all jobs that are available and use a search form to find a job"""

    # keyword search for job positions
    search_query = request.GET.get('search')

    todays_date = date.today()

    # get all job positions that haven't passed their closing date
    #'__gt' (greater than), compares field value with provided value.
    jobs = JobPositions.objects.filter(closing_date__gt=todays_date).order_by('posted')

    # check whether user has used search box
    # 'Q' object is used to create complex queries and '|' joins the queries
    if search_query:
        jobs = jobs.filter(
            Q(job_title__icontains=search_query) |
            Q(company__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # add pagination
    paginator = Paginator(jobs, 4) # shows 4 jobs per page
    page = request.GET.get('page') # retrieves the value associated with the 'page' parameter

    try:
        jobs = paginator.page(page) # retrieves the specific page from the 'paginator' object
    except PageNotAnInteger:
        jobs = paginator.page(1) # if the page number is not a valid integer it returns the first page
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages) # if the page number is out of range it delivers the last page

    context = {'jobs': jobs}
    return render(request, 'job_positions.html', context)


def job_details(request, job_slug):
    """user can view job details and apply for job"""
    job = get_object_or_404(JobPositions, slug=job_slug)

    if request.method == "POST":
        form = ApplicationForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            covering_letter = request.FILES['covering_letter']
            try:
                apply_job = Applied(job=job, applicant=request.user, covering_letter=covering_letter, applied_date=date.today())
            except IntegrityError:
                # user has already applied for the job
                return render(request, 'apply_error.html', {})
            else:
                apply_job.save()
                context = {'job': job}
                return render(request, 'application_confirmed.html', context)
    
    form = ApplicationForm()

    # check if user has applied for the job and store as True or False
    applied = Applied.objects.filter(job=job, applicant=request.user.id).exists()

    context = {'job': job, 'apply_form': form, 'user': request.user, 'applied': applied}
    return render(request, 'job_details.html', context)


def application_confirmed(request, job_slug):
    """confirm user has applied for job"""
    job = get_object_or_404(JobPositions, slug=job_slug)
    context = {'job': job}
    return render(request, 'application_confirmed.html', context)


def about_us(request):
    return render(request, 'about_us.html', {})


def contact_us(request):
    """company contact information and contact form"""
    # google api key to display google map on page
    map_key = settings.GOOGLE_API_KEY

    if request.method == "POST":
        form = ContactUsForm(request.POST)
        # clean the data because the form is basic forms.Form.
        # if the data came from forms.ModelForm then form.save() automatically cleans data.
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            body = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "email": form.cleaned_data["email_address"],
                "message": form.cleaned_data["message"],
                }
            message = "/n".join(body.values())

            try:
                # Django requires the format  send_mail to be ('subject', 'message', 'from_email', ['to_email']).
                # The from and to email addresses are both set to admin@example.com so the email will appear in the terminal for testing purposes.
                send_mail(subject, message, "jacksrecruitmentagency@email.com", ["jacksrecruitmentagency@email.com"])
            except BadHeaderError:
                # to prevent attackers from inserting email headers, we need to return a bad header error.
                return HttpResponse("Invalid header found")
            
            # if the form is submitted correctly, the user will be redirected to the home page.
            messages.success(request, "Thank you for contacting us. We will get back to you as soon as possible.")
            return redirect('home')

    # if the user simply requests to see the page, the empty form displays in the contact_us page.
    form = ContactUsForm()
    return render(request, "contact_us.html", {"form": form, "map_key": map_key})
