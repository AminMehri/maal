from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from Financial.models import Withdraw
from Admin.permission import IsSuperUser, IsAdminUser, IsUnknownUser, IsFreelancer
from Account.models import Freelancer
from Project.models import Project, AcceptedProject
from Account.models import Account
from Admin.models import Admin
from Project.serializers import CreateProjectSerializer
import traceback


def error_text(error_obj):
    text = "مقادیر نادرست برای:"
    for field, reason in error_obj.items():
        text += f"\n{field}: {reason[0]}"
    return text



# TODO: محاسبه پرایس و فی پرسنت
class CreateProject(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            serializer = CreateProjectSerializer(data=request.data)
            if serializer.is_valid():
                title = serializer.data.get('title')
                total_price = serializer.data.get('total_price')
                description = serializer.data.get('description')
                categories = serializer.data.get('categories')
                files = [x for x in request.FILES]
                
            else:
                return Response({'message': 'لطفا مقادیر خواسته شده را به طور صحیح وارد کنید.', 'detail': error_text(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
            
            owner = Account.objects.get(user=request.user)

            price = 10
            fee_percent = 10
            
            Project.objects.create(title=title, total_price=total_price, price=price, fee_percent=fee_percent, description=description, categories=categories, files=files, owner=owner, admin_confirmed=False, is_full=False, is_publish=False, is_delete=False, created_at=timezone.now())
            return Response()
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ShowProjects(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            lastShow = int(request.query_params.get("lastShow"))

            projects = Project.objects.filter(admin_confirmed=True).filter(is_full=False).filter(is_delete=False).order_by('-created_at')[lastShow: lastShow + 9]

            data = []
            for project in projects:
                data.append({
                    'owner': project.owner.user.username,
                    'title': project.title,
                    'price': project.price,
                    'categories': project.categories,
                    'id': project.id,
                })
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ShowProjectsHistory(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            lastShow = int(request.query_params.get("lastShow"))
            account = Account.objects.get(user=request.user)

            projects = Project.objects.filter(admin_confirmed=True).filter(owner=account).filter(is_delete=False).order_by('-created_at')[lastShow: lastShow + 9]

            data = []
            for project in projects:
                data.append({
                    'owner': project.owner.user.username,
                    'title': project.title,
                    'price': project.price,
                    'categories': project.categories,
                    'id': project.id,
                })
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ShowSingleProject(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            id = int(request.query_params.get("id"))

            if not Project.objects.filter(id=id).filter(admin_confirmed=True).filter(is_delete=False).exists():
                return Response({'message': 'پروژه مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)
            

            project = Project.objects.get(id=id)

            data = [{
                'owner': project.owner.user.username,
                'title': project.title,
                'price': project.price,
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



class DeleteProject(APIView):
    permission_classes = (IsAuthenticated, IsFreelancer)

    def post(self, request):
        try:
            id = request.data.get("id")

            if not Project.objects.filter(id=id).exists():
                return Response({'message': 'پروژه مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)
            
            if not Project.objects.filter(id=id, owner__user=request.user).exists():
                return Response({'message': 'شما قادر به حذف پروژه مورد نظر نیستید.'}, status=status.HTTP_403_FORBIDDEN)

            if Project.objects.filter(id=id, owner__user=request.user, is_delete=True).exists():
                return Response({'message': 'پروژه مورد نظر قبلا حذف شده است.'}, status=status.HTTP_208_ALREADY_REPORTED)
            
            if Project.objects.filter(id=id, owner__user=request.user, is_publish=True).exists():
                return Response({'message': 'شما نمیتوانید پروژه منتشر شده را حذف نمایید.'}, status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

            if AcceptedProject.objects.filter(project__id=id).exists():
                AcceptedProject.objects.filter(project__id=id).update(is_delete_project=True, is_delete_project_at=timezone.now(), pending=False)

            Project.objects.filter(id=id).update(is_delete=True, deleted_at=timezone.now())
            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# TODO: محاسبه فالوور فالوینگ اینگیجمنت و پرایس
class GetProject(APIView):
    permission_classes = (IsAuthenticated, IsFreelancer)

    def post(self, request):
        try:
            id = request.data.get("id")

            if Project.objects.filter(id=id).exists():
                proj = Project.objects.get(id=id)
                if proj.admin_confirmed == False or proj.is_full == False or proj.is_delete == True or proj.is_publish == False:
                    return Response({"message": "پروژه مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "پروژه مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
            
            freelancer = Freelancer.objects.get(account__user=request.user) 
            
            if AcceptedProject.objects.filter(project__id=id, freelancer=freelancer).exists():
                return Response({"message": "شما قبلا این پروژه را قبول کرده اید."}, status=status.HTTP_208_ALREADY_REPORTED)
            
            price = 10
            followers = 10
            following = 10
            engagement = 10

            AcceptedProject.objects.create(project_id=id, freelancer=freelancer, pending=True, request_at=timezone.now(), price=price, followers=followers, following=following ,engagement=engagement)
            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# TODO: یه فریلنسر تا کی میتونه از قبول پروژه انصراف بده
class CancelAcceptedProject(APIView):
    permission_classes = (IsAuthenticated, IsFreelancer)

    def post(self, request):
        try:
            id = request.data.get("id")

            if not AcceptedProject.objects.filter(project__id=id, freelancer__account__user=request.user, is_delete_project=False).exists():
                return Response({"message": "شما این پروژه را قبول نکرده اید."}, status=status.HTTP_404_NOT_FOUND)
            
            if AcceptedProject.objects.filter(project__id=id, freelancer__account__user=request.user, is_cancel=True).exists():
                return Response({"message": "شما قبلا از قبول این پروژه انصراف داده اید."}, status=status.HTTP_208_ALREADY_REPORTED)
            
            AcceptedProject.objects.filter(project__id=id, freelancer__account__user=request.user).update(is_cancel=True, is_cancel_at=timezone.now(), pending=False)
            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ShowAcceptedProjectHistory(APIView):
    permission_classes = (IsAuthenticated, IsFreelancer)

    def get(self, request):
        try:
            lastShow = int(request.query_params.get("lastShow"))

            freelancer = Freelancer.objects.get(account__user=request.user)             
            projects = AcceptedProject.objects.filter(freelancer=freelancer)[lastShow: lastShow + 9]

            data = []
            for project in projects:
                data.append({
                    'project': project.project.title,
                    'freelancer': project.freelancer.account.user.username,
                    'pending': project.pending,
                    'accept_at': project.accept_at,
                    'price': project.price,
                    'is_cancel': project.is_cancel,
                    'is_delete_project': project.is_delete_project,
                    'id': project.id,
                })
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SubmitStory(APIView):
    permission_classes = (IsAuthenticated, IsFreelancer)

    def post(self, request):
        try:
            id = request.data.get("id")    #id project

            if not Project.objects.filter(id=id, admin_confirmed=True, is_full=True, is_delete=False).exists():
                return Response({"message": "پروژه موردنظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
            
            if Project.objects.filter(id=id, is_publish=False).exists():
                return Response({"message": "پروژه مورد نظر هنوز پابلیش نشده است.", "detail": "لطفا تا پرشدن ظرفیت پروژه منتظر بمانید."}, status=status.HTTP_423_LOCKED)

            if not AcceptedProject.objects.filter(project__id=id, freelancer__account__user=request.user).exists():
                return Response({"message": "شما پروژه موردنظر را قبول نکرده اید و نمیتوانید این درخواست را ثبت کنید"}, status=status.HTTP_403_FORBIDDEN)
            
            if AcceptedProject.objects.filter(project__id=id, freelancer__account__user=request.user, submited_story=True).exists():
                return Response({"message": "شما قبلا تایید استوری خودرا انجام داده اید."}, status=status.HTTP_208_ALREADY_REPORTED)
            
            if AcceptedProject.objects.filter(project__id=id, freelancer__account__user=request.user, is_cancel=True).exists():
                return Response({"message": "شما از قبول این پروژه انصراف داده اید."}, status=status.HTTP_404_NOT_FOUND)
            
            AcceptedProject.objects.filter(project__id=id, freelancer__account__user=request.user).update(submited_story=True, submited_story_time=timezone.now())
            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
