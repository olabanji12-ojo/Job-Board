from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    
    ROLE_CHOICES = {
        ('employee', 'Employee'),
        ('employer', 'Employer'),
    }
    
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'role']
    
    def __str__(self):
        return self.name
   
class Profile(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    skills = models.CharField(max_length=200, null=True, blank=True)
    CV = models.FileField(null=True, blank=True)
    profile_picture = models.ImageField(default='download.jpg', upload_to='static/images', null=True, blank=True)
    education = models.CharField(max_length=200, null=True, blank=True)
    
    
    def __str__(self):
        return self.user.name
    
    
class Job(models.Model):
    
    job_logo = models.ImageField(default='download.jpg', upload_to='static/images', null=True, blank=True)

    title = models.CharField(max_length=255)
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applied_jobs', null=True, blank=True)
    description = models.TextField()
    company_name = models.CharField(max_length=100)
    company_details = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    
        
class Job_application(models.Model):
    
    STATUS_CHOICES = [
        
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='jobs_applied')    
    job = models.ForeignKey(Job, null=True, blank=True, on_delete=models.CASCADE, related_name='job_applications')
 
    
    
    def __str__(self):
        return f'{self.user} --- {self.job} -- {self.status}'
    
    
# Create your models here.
