from allauth.account.adapter import DefaultAccountAdapter

class MyAdapter(DefaultAccountAdapter):
    
    def save_user(self, request, user, form, commit=True):
        
        data = form.cleaned_data

        user.first_name=data['first_name']
        user.last_name=data['last_name']
        user.age=data['age']
        user.email=data['email']
        
        if "password1" in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password() #This method ensures that the user object has a password value that cannot be used to log in
            
        user.save()
        return user        