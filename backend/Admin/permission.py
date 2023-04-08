from rest_framework.permissions import BasePermission, SAFE_METHODS
from Account.models import Account
from Admin.models import Admin



# نکته اینه ک اگه طرف کلن ادمین نباشه ۵۰۰ برمیگردونه
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        account = Account.objects.get(user=request.user)
        if not Admin.objects.filter(user=account).exists():
            return False
        admin = Admin.objects.get(user=account)
        self.message = 'This does not fit you'
        return bool(request.user and admin.admin_rule == 'superuser')



class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        account = Account.objects.get(user=request.user)
        if not Admin.objects.filter(user=account).exists():
            return False
        admin = Admin.objects.get(user=account)
        return bool(request.user and (admin.admin_rule == 'admin' or admin.admin_rule == 'superuser'))
    


class IsUnknownUser(BasePermission):
    def has_permission(self, request, view):
        account = Account.objects.get(user=request.user)
        if not Admin.objects.filter(user=account).exists():
            return False
        admin = Admin.objects.get(user=account)
        return bool(request.user and (admin.admin_rule == 'unknown' or admin.admin_rule == 'admin' or admin.admin_rule == 'superuser'))