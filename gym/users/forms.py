from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser

class MyCustomSignupForm(SignupForm):
    
    first_name = forms.CharField(max_length=250, label='First Name')
    
    last_name = forms.CharField(max_length=250, label='Last Name')
    
    age = forms.IntegerField(label='Age')
   
    
    def save(self, request):

        user = super(MyCustomSignupForm, self).save(request)

        return user
    
class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        
        fields = ['age', 'avatar' , 'first_name' , 'last_name']