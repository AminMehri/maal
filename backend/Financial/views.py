from Financial.models import Withdraw, Deposit
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from Account.models import Freelancer, User, Account



class WithdrawRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            username = request.user.username
            amount = request.data.get("amount")

            user = get_object_or_404(User, username=username)
            account = get_object_or_404(Account, user=user)
            freelancer = get_object_or_404(Freelancer, account=account)

            Withdraw.objects.create(freelancer=freelancer, amount=amount, created_at=timezone.now())
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"data": e}, status=status.HTTP_400_BAD_REQUEST)


