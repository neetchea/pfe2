from django.shortcuts import render
import logging

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                user_groups = request.user.groups.all()
                logging.info(f"User's groups: {[group.name for group in user_groups]}")
                logging.info(f"Allowed roles: {allowed_roles}")
                for group in user_groups:
                    if group.name in allowed_roles:
                        return view_func(request, *args, **kwargs)

            # Pass user type to the template
            context = {
                'user': request.user
            }
            return render(request, 'core/403.html', context)
        return wrapper_func
    return decorator















# from django.shortcuts import render

# def allowed_users(allowed_roles=[]):
#     def decorator(view_func):
#         def wrapper_func(request, *args, **kwargs):
#             if request.user.groups.exists():
#                 user_groups = request.user.groups.all()
#                 for group in user_groups:
#                     if group.name in allowed_roles:
#                         return view_func(request, *args, **kwargs)

#             # Pass user type to the template
#             context = {
#                 'user': request.user
#             }
#             return render(request, 'core/acces_interdit.html', context)
#         return wrapper_func
#     return decorator
