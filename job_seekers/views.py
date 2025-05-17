from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, ProfileForm, JobForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import CustomUser, Profile, Job, Job_application

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from .decorators import restrict_to_employee

from django.core.paginator import Paginator

from django.http import StreamingHttpResponse
import requests
import json
import time

def home(request):
    
    user = request.user
    context = {'user':user}
    return render(request, 'base/home.html', context)


def login_page(request):
    # If already authenticated and role is employee, redirect to their home
    if request.user.is_authenticated and request.user.role == 'employee':
        return redirect('employee_home_page')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            if user.role == 'employee':
                login(request, user)
                # messages.success(request, 'You have logged in successfully, Make sure to update your profile in the profile link')
                if not user.has_seen_login_message:
                    messages.success(request, 'You have logged in successfully, Make sure to update your profile in the profile link')
                    user.has_seen_login_message = True
                    user.save()
                return redirect('employee_home_page')
                
            else:
                messages.error(request, 'Access denied: You are not registered as an employee.')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'base/login_page.html')
    
 
def register_page(request):
    if request.user.is_authenticated:
        return redirect('employee_home_page')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return render(request, 'partials/register_sweetalert.html')
      
        else:
            messages.error(request, 'An error occurred during registration')
    else:
        form = CustomUserCreationForm()        
    context = {'form': form}
    return render(request, 'base/register_page.html', context)  
 
 
@login_required(login_url='main_login')
@restrict_to_employee
def employee_home_page(request):
    if request.user.role == 'employer':  # Checking for 'employer' role
        return redirect('employer_home_page')
    
    q = request.GET.get('q', '')  # Default to empty string if no query
    
    # Search functionality
    if q:
        jobs = Job.objects.filter(title__icontains=q)
    else:
        jobs = Job.objects.all()

    # Pagination logic
    paginator = Paginator(jobs, 3)  # Show 6 jobs per page
    page = request.GET.get('page')
    jobs_page = paginator.get_page(page)

    context = {'jobs': jobs_page, 'q': q}
    return render(request, 'base/employee_home_page.html', context)


def register_sweetalert(request):
    
    context = {}
    return render(request, 'partials/register_sweetalert.html', context)

def logout_page(request):

        logout(request)
        messages.success(request, 'You have been logged out successfully!')
        return redirect('main_login')

        
@login_required(login_url='main_login')
@restrict_to_employee        
def job_details(request, user_id, job_id):
    
    user = CustomUser.objects.get(id=user_id)
    job = Job.objects.get(id=job_id)
    
    
    applied_jobs = Job_application.objects.filter(user=user, job=job).exists()
        
    print(applied_jobs)
    
    

    context = {'user': user, 'job': job, 'applied_jobs': applied_jobs}
    return render(request, 'base/job_details.html', context)



@login_required(login_url='main_login')
@restrict_to_employee
def job_details_apply(request, user_id, job_id):
    
    
    if request.method == 'POST':
        
        user = CustomUser.objects.get(id=user_id)
        job = Job.objects.get(id=job_id)
        
        job_application, created = Job_application.objects.get_or_create(user=user, job=job)
        
        applied_jobs = Job_application.objects.filter(user=user, job=job).exists()
        
        print(applied_jobs)
        messages.success(request, 'You have applied for the job successfully!')
        
    
    context = {'applied_jobs': applied_jobs}
    return render(request, 'partials/jobs_details_applied.html', context)


@login_required(login_url='main_login')
@restrict_to_employee
def applied_jobs(request):
    
    user = request.user
    applied_jobs = user.jobs_applied.all()
    
    # print('applied_jobs', applied_jobs)
    context = {'user': user, 'applied_jobs': applied_jobs}
    return render(request, 'base/applied_jobs.html', context)


@login_required(login_url='main_login')
@restrict_to_employee
def profile(request):
    
    user = request.user
    
    profile = Profile.objects.get(user=user)
    
    # form = ProfileForm()
    
     # return redirect('employee_home_page')
        
        
    context = {'user': user, 'profile': profile}
    
    return render(request, 'base/profile.html', context)


@login_required(login_url='main_login')
@restrict_to_employee
def profile_swap(request, id):
    
    user = CustomUser.objects.get(id=id)
    profile = Profile.objects.get(user=user)
    
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
            
    context = {'user': user, 'profile': profile, 'form': form}
    return render(request, 'partials/profile_swap.html', context)




def main_login(request):
    
    return render(request, 'base/main_login.html')

# AI CHAT INTEGRATION

@login_required(login_url='main_login')
def chat_with_ai(request):
    
    return render(request, 'base/chat_with_ai.html')


def get_user_response(request):
    data = json.loads(request.body)
    user_input = data['userInput']
    print(user_input)
    
    url = 'http://localhost:11434/api/generate'
    
    ai_api = {
        'model': 'gemma:2b',
        'prompt': user_input,
        'stream': True
    }
    
    response = requests.post(url, json=ai_api, stream=True)

    def event_stream():
        print('\nAI response:', end='', flush=True)

        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode('utf-8'))
                    result = json_data.get('response', '')
                    yield result + " "  # Yield each response chunk
                    time.sleep(0.2)  # Small delay to simulate real-time response
                    print(result, end='', flush=True)

                except json.JSONDecodeError:
                    yield 'Error: Could not decode JSON response'
                    break

    return StreamingHttpResponse(event_stream(), content_type='text/plain')



































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































