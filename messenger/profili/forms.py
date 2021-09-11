from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from profili.models import Account

# FŠorma za registraciju
class RegistreationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Email required.")

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

    #Provjerava valjanost emaila
    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")

    #Provjerava valjanost usernamea
    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")

# Forma za login
class LoginForm(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    # Cisti podatke u formi
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email = email, password = password):
                raise forms.ValidationError("Invalide login")    

