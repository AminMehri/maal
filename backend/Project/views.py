from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from Financial.models import Withdraw
from Admin.permission import IsSuperUser, IsAdminUser, IsUnknownUser
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


# فیلد فایل چون اری فیلده نمیدونم چجوری بهش بدم فایلارو
class CreateProject(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            serializer = CreateProjectSerializer(data=request.data)
            if serializer.is_valid():
                title = serializer.data.get('title')
                total_price = serializer.data.get('total_price')
                price = serializer.data.get('price')
                fee_percent = serializer.data.get('fee_percent')
                description = serializer.data.get('description')
                categories = serializer.data.get('categories')
                files = serializer.data.get('files')
                
            else:
                return Response({'message': 'لطفا مقادیر خواسته شده را به طور صحیح وارد کنید.', 'detail': error_text(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
            
            owner = Account.objects.get(user=request.user)
            
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
                    'total_price': project.total_price,
                    'price': project.price,
                    'fee_percent': project.fee_percent,
                    'categories': project.categories,
                })
            return Response({"data": data}, status=status.HTTP_200_OK)
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
                    'total_price': project.total_price,
                    'price': project.price,
                    'fee_percent': project.fee_percent,
                    'categories': project.categories,
                })
            return Response({"data": data}, status=status.HTTP_200_OK)
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



class DeleteProject(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            id = request.data.get("id")
            account = Account.objects.get(user=request.user)

            if not Project.objects.filter(id=id).exists():
                return Response({'message': 'پروژه مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)
            
            if not Project.objects.filter(id=id).filter(owner=account).exists():
                return Response({'message': 'شما قادر به حذف پروژه مورد نظر نیستید.'}, status=status.HTTP_403_FORBIDDEN)

            if Project.objects.filter(id=id).filter(owner=account).filter(is_delete=True).exists():
                return Response({'message': 'پروژه مورد نظر قبلا حذف شده است.'}, status=status.HTTP_208_ALREADY_REPORTED)
            
            if Project.objects.filter(id=id).filter(owner=account).filter(is_publish=True).exists():
                return Response({'message': 'شما نمیتوانید پروژه منتشر شده را حذف نمایید.'}, status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)


            Project.objects.filter(id=id).update(is_delete=True, deleted_at=timezone.now())
            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetProject(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            id = request.data.get("id")

            if Project.objects.filter(id=id).exists():
                proj = Project.objects.get(id=id)
                if proj.admin_confirmed == False or proj.is_full == True or proj.is_delete == True or proj.is_publish == False:
                    return Response({"message": "پروژه مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "پروژه مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
            
            account = Account.objects.get(user=request.user)
            
            # kiram to django. chera get error mide???. ye min pish nemidad. alan mide!!!!
            try:
                freelancer = Freelancer.objects.get(account=account) 
            except:
                freelancer = None

            if not freelancer:
                return Response({"message": "تنها فریلنسر ها قادر به قبول پروژه هستند.", "detail": "برای دسترسی به این بخش لطفا درخواست خود را برای فریلنسر شدن ثبت نمایید."}, status=status.HTTP_404_NOT_FOUND)
                
            if freelancer.is_accepted == False:
                return Response({"message": "تنها فریلنسر ها قادر به قبول پروژه هستند.", "detail": "درخواست شما برای فریلنسری هنوز تایید نشده است. لطفا بعدا تلاش کنید."}, status=status.HTTP_404_NOT_FOUND)
            
            price = 10
            followers = 10
            following = 10
            engagement = 10

            AcceptedProject.objects.create(project_id=id, freelancer=freelancer, pending=True, request_at=timezone.now(), price=price, followers=followers, following=following ,engagement=engagement)
            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ShowAcceptedProjectHistory(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            lastShow = int(request.query_params.get("lastShow"))
            account = Account.objects.get(user=request.user)

            # kiram to django. chera get error mide???. ye min pish nemidad. alan mide!!!!
            try:
                freelancer = Freelancer.objects.get(account=account) 
            except:
                freelancer = None

            if not freelancer:
                return Response({"message": "تنها فریلنسر ها قادر به قبول پروژه هستند.", "detail": "برای دسترسی به این بخش لطفا درخواست خود را برای فریلنسر شدن ثبت نمایید."}, status=status.HTTP_404_NOT_FOUND)
                    
            if freelancer.is_accepted == False:
                return Response({"message": "تنها فریلنسر ها قادر به قبول پروژه هستند.", "detail": "درخواست شما برای فریلنسری هنوز تایید نشده است. لطفا بعدا تلاش کنید."}, status=status.HTTP_404_NOT_FOUND)
            
            projects = AcceptedProject.objects.filter(freelancer=freelancer)[lastShow: lastShow + 9]

            data = []
            for project in projects:
                data.append({
                    "project": project.project.title,
                    "freelancer": project.freelancer.account.user.username,
                    "pending": project.pending,
                    "accept_at": project.accept_at,
                    "price": project.price,
                })
            
            return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



