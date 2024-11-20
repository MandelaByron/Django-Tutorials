from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    first_name  = forms.CharField(max_length=250, label='First Name')
    
    last_name  = forms.CharField(max_length=250, label='Last Name')
    
    age = forms.IntegerField(label="Age")
    
    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        return user