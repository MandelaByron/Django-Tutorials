from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from .managers import UserManager
import os
from PIL import Image
def get_random_filename(instance, filename):
    # Extract the file extension from the original filename
    ext = filename.split('.')[-1]
    
    # Generate a random filename with uuid
    random_filename = f"{uuid.uuid4()}.{ext}"
    
    # Return the full path, you can customize this path
    return os.path.join('profile-portraits/', random_filename)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(db_index = True, unique = True, editable=False , default = uuid.uuid4)
    
    first_name = models.CharField(max_length = 250)
    
    last_name = models.CharField(max_length = 250)
    
    avatar = models.ImageField(default='default.jpg', upload_to=get_random_filename)
    
    age = models.IntegerField(null=False, blank=False)

    email = models.EmailField(db_index=True, unique=True)
    
    is_staff = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default = True)
    
    is_superuser = models.BooleanField(default = False)
    
    
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age']
    
    objects = UserManager()
    
    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)

        # Open the image file
        img = Image.open(self.avatar.path)

        # Set the desired maximum size
        max_size = (300, 300)  # Example size (300x300px)

        # Check if the image needs resizing
        if img.height > 300 or img.width > 300:
            img.thumbnail(max_size)

            # Save the image back to the file system with the same path
            img.save(self.avatar.path)