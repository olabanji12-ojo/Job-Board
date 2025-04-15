from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def restrict_to_employer(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check the role directly on the user
        if request.user.role != 'employer':
            # Add a message to inform the user
            messages.error(request, "You do not have permission to view this page.")
            # Redirect to a safe page (home page or any other page)
            return redirect('employee_home_page')  # or 'some_view_name'
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def restrict_to_employee(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check the role directly on the user
        if request.user.role != 'employee':
            # Add a message to inform the user
            messages.error(request, "You do not have permission to view this page.")
            # Redirect to a safe page (home page or any other page)
            return redirect('employer_home_page')  # or 'some_view_name'
        return view_func(request, *args, **kwargs)
    return _wrapped_view
