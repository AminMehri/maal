from rest_framework.permissions import BasePermission, SAFE_METHODS
from Account.models import Account, Freelancer
from Admin.models import Admin



# نکته اینه ک اگه طرف کلن ادمین نباشه ۵۰۰ برمیگردونه
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        self.message = 'شما قابلیت دسترسی به این بخش را ندارید.'
        if not Admin.objects.filter(user__user=request.user).exists():
            return False
        admin = Admin.objects.get(user__user=request.user)
        return bool(request.user and admin.admin_rule == 'superuser')



class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        self.message = 'شما قابلیت دسترسی به این بخش را ندارید.'
        if not Admin.objects.filter(user__user=request.user).exists():
            return False
        admin = Admin.objects.get(user__user=request.user)
        return bool(request.user and (admin.admin_rule == 'admin' or admin.admin_rule == 'superuser'))
    


class IsUnknownUser(BasePermission):
    def has_permission(self, request, view):
        self.message = 'شما قابلیت دسترسی به این بخش را ندارید.'
        if not Admin.objects.filter(user__user=request.user).exists():
            return False
        admin = Admin.objects.get(user__user=request.user)
        return bool(request.user and (admin.admin_rule == 'unknown' or admin.admin_rule == 'admin' or admin.admin_rule == 'superuser'))



class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        self.message = "تنها فریلنسر ها اجازه دسترسی به این قسمت را دارند. در صورتی که درخواست فریلنسری خود را ثبت کرده اید لطفا تا تایید آن منتظر بمانید."
        if not Freelancer.objects.filter(account__user=request.user).exists():
            return False
        freelancer = Freelancer.objects.get(account__user=request.user)
        return bool(request.user and freelancer.is_accepted == True)
