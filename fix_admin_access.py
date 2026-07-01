"""
Script to fix admin access for superadmin user.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ging_profile_v2.settings')
django.setup()

from users.models import User

def fix_admin_access():
    try:
        user = User.objects.get(username='superadmin')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"✓ Admin access enabled for '{user.username}'")
        print(f"  is_staff: {user.is_staff}")
        print(f"  is_superuser: {user.is_superuser}")
    except User.DoesNotExist:
        print("✗ User 'superadmin' does not exist")

if __name__ == '__main__':
    fix_admin_access()
