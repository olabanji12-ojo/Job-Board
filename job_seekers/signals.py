from .models import CustomUser, Profile, Job_application, Job, Employer_Account
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.core.mail import send_mail, EmailMessage
from django.conf import settings


@receiver(post_save, sender=CustomUser)    
def create_profile(sender, instance, created, **kwargs):
    user = instance
    if created and user.role == 'employee':
        profile = Profile.objects.create(
            user=user
        )
        print('Profile created')
        subject = "🎉 Welcome to Emmanuel's Job Board Application!"

        message = f"""
        Hi {user.username},

        We're thrilled to have you join Emmanuel's Job Board – a growing platform built to help individuals like you find meaningful opportunities, build your career, and connect with potential employers.

        Here’s what you can look forward to:
        🔹 Creating your professional profile  
        🔹 Exploring job listings across different fields  
        🔹 Applying to roles that match your skills  
        🔹 Connecting with companies looking for talent like you

        This is just the beginning — we’re excited to see where this journey takes you!

        If you ever have questions, feedback, or need support, feel free to reply to this email and we’ll be glad to help.

        Warm regards,  
        Emmanuel & The Team  
        """

        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            reply_to=[settings.EMAIL_HOST_USER],
        )
        email.send(fail_silently=False)

    elif created and user.role == 'employer':
        employer = Employer_Account.objects.create(
            user=user
        )
        print('Employer Account created')
        subject = "👋 Welcome to Emmanuel's Job Board – Employer Dashboard"

        message = f"""
        Hello {user.username},

        Welcome aboard! We’re excited to have you as a part of Emmanuel's Job Board – a platform created to help you discover and connect with talented individuals looking to grow their careers.

        As an employer, here’s what you can now do:
        🔹 Set up your company/employer profile  
        🔹 Post job listings to attract top candidates  
        🔹 Review and manage applications with ease  
        🔹 Connect with potential employees and grow your team

        Thank you for choosing Emmanuel's Job Board. We're committed to supporting you in building strong, talented teams.

        Questions? Need help? Just reply to this email – we’re here for you.

        Best regards,  
        Emmanuel & The Team  
        """

        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            reply_to=[settings.EMAIL_HOST_USER],
        )
        email.send(fail_silently=False)
        


@receiver(post_delete, sender=CustomUser)        
def delete_profile(sender, instance, **kwargs):
    user = instance
    instance.profile.delete() 
    print('CustomUser associated with Profile has been deleted')
    
@receiver(post_save, sender=Job_application)    
def notify_job_seeker(sender, instance, created, **kwargs):
    job_application = instance
    if created == False and instance.status == 'accepted':
        job_seeker = job_application.user
        job = job_application.job
        subject = f"🎉 Your application for '{job.title}' has been accepted!"
        
        message = f"""
        Hi {job_seeker.name},

        Great news! Your application for the position '{job.title}' has been accepted by {job.company_name}.

        They might reach out to you soon — so keep an eye on your inbox or dashboard.

        Wishing you all the best!

        – Emmanuel's Job Board Team
        """
        
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [job_seeker.email],
            reply_to=[job.employer.email]
        )
        email.send()
    