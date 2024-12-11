from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
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
    def get_queryset(self):
        return super().get_queryset().filter(status = Blog.Status.PUBLISHED)

class Blog(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF" , "DRAFT"
        
        PUBLISHED = "PB", "PUBLISHED"
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts")        
    
    tags = TaggableManager() #name, slug
    
    title = models.CharField(max_length=255)
    
    content = models.TextField()
    
    category = models.CharField(max_length=25, default="Workout")
    
    dateCreated = models.DateTimeField(auto_now_add=True) #the date will be saved automatically when creating an object.
    
    #the date will be updated automatically when saving an object.
    updated = models.DateTimeField(auto_now=True)
    
    viewCount = models.PositiveIntegerField(default=0)
    
    slug = models.SlugField(unique=True, blank=True, max_length=250)
            
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    
    thumbnail = models.ImageField(default='default_thumbnail.jpg', upload_to=get_random_filename)
    
    def get_absolute_url(self):
        return reverse(viewname='blog-detail', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        super().save(*args, **kwargs)
        
    class Meta:
        indexes = [
            models.Index(fields=['updated'])
        ]
        
        ordering = ["-dateCreated"]
    
    def __str__(self):
        return self.title
    
    objects = models.Manager() #Blog.objects.all() -> QuerySet
    published = PublishedManager() # Our custom manager
#Blog.objects.all() -> QuerySet
    