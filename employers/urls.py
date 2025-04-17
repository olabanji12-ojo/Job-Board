from django.urls import path
from .import views 

urlpatterns = [
    
    path('employer_home_page/', views.employer_home_page, name='employer_home_page'),
    path('employer_login_page/', views.employer_login_page, name='employer_login_page'),
    
    path('create_jobs/', views.create_jobs, name='create_jobs'),
    path('edit_jobs/<int:id>/', views.edit_jobs, name='edit_jobs'),
    
    path('account_page/', views.account_page, name='account_page'),
    
    path('view_applicants/', views.view_applicants, name='view_applicants'),
    
    path('applicants_profile/<int:id>/', views.applicants_profile, name='applicants_profile'),
    
    path('accept_applicant/<int:user_id>/<int:job_id>/', views.accept_applicant, name='accept_applicant'),
    
    path('delete_jobs/<int:id>/', views.delete_jobs, name='delete_jobs'),
    
]   

 