from django import forms

class SignupForm(forms.Form):
    firstname = forms.CharField(label="First Name",max_length=225)
    lastname = forms.CharField(label="Last Name",max_length=225)
    username = forms.CharField(label="Username",max_length=225)
    email = forms.EmailField(label="Email",max_length=225)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username",max_length=225)
    password = forms.CharField(widget=forms.PasswordInput)