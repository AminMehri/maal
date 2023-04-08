from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from Financial.models import Withdraw
from Admin.permission import IsSuperUser, IsAdminUser, IsUnknownUser
from Account.models import Freelancer, Account
from Project.models import AcceptedProject
from Admin.models import Admin
from Ticket.models import Ticket
from Project.models import Project
import traceback


class AcceptWithdraw(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def post(self, request):
        try:
            id = request.data.get("id")
            user = request.user

            if Withdraw.objects.filter(id=id, is_paid=True).exists():
                return Response({"message": "این درخواست قبلا پرداخت شده است."}, status=status.HTTP_208_ALREADY_REPORTED)

            Withdraw.objects.filter(id=id).update(is_paid=True, paid_by=user, paid_at=timezone.now())

            return Response(status=status.HTTP_200_OK)

        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

class ShowFreelancers(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            lastShow = int(request.query_params.get("lastShow"))

            freelancers = Freelancer.objects.all().order_by('-created_at')[lastShow: lastShow + 9]

            data = []
            for freelancer in freelancers:
                data.append({
                    'account': freelancer.account.user.username,
                    'is_accepted': freelancer.is_accepted,
                    'verified_by': freelancer.verified_by.username,
                    'reject_reason': freelancer.reject_reason,
                })
            
            return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ShowFreelancerHistory(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            # TODO: lastShow
            id = int(request.query_params.get("id"))

            if not Freelancer.objects.filter(id=id).exists():
                return Response({"message": "کاربر مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

            freelancer = Freelancer.objects.get(id=id)
            projects = AcceptedProject.objects.filter(freelancer=freelancer).order_by("-accept_at")

            data = []
            for project in projects:
                data.append({
                    "project": project.project.title,
                    "freelancer": project.freelancer.account.user.username,
                    "pending": project.pending,
                    "price": project.price,
                    "followers": project.followers,
                    "following": project.following,
                    "engagement": project.engagement,
                })
            return Response({"data": data}, status=status.HTTP_200_OK)

        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AcceptFreelancer(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def post(self, request):
        try:
            id = request.data.get("id")
            user = request.user

            if not Freelancer.objects.filter(id=id).exists():
                return Response({"message": "کاربر مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
            
            Freelancer.objects.filter(id=id).update(is_accepted=True, verified_by=user, verified_time=timezone.now())

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RejectFreelancer(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def post(self, request):
        try:
            id = request.data.get("id")
            reject_reason = request.data.get("reject_reason")
            user = request.user

            if not Freelancer.objects.filter(id=id).exists():
                return Response({"message": "کاربر مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
            
            Freelancer.objects.filter(id=id).update(is_accepted=False, verified_by=user, reject_reason=reject_reason)
            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            



class ShowTickets(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        try:
            lastShow = int(request.query_params.get("lastShow"))

            tickets = Ticket.objects.all().order_by('-created_at')[lastShow: lastShow + 9]

            data = []
            for ticket in tickets:
                data.append({
                    'user': ticket.user.user.username,
                    'subject': ticket.subject,
                    'description': ticket.description,
                    'is_awnsered': ticket.is_awnsered,
                    'responsive_admin': ticket.responsive_admin.user.user.username if ticket.responsive_admin else None,
                })
            
            return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ShowProjects(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        try:
            lastShow = int(request.query_params.get("lastShow"))

            projects = Project.objects.all().order_by('-admin_confirmed')[lastShow: lastShow + 9]

            data = []
            for project in projects:
                data.append({
                    'owner': project.owner.user.username,
                    'admin_confirmed': project.admin_confirmed,
                    'confirmed_by': project.confirmed_by.user.user.username if project.confirmed_by else None,
                    'title': project.title,
                    'total_price': project.total_price,
                    'price': project.price,
                    'fee_percent': project.fee_percent,
                    'categories': project.categories,
                    'is_full': project.is_full,
                    'is_delete': project.is_delete,
                    'deleted_at': project.deleted_at,
                    'is_publish': project.is_publish,
                })
            return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ShowSingleProject(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        try:
            id = int(request.query_params.get("id"))

            if not Project.objects.filter(id=id).exists():
                return Response({'message': 'پروژه مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

            project = Project.objects.get(id=id)

            data = [{
                'owner': project.owner.user.username,
                'admin_confirmed': project.admin_confirmed,
                'confirmed_by': project.confirmed_by.user.user.username if project.confirmed_by else None,
                'title': project.title,
                'total_price': project.total_price,
                'price': project.price,
                'fee_percent': project.fee_percent,
                'categories': project.categories,
                'is_full': project.is_full,
                'is_publish': project.is_publish,
                'description': project.description,
                'files': project.files,
                'published_at': project.published_at,
                'created_at': project.created_at,
            }]
            return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ConfirmProject(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser) 

    def post(self, request):
        try:
            id = request.data.get("id")
            
            if not Project.objects.filter(id=id).filter(is_delete=False).exists():
                return Response({'message': 'پروژه مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)
            
            if not Project.objects.filter(id=id).filter(admin_confirmed=False).exists():
                return Response({'message': 'پروژه مورد نظر قبلا تایید شده است.'}, status=status.HTTP_423_LOCKED)

            account = Account.objects.get(user=request.user)
            admin = Admin.objects.get(user=account)

            Project.objects.filter(id=id).update(admin_confirmed=True, confirmed_by=admin, reject_reason='')

            return Response(status=status.HTTP_200_OK)

        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RejectProject(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser) 

    def post(self, request):
        try:
            id = request.data.get("id")
            reject_reason = request.data.get("reject_reason")
            
            if not Project.objects.filter(id=id).filter(is_delete=False).exists():
                return Response({'message': 'پروژه مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

            account = Account.objects.get(user=request.user)
            admin = Admin.objects.get(user=account)

            Project.objects.filter(id=id).update(admin_confirmed=False, confirmed_by=admin, reject_reason=reject_reason)

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
