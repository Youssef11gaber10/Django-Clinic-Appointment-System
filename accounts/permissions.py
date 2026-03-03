from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from functools import wraps


def require_role(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in roles:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied("You do not have permission to access this page.")
        return wrapper
    return decorator


def user_has_role(user, *roles):
    return user.role in roles


def user_has_permission(user, perm):
    return user.has_perm(perm)


PATIENT_PERMS = [
    'accounts.view_userapp',
    'accounts.change_userapp',
    'appointments.view_appointment',
    'medical.view_consultation',
    'medical.view_requestedtest',
    'medical.view_prescriptoinitem',
]

DOCTOR_PERMS = [
    'accounts.view_userapp',
    'accounts.change_userapp',
    'accounts.view_doctorprofile',
    'accounts.change_doctorprofile',
    'appointments.view_appointment',
    'appointments.change_appointment',
    'scheduling.view_slot',
    'scheduling.add_slot',
    'scheduling.change_slot',
    'scheduling.delete_slot',
    'scheduling.view_availability',
    'scheduling.add_availability',
    'scheduling.change_availability',
    'scheduling.delete_availability',
    'medical.add_consultation',
    'medical.change_consultation',
    'medical.view_consultation',
    'medical.add_prescriptoinitem',
    'medical.change_prescriptoinitem',
    'medical.view_prescriptoinitem',
    'medical.add_requestedtest',
    'medical.view_requestedtest',
]

RECEPTIONIST_PERMS = [
    'accounts.view_userapp',
    'appointments.view_appointment',
    'appointments.change_appointment',
    'scheduling.view_slot',
    'medical.view_consultation',
]

ADMIN_PERMS = [
]
