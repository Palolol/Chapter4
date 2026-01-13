from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.user import UserTable
from app.models.role import RoleTable

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
@login_required
def index():
    total_users = UserTable.query.count()
    total_admins = UserTable.query.join(UserTable.roles).filter(RoleTable.name == "Admin").count()

    return render_template(
        "users/dashboard.html",
        total_users=total_users,
        total_admins=total_admins,
        current_user=current_user,
    )
