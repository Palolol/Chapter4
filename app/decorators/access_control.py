from functools import wraps 
from flask import flash, redirect, url_for, abort
from flask_login import current_user

def role_required(roles):
    """
    Decorator to restrict access based on user roles.
    
    Usage:
        @role_required(['Admin', 'Expert])
        def admin_only_route():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is logged in
            if not current_user.is_authenticated:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for("auth.login"))
            
            # Check if user has any of the required roles
            if not current_user.has_any_role(roles):
                flash("You don't have permission to access this page.", "danger")
                abort(403) #Forbidden
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def permission_required(permission_name):
    """
    Decorator to restrict access based on specific permission.
    
    Usage:
        @permission_required('delete_users')
        def delete_user_route():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for("auth.login"))
            
            if not current_user.has_permission(permission_name):
                flash(f"You need '{permission_name}' permission to access this.", "danger")
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """
    Shortcut decorator for admin-only routes.
    
    Usage:
        @admin_required
        def admin_panel():
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in.", "warning")
            return redirect(url_for("auth.login"))
        
        if not current_user.is_admin():
            flash("Admin access required.", "danger")
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def owner_or_admin_required(get_resource_owner_id):
    """
    Allow access only to resource owner or admin.
    
    Usage:
        @owner_or_admin_required(lambda: diagnosis.user_id)
        def view_diagnosis(id):
            diagnosis = DiagnosisTable.query.get_or_404(id)
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            
            # Execute the lambda or function to get owner_id
            owner_id = get_resource_owner_id() if callable(get_resource_owner_id) else get_resource_owner_id
            
            # Allow if admin or owner
            if not (current_user.is_admin() or current_user.id == owner_id):
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator