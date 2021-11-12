from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

	class Meta:
		model = CustomUser
		fields = ('email', 'username', 'password1', 'password2', )

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = CustomUser.objects.exclude(pk=self.instance.pk).get(email=email)
		except CustomUser.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % CustomUser)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = CustomUser.objects.exclude(pk=self.instance.pk).get(username=username)
		except CustomUser.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)