from app import create_app
from extensions import db
from app.models.user import UserTable
from app.models.role import RoleTable

app = create_app()

with app.app_context():
    user = UserTable.query.filter_by(username="Palolol").first()
    admin_role = RoleTable.query.filter_by(name="Admin").first()

    if not user:
        print("❌ User 'Palolol' not found")
    elif not admin_role:
        print("❌ Admin role not found")
    elif admin_role in user.roles:
        print("⚠ User already has Admin role")
    else:
        user.roles.append(admin_role)
        db.session.commit()
        print("✅ Admin role assigned to Palolol")
