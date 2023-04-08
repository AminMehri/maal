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
from Ticket.models import Ticket, Conversation
from Account.models import Account
from Ticket.serializers import CreateTicketSerializer
import traceback


def error_text(error_obj):
    text = "مقادیر نادرست برای:"
    for field, reason in error_obj.items():
        text += f"\n{field}: {reason[0]}"
    return text


class CreateTicket(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            serializer = CreateTicketSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"message": "مقادیر به درستی وارد نشده", "detail": error_text(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)


            subject = serializer.data.get('subject')
            text = serializer.data.get('text')
            account = Account.objects.get(user=request.user)
            conversation = Conversation.objects.create(account=account, subject=subject, status="Pending" , last_update=timezone.now())
            Ticket.objects.create(conversation=conversation, text=text)

            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)