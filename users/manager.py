from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    #create_user, create_superuser
    def create_user(self, email, first_name, last_name, age, password=None, **extra_fields):
        
        if email is None:
            raise ValueError("Email field is required")
        
        if first_name is None:
            raise ValueError("First Name field is required")
        
        if last_name is None:
            raise ValueError("Last Name field is required")
        
        if age is None:
            raise ValueError("Age field is required")
        
        email = self.normalize_email(email)
        
        user = self.model(email=email, first_name=first_name, last_name=last_name, age=age, **extra_fields)
        
        user.set_password(password)
        
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, first_name, last_name, age, password=None, **extra_fields):
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        return self.create_user(email=email, first_name=first_name, last_name=last_name, age=age, password=password,**extra_fields)
        