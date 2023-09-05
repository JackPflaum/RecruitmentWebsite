from django.urls import path
from . import views as accounts_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', accounts_views.register_user, name='register'),
    path('login/', accounts_views.login_user, name='login'),
    path('logout/', accounts_views.logout_user, name='logout'),
    path('profile/<slug:slug>', accounts_views.user_profile, name='user_profile'),
    path('update', accounts_views.update_profile, name='update_profile'),

    path('reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html',
    email_template_name='registration/password_reset_email.html',
    subject_template_name='registration/password_reset_subject.txt'), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
    name='password_reset_done'),    

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
    name="password_reset_confirm"),

    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
    name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # serves uploaded media files during development