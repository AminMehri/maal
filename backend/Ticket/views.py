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
from Ticket.models import Ticket, Conversation, AdminAnswer
from Account.models import Account
from Ticket.serializers import CreateConversationSerializer, AddTicketSerializer
import traceback
from datetime import datetime


def error_text(error_obj):
    text = "مقادیر نادرست برای:"
    for field, reason in error_obj.items():
        text += f"\n{field}: {reason[0]}"
    return text


class Conversation(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):     # Get List Of Client Conversations
        try:
            lastShow = int(request.query_params.get("lastShow"))

            data = [{
                "id": conver.id,
                "status": conver.status,
                "subject": conver.subject,
                "last_update": datetime.strftime(conver.last_update, "%Y-%m-%d %H:%M"),
            } for conver in Conversation.objects.filter(account__user=request.user).order_by("-last_update")[lastShow: lastShow + 9]]

            return Response(data)
        
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request):    # Open new Conversation
        try:
            serializer = CreateConversationSerializer(data=request.data)
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



class Ticket(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):     # Get Conversation detail and Show All Messages in
        try:
            conversationId = request.query_params.get("id")
            conversation = Conversation.objects.get(id=conversationId, account__user=request.user)
            messages = Ticket.objects.filter(conversation=conversation) + AdminAnswer.objects.filter(conversation=conversation)
            messages = messages.order_by("-created_at")

            conversation = {
                "id": conversation.id,
                "subject": conversation.subject,
                "status": conversation.status,
                "created_at": datetime.strftime(conversation.created_at, "%Y-%m-%d %H:%M"),
                "last_update": datetime.strftime(conversation.last_update, "%Y-%m-%d %H:%M"),
            }

            msgs = [{
                "Sender": "Admin" if msg.admin else "Client",   # ممکنه ارور بده
                "text": msg.text,
                "created_at": datetime.strftime(msg.created_at, "%Y-%m-%d %H:%M"),
            } for msg in messages]

            return Response({"conversation": conversation, "messages": msgs})
        
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request):    # Add Message to existiong Conversation
        try:
            serializer = AddTicketSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"message": "مقادیر به درستی وارد نشده", "detail": error_text(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

            text = serializer.data.get('text')
            conversationId = serializer.data.get('conversationId')
            conversation = Conversation.objects.get(id=conversationId, account__user=request.user)
            conversation.last_update = timezone.now()
            conversation.status = "Pending"
            conversation.save()
            Ticket.objects.create(conversation=conversation, text=text)

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

