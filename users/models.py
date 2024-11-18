from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from .manager import UserManager

class Users(AbstractBaseUser, PermissionsMixin):
    
    public_id = models.UUIDField(unique=True, editable=False, db_index=True, default=uuid.uuid4)

    first_name = models.CharField(max_length=250)
    
    last_name = models.CharField(max_length=250)
        
    email = models.EmailField(unique=True, db_index=True)
    
    age = models.PositiveIntegerField(null=False, blank=False)
    
    is_staff = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age']
    
    objects = UserManager()
    
    