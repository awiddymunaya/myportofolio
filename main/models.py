import uuid
from django.db import models
from django.contrib.auth.models import User # Mengimpor model User bawaan Django

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    
    # FITUR BARU: Relasi Bintang (Star) ke model User
    stars = models.ManyToManyField(User, related_name='starred_experiences', blank=True)
    
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None
        
    @property
    def total_stars(self):
        return self.stars.count()


class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.CharField(max_length=50)
    institution_name = models.CharField(max_length=255)
    start_year = models.IntegerField() 
    end_year = models.CharField(max_length=20) 
    description = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"{self.level} - {self.institution_name}"