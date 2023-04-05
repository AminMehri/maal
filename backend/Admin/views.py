from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from Financial.models import Withdraw
from Admin.permission import IsSuperUser
from Account.models import Freelancer
from Project.models import AcceptedProject



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

        except Exception as e:
            return Response({"data": str(e)}, status=status.HTTP_400_BAD_REQUEST)




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
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ShowFreelancerHistory(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            id = request.query_pramas.get("id")

            freelancer = get_object_or_404(Freelancer, id=id)
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

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
