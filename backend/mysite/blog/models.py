from django.db import models
from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    reading_time = models.FloatField(default=0)


    class Meta:
        ordering = ['-published_date']


    def save(self, *args, **kwargs):
        #calculate reading time
        word_count = len(self.content.split())
        self.reading_time = round(word_count / 200, 2)
            
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
    
    #for counting words of the post
    def word_count(self):
        return len(self.content.split())
    
    #for calculate reading time
    def read_time(self):
        words = len(self.content.split())
        return round(words / 200, 2)
    
    #error raising
    def clean(self):
        super().clean()

        #title too short error
        if len(self.title) < 5:
            raise ValidationError("Title is too short! it must be at least 5 characters")
        

        # Title cannot be same as content
        if self.title.strip().lower() == self.content.strip().lower():
            raise ValidationError("Title and content cannot be same")
        
        #Prevent banned words
        forbidden = ["sex", "terrorism"]

        for word in forbidden:
            if word in self.content.lower():
                raise ValidationError("Your content contains inappropriate words")
            
            if word in self.title.lower():
                raise ValidationError("Your title contains inappropriate words")
            

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"Comment by {self.user.username}"