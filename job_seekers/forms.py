from django import forms
from .models import CustomUser, Job, Profile
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email', 'role', 'password1', 'password2']

        widgets = {
            'username' : forms.TextInput(attrs={'placeholder': 'Enter username...'}),
            'email' : forms.EmailInput(attrs={'placeholder': 'Enter email...'}),
            'password1' : forms.PasswordInput(attrs={'placeholder': 'Enter password...'}),
            'password2' : forms.PasswordInput(attrs={'placeholder': 'Confirm password...'})
        }
        
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for formfield in ['username', 'email', 'password1', 'password2']:
            self.fields[formfield].help_text = ''


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['skills', 'CV', 'profile_picture']
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'    
            
            

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_logo', 'title', 'description', 'company_name', 'company_details', 'location']
        
    # def __init__(self, *args, **kwargs):
    #     super(JobForm, self).__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs['class'] = 'form-control'    
        
        
