# from django.http import HttpResponse
# from django.shortcuts import redirect
# from django.contrib import messages

# def login_required(view_fun):
#     def wrapper_fun(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return view_fun(request, *args, **kwargs)
#         else:
#             messages.warning(request,"Login required...")
#             return redirect('dashboard:login')
#     return wrapper_fun



from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

from functools import wraps


def login_required(view_fun):
    def wrapper_fun(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_fun(request, *args, **kwargs)
        else:
            messages.warning(request,"Login required...")
            return redirect('dashboard:login')
    return wrapper_fun




def user_role_required(role):
    def decorator(view_func):
        def wrapper(self, request, *args, **kwargs):
            if request.user.is_authenticated and getattr(request.user,f'is_{role}'):
                return view_func(self, request, *args, **kwargs)
            else:
                messages.warning(request, f"{role.capitalize()} login required...")
                return redirect('dashboard:login')
        return wrapper
    return decorator





def admin_and_agent_required(view_func):
    @wraps(view_func)
    def decorator(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_agent or request.user.is_sub_admin):
            return view_func(self, request, *args, **kwargs)
        else:
            messages.warning(request, "Admin or Agent login required...")
            return redirect('dashboard:login')
    return decorator

# def admin_and_vendor_required(view_func):
#     @wraps(view_func)
#     def decorator(self, request, *args, **kwargs):
#         if request.user.is_authenticated and (request.user.is_admin or request.user.is_vendor):
#             return view_func(self, request, *args, **kwargs)
#         else:
#             messages.warning(request, "Admin or vendor login required...")
#             return redirect('dashboard:login')
#     return decorator

def all_users_required(view_func):
    @wraps(view_func)
    def decorator(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(self, request, *args, **kwargs)
        else:
            messages.warning(request, "Login required...")
            return redirect('dashboard:login')
    return decorator


def user_role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and getattr(request.user, f'is_{role}'):
                return view_func(request, *args, **kwargs)
            else:
                messages.warning(request, f"{role.capitalize()} login required...")
                return redirect('dashboard:login')
        return wrapper
    return decorator


def admin_and_agent_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_agent or request.user.is_sub_admin):
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, "Admin or agent login required...")
            return redirect('dashboard:login')
    return wrapper

# def admin_and_vendor_required(view_func):
#     @wraps(view_func)
#     def wrapper(request, *args, **kwargs):
#         if request.user.is_authenticated and (request.user.is_admin or request.user.is_vendor):
#             return view_func(request, *args, **kwargs)
#         else:
#             messages.warning(request, "Admin or vendor login required...")
#             return redirect('dashboard:login')
#     return wrapper

def all_users_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, "Login required...")
            return redirect('dashboard:login')
    return wrapper