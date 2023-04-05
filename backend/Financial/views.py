from Financial.models import Withdraw, Deposit
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from Account.models import Freelancer, User, Account
from Financial.serializers import WithdrawRequestSerializer
import traceback



class WithdrawRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            serializer = WithdrawRequestSerializer(data=request.data)
            if serializer.is_valid():
                amount = serializer.data.get('amount')
                
            else:
                return Response({'message': 'لطفا مقدار برداشتی مورد نظر را به طور صحیح وارد کنید.'}, status=status.HTTP_400_BAD_REQUEST)

            account = Account.objects.get(user=request.user)
            if not Freelancer.objects.filter(account=account, is_accepted=True).exists():
                return Response({"message": "اکانت فریلنسری تایید شده ای برای شما یافت نشد!", 
                                "detail": "اگر درخواست اکانت فریلنسری خود را ثبت کردید باید تا زمان تایید شدن آن صبر کنید."})
            
            freelancer = Freelancer.objects.get(account=account, is_accepted=True)

            Withdraw.objects.create(freelancer=freelancer, amount=amount)
            return Response(status=status.HTTP_200_OK)
        
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)