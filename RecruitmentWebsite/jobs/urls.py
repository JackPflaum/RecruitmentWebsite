from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('job_positions/', views.job_positions, name='job_positions'),
    path('job_details/<int:id>', views.job_details, name='job_details'),
    path('application_confirmed/<int:id>', views.application_confirmed, name='application_confirmed'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('email_confirmed/', views.email_confirmed, name='email_confirmed'),
]