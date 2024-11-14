from django.db import models
from django.conf import settings
from tinymce import models as tinymce_models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
import os
import uuid
def get_random_filename(instance, filename):
    # Extract the file extension from the original filename
    ext = filename.split('.')[-1]
    
    # Generate a random filename with uuid
    random_filename = f"{uuid.uuid4()}.{ext}"
    
    # Return the full path, you can customize this path
    return os.path.join('blog-portraits/', random_filename)

class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status = Blog.Status.PUBLISHED)
    
class Blog(models.Model):
    
    class Status(models.TextChoices):
         DRAFT = 'DF', 'Draft'
         PUBLISHED = 'PB', 'Published'
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    
    tags = TaggableManager()
    
    title = models.CharField(max_length=255)
    
    content = tinymce_models.HTMLField()
    
    publish = models.DateTimeField(default=timezone.now)
    
    #the date will be saved automatically when creating an object.
    dateCreated = models.DateTimeField(auto_now_add=True)
    
    #the date will be updated automatically when saving an object.
    updated = models.DateTimeField(auto_now=True)
    #image = models.ImageField(upload_to='images/',null=True, blank=True)
    
    category = models.CharField(max_length=25,default='Workout')
    
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    
    status = models.CharField(max_length=2,choices=Status.choices, default=Status.DRAFT)
    
    view_count = models.PositiveIntegerField(default=0)
    
    thumbnail = models.ImageField(default='default_thumbnail.jpg', upload_to=get_random_filename)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

        
    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})
    
    
    def __str__(self):
        return self.title

    class Meta:
        
        ordering = ['-updated','-publish']
        indexes = [
            models.Index(fields=['-publish']),
            ]
        
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.