from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from django.contrib import messages
from job_seekers.models import CustomUser, Profile, Job, Job_application

from job_seekers.forms import JobForm
from job_seekers.decorators import restrict_to_employee, restrict_to_employer
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse

from job_seekers.signals import notify_job_seeker

@login_required(login_url='employer_login_page')
@restrict_to_employer
def employer_home_page(request):
    if request.user == 'employee':
        return redirect('employee_home_page')
    
    q = request.GET.get('q')
    if q is not None:
        
        jobs = Job.objects.filter(title__icontains=q)
    else:
        q = ''
        jobs = Job.objects.all()
        
    paginator = Paginator(jobs, 3)
    page = request.GET.get('page')
    jobs_page = paginator.get_page(page)
    
    context = {'jobs': jobs_page, 'q': q}
    
    return render(request, 'emp/employer_home_page.html', context)



def employer_login_page(request):
    # Redirect if already logged in as an employer
    if request.user.is_authenticated and request.user.role == 'employer':
        return redirect('employer_home_page')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.role == 'employer':
                login(request, user)
                return redirect('employer_home_page')
            else:
                messages.error(request, 'Access denied: You are not registered as an employer.')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'emp/employer_login_page.html')


@login_required(login_url='employer_login_page')
@restrict_to_employer
def create_jobs(request):
    
    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('employer_home_page')
    context = {'form': form}
    return render(request, 'emp/create_jobs.html', context)


@login_required(login_url='employer_login_page')
@restrict_to_employer
def edit_jobs(request, id):
    job = Job.objects.get(id=id)
    form = JobForm(instance=job)
    
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employer_home_page')
            
    context = {'job': job, 'form': form}
    return render(request, 'emp/create_jobs.html', context)
 
 
@login_required(login_url='employer_login_page')
@restrict_to_employer 
def delete_jobs(request, id):
    
    if request.method == 'POST':
        job = Job.objects.get(id=id)
        if job.employer != request.user:
            return HttpResponseForbidden("You are not allowed to delete this job.")
        job.delete()
        messages.success(request, 'Job deleted successfully')
    response = HttpResponse()
    response["HX-Redirect"] = reverse("employer_home_page")
    return response    
        
        
@login_required(login_url='employer_login_page')
@restrict_to_employer
def account_page(request):
    
    context = {}
    return render(request, 'emp/account_page.html', context) 


@login_required(login_url='employer_login_page')
@restrict_to_employer
def view_applicants(request):
    
    employer = request.user
    
    employer_jobs = Job.objects.filter(employer=employer)
    
    job_applications = Job_application.objects.filter(job__in=employer_jobs)
    
    context = {'employer': employer, 'job_applications': job_applications}
    return render(request, 'emp/view_applicants.html', context)
 

@login_required(login_url='employer_login_page')
@restrict_to_employer
def applicants_profile(request, id):
    user = CustomUser.objects.get(id=id)
    job_application = Job_application.objects.get(user=user)
    profile = Profile.objects.get(user=job_application.user)
    
    job = job_application.job
    
    context = {'user': user, 'profile': profile, 'job':job, 'job_application': job_application}
    return render(request, 'emp/applicants_profile.html', context)


@login_required(login_url='employer_login_page')
@restrict_to_employer
def accept_applicant(request, user_id, job_id):
    user = CustomUser.objects.get(id=user_id)
    job = Job.objects.get(id=job_id)
    
    
    job_application = Job_application.objects.get(user=user, job=job)
    
    if request.method == 'POST':
        job_application.status = "accepted"
        job_application.save()
        # notify_job_seeker(job_application.user, job_application.job.company, job_application.job.title)
    
        # messages.success(request, "Job seeker has been notified via email.")

    
    context = {'user':user, 'job': job, 'job_application':job_application}
    return render(request, 'partials/accept_applicant.html', context)



# Create your views here.
