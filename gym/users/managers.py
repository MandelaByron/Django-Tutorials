from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.forms import ValidationError

class UserManager(BaseUserManager):
    
    def get_object_by_public_id(self, public_id):
        
        try:
            instance = self.get(public_id)
            
            return instance
        except ObjectDoesNotExist:
            
            raise Http404("User with the ID Doesn't exist")
        
        except (ValueError, TypeError, ValidationError):
            raise Http404('Invalid Public Id')
            
    def create_user(self, email, first_name, last_name,age,password=None,**extra_fields):
        
        if email is None:
            raise ValueError('Email is required')
        
        if first_name is None:
            raise ValueError('First Name is required')
        
        if last_name is None:
            raise ValueError('Last Name is required')

        if age is None:
            raise ValueError('Age is required')       
        
        email = self.normalize_email(email)
        
        
        user = self.model(email=email, first_name=first_name, last_name=last_name, age=age, **extra_fields)
        
        user.set_password(password)
        
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, first_name, last_name , age, password = None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email=email, first_name=first_name, last_name=last_name, age=age, password=password, **extra_fields)
    
    