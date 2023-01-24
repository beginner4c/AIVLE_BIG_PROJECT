from django import forms
from . import models
class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            "username",
            "name",
            "email",
            "phone",
        )
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password
   
    def save(self, *args, **kwargs): 
        user = super().save(commit=False)
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        
        user.username = username
        user.email = email
        user.set_password(password) 
        user.save() 