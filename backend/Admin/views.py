from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Account.models import Freelancer, Account
from Admin.permission import IsSuperUser, IsAdminUser, IsUnknownUser, IsFreelancer
from Admin.models import Admin
from Financial.models import Withdraw
from Project.models import Project, AcceptedProject
from Ticket.models import Ticket, Conversation, AdminAnswer
from Ticket.serializers import AddTicketSerializer
from datetime import datetime
from itertools import chain
import traceback


def error_text(error_obj):
    text = "مقادیر نادرست برای:"
    for field, reason in error_obj.items():
        text += f"\n{field}: {reason[0]}"
    return text



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
    permission_classes = (IsAuthenticated, IsAdminUser)

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
                    'id': freelancer.id,
                })
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ShowFreelancerHistory(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            id = int(request.query_params.get("id"))
            lastShow = int(request.query_params.get("lastShow"))

            if not Freelancer.objects.filter(id=id).exists():
                return Response({"message": "کاربر مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

            projects = AcceptedProject.objects.filter(freelancer__id=id).order_by("-accept_at")[lastShow: lastShow + 9]

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
                    'is_cancel': project.is_cancel,
                    'is_cancel_at': project.is_cancel_at,
                    'is_delete_project': project.is_delete_project,
                    'is_delete_project_at': project.is_delete_project_at,
                    'id': project.id,
                })
            return Response(data, status=status.HTTP_200_OK)

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
                    'id': project.id,
                })
            return Response(data, status=status.HTTP_200_OK)
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
                'id': project.id
            }]
            return Response(data, status=status.HTTP_200_OK)
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



class ShowFreelancersPublishProject(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        try:
            lastShow = int(request.query_params.get("lastShow"))

            projects = AcceptedProject.objects.filter(submited_story=True, story_checked_at_end=False).order_by('submited_story_time')[lastShow: lastShow + 9]
            data = []
            for project in projects:
                data.append({
                    'project': project.project.title,
                    'freelancer': project.freelancer.account.user.username,
                    'price': project.price,
                    'followers': project.followers,
                    'following': project.following,
                    'engagement': project.engagement,
                    'submited_story': project.submited_story,
                    'story_checked_on_start': project.story_checked_on_start,
                    'story_checked_at_end': project.story_checked_at_end,
                    'story_checked_by': project.story_checked_by.user.user.username if project.story_checked_by else None,
                    'id': project.id,
                })
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CheckStoryOnStart(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        try:
            id = request.data.get("id")   #id accepted project
            admin = Admin.objects.get(user__user=request.user)
            
            if not AcceptedProject.objects.filter(id=id, story_checked_on_start=False, story_checked_at_end=False).exists():
                return Response({"message": "تایید استوری فریلنسر قبلا تایید شده است."}, status=status.HTTP_208_ALREADY_REPORTED)

            AcceptedProject.objects.filter(id=id).update(story_checked_on_start=True, stroy_checked_on_start_time=timezone.now(), story_checked_by=admin)
            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CheckStoryAtEnd(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        try:
            id = request.data.get("id")   #id accepted project
            admin = Admin.objects.get(user__user=request.user)
            
            if not AcceptedProject.objects.filter(id=id, story_checked_at_end=False).exists():
                return Response({"message": "تایید استوری فریلنسر قبلا تایید شده است."}, status=status.HTTP_208_ALREADY_REPORTED)
            
            if AcceptedProject.objects.filter(id=id, story_checked_on_start=False).exists():
                return Response({"message": "تایید استوری در هنگام گذاشتن استوری هنوز انجام نشده است."}, status=status.HTTP_208_ALREADY_REPORTED)

            AcceptedProject.objects.filter(id=id).update(story_checked_at_end=True, stroy_checked_at_end_time=timezone.now(), story_checked_by=admin)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ShowConversationsView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        try:
            lastShow = int(request.query_params.get("lastShow"))
            conversations = Conversation.objects.filter(status="Pending").order_by('last_update')[lastShow: lastShow + 9]

            data = []
            for conversation in conversations:
                data.append({
                    "id": conversation.id,
                    "subject": conversation.subject,
                    "status": conversation.status,
                    "created_at": datetime.strftime(conversation.created_at, "%Y-%m-%d %H:%M"),
                    "last_update": datetime.strftime(conversation.last_update, "%Y-%m-%d %H:%M"),
                })

            return Response(data)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ShowConversationsAdminHistory(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        try:
            lastShow = int(request.query_params.get("lastShow"))
            answers = AdminAnswer.objects.filter(admin__user__user=request.user)[lastShow: lastShow + 9]

            data = []
            ids = []
            for answer in answers:
                if not answer.conversation.id in ids:
                    ids.append(answer.conversation.id)
                    data.append({
                        'id': answer.conversation.id,
                        'account': answer.conversation.account.user.username,
                        'subject': answer.conversation.subject,
                        'status': answer.conversation.status,
                        'created_at': answer.conversation.created_at,
                        'last_update': answer.conversation.last_update,
                    })
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ShowSingleConversationView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        try:
            id = int(request.query_params.get("id"))
            
            if not Conversation.objects.filter(id=id).exists():
                return Response({'message': 'بحث موردنظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

            conversation = Conversation.objects.get(id=id)

            tickets = Ticket.objects.filter(conversation=conversation)
            admin_awnsers = AdminAnswer.objects.filter(conversation=conversation, admin__user__user=request.user)

            messages = sorted(chain(tickets, admin_awnsers), key=lambda instance: instance.created_at)

            data = []
            for message in messages:
                try:
                    state = "ADMIN" if message.admin else None
                except:
                    state = "CLIENT"
                data.append({
                    "sender": state,
                    "text": message.text,
                    "created_at": datetime.strftime(message.created_at, "%Y-%m-%d %H:%M"),  
                })

            return Response(data)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AdminAwnserTicketView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        try:
            serializer = AddTicketSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"message": "مقادیر به درستی وارد نشده", "detail":(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
            
            text = serializer.data.get('text')
            conversationId = serializer.data.get('conversationId')

            if Conversation.objects.filter(id=conversationId, status="Closed").exists():
                return Response({"message": "این بحث خاتمه پیدا کرده است."}, status=status.HTTP_406_NOT_ACCEPTABLE)

            conversation = Conversation.objects.get(id=conversationId)
            conversation.last_update = timezone.now()
            conversation.status = "Answered"
            conversation.save()
            admin = Admin.objects.get(user__user=request.user)
            AdminAnswer.objects.create(conversation=conversation, admin=admin, text=text)

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CloseConversationView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        try:
            id = request.data.get("id")
            
            if not Conversation.objects.filter(id=id).exists():
                return Response({'message': 'بحث موردنظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)
            
            if not AdminAnswer.objects.filter(admin__user__user=request.user, conversation__id=id).exists():
                return Response({"message": "شما نمیتوانید این بحث را خاتمه اعلام کنید."}, status=status.HTTP_403_FORBIDDEN)

            if Conversation.objects.filter(id=id, status="CLOSED").exists():
                return Response({"message": "بحث موردنظر قبلا خاتمه یافته است."}, status=status.HTTP_208_ALREADY_REPORTED)
                
            Conversation.objects.filter(id=id).update(status="Closed")

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)