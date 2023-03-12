from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import ContactUsForm, ApplicationForm
from .models import JobPositions
from accounts.views import login_user


def home(request):
    return render(request, 'home.html', {})


def job_positions(request):
    jobs = JobPositions.objects.all().order_by('posted')
    context = {'jobs': jobs}
    return render(request, 'job_positions.html', context)


def job_details(request, id):
    job = JobPositions.objects.get(id=id)
    form = ApplicationForm()
    context = {'job': job, 'apply_form': form}
    return render(request, 'job_details.html', context)


def application_confirmed(request, id):
    job = JobPositions.objects.get(id=id)
    context = {'job': job}
    return render(request, 'application_confirmed.html', context)


def about_us(request):
    return render(request, 'about_us.html', {})


def contact_us(request):
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
