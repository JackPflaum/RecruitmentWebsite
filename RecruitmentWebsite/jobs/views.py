from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import ContactUsForm, ApplicationForm
from .models import JobPositions, Applied
from accounts.views import login_user
from datetime import date


def home(request):
    return render(request, 'home.html', {})


def job_positions(request):
    """user can view all jobs that are available"""
    jobs = JobPositions.objects.all().order_by('posted')
    context = {'jobs': jobs}
    return render(request, 'job_positions.html', context)


def job_details(request, id):
    """user can view job details and apply for job"""
    job = get_object_or_404(JobPositions, id=id)

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
    applied = Applied.objects.filter(job=job, applicant=request.user.id).exists()

    context = {'job': job, 'apply_form': form, 'user': request.user, 'applied': applied}
    return render(request, 'job_details.html', context)


def application_confirmed(request, id):
    """confirm user has applied for job"""
    job = get_object_or_404(JobPositions, id=id)
    context = {'job': job}
    return render(request, 'application_confirmed.html', context)


def about_us(request):
    return render(request, 'about_us.html', {})


def contact_us(request):
    """company contact information and contact form"""
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
            # if the form is submitted correctly, the user will be redirected to the message_confirmed page.
            return redirect("email_confirmed")

    # if the user simply requests to see the page, the empty form displays in the contact_us page.
    form = ContactUsForm()
    return render(request, "contact_us.html", {"form": form})


def email_confirmed(request):
    return render(request, 'email_confirmed.html', {})
