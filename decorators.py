from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(view_func):
      @wraps(view_func)
      def wrapper(request, *args, **kwargs):
           #  only admin users allowed
        if not request.user.is_superuser:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
      return wrapper