from django.urls import path
from .import views


urlpatterns = [
    
    path('', views.home, name='home'),
    path('login_page/', views.login_page, name='login_page'),
    path('register_page/', views.register_page, name='register_page'),
    path('employee_home_page/', views.employee_home_page, name='employee_home_page'),
    path('logout_page/', views.logout_page, name='logout_page'),
    
    
    path('job_details/<int:user_id>/<int:job_id>', views.job_details, name='job_details'),
    
    path('job_details_apply/<int:user_id>/<int:job_id>', views.job_details_apply, name='job_details_apply'),
    
    path('applied_jobs/', views.applied_jobs, name='applied_jobs'),
    
    path('profile/', views.profile, name='profile'),
    
    path('chat_with_ai/', views.chat_with_ai, name='chat_with_ai'),
    
    
    # SWEET ALERTS
    path('register_sweetalert/', views.register_sweetalert, name='register_sweetalert'),
    path('profile_swap/<int:id>/', views.profile_swap, name='profile_swap'),
    
    path('get_user_response/', views.get_user_response, name='get_user_response'),
    
    path('main_login/',views.main_login, name='main_login'),
        
]


