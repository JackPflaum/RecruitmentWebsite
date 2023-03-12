from django import forms
from .models import Applied

class ContactUsForm(forms.Form):
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	email_address = forms.EmailField(max_length=255)
	subject = forms.CharField(max_length=255)
	message = forms.CharField(widget=forms.Textarea, max_length=2000)


class ApplicationForm(forms.ModelForm):
	covering_letter = forms.FileField(error_messages={'required': 'Please upload a non-empty file.'})

	class Meta:
		model = Applied
		fields = ['covering_letter']
