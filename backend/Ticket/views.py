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
from Ticket.models import Ticket
from Account.models import Account
from Ticket.serializers import CreateTicketSerializer
import traceback



class CreateTicket(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            serializer = CreateTicketSerializer(data=request.data)
            if serializer.is_valid():
                subject = serializer.data.get('subject')
                description = serializer.data.get('description')
                
            else:
                return Response({'message': 'لطفا مقادیر موضوع و توضیحات را به درستی وارد کنید.'}, status=status.HTTP_400_BAD_REQUEST)

            account = Account.objects.get(user=request.user)
            
            Ticket.objects.create(user=account, subject=subject, description=description, created_at=timezone.now())

            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)