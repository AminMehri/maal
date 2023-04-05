from Financial.models import Withdraw, Deposit
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Account.models import Freelancer, Account
import traceback
from django.utils import timezone
import datetime
from .serializers import newDepositSerializer
import requests
import json


MERCHANT = ''
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
CallbackURL = 'http://192.168.1.105:8080/verifyPay/'  # front end url!
# CallbackURL = 'https://botmix.ir/verifyPay/'  # front end url!


def error_text(error_obj):
    text = "مقادیر نادرست برای:"
    for field, reason in error_obj.items():
        text += f"\n{field}: {reason[0]}"
    return text


class WithdrawRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        account = Account.objects.get(user=request.user)
        lastShow = int(request.query_params.get("lastShow"))
        data = [{
            "id": ins.id,
            "is_paid": ins.is_paid,
            "amount": ins.amount,
            "paid_at": datetime.datetime.strftime(ins.paid_at, "%Y-%m-%d %H:%M"),
            "is_paid": ins.is_paid,
            "created_at": datetime.datetime.strftime(ins.created_at, "%Y-%m-%d %H:%M"),
        } for ins in Withdraw.objects.filter(freelancer__account=account, is_cancel=False).order_by("-created_at")[lastShow: lastShow + 9]]

        return Response(data)


    def post(self, request):
        try:
            amount = request.data.get("amount")
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


    def delete(self, request):
        account = Account.objects.get(user=request.user)
        id = request.query_params.get("id")
        withdraw = Withdraw.objects.get(Freelancer__account=account, id=id, is_paid=False, is_cancel=False)
        withdraw.is_cancel = True
        withdraw.cancel_at = timezone.now()
        withdraw.save()
        return Response()


class GetBalance(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        account = Account.objects.get(user=request.user)
        return ("{:,}".format(account.balance) + " تومان")



class Deposit(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        lastShow = int(request.query_params.get("lastShow"))
        account = Account.objects.get(user=request.user)
        data = [{
            "ref_id": dep.ref_id,
            "amount": "{:,}".format(dep.amount) + " تومان",
            "paid_at": datetime.datetime.strftime(dep.paid_at, "%Y-%m-%d %H:%M"),
        } for dep in Deposit.objects.filter(account=account, is_paid=True).order_by("-paid_at")[lastShow: lastShow + 9]]
        return Response(data)
    

    def post(self, request):
        account = Account.objects.get(user=request.user)
        if Deposit.objects.filter(account=account, created_at__gte=timezone.now() - datetime.timedelta(minutes=5)).exists():
            return Response({"message": "هر ۵ دقیقه یکبار قادر به ساخت درگاه پرداخت هستید!", "detail": "لطفا کمی صبر کرده و مجددا تلاش نمایید."}, 
                            status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        ser = newDepositSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"message": "مقادیر به درستی وارد نشده.", "detail": error_text(ser.errors)}, status=status.HTTP_400_BAD_REQUEST)
        
        amount = request.data.get("amount")

        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "callback_url": CallbackURL,
            "description": f"شارژ حساب کاربری",
            "metadata": {"email": request.user.email}
        }
        req_header = {"accept": "application/json",
                        "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)

        authority = req.json()['data']['authority']

        if len(req.json()['errors']) == 0:
            Deposit.objects.create(account=account, amount=amount)
            return Response(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return Response(f"Error code: {e_code}, Error Message: {e_message}", status=status.HTTP_410_GONE)




class ZarinVerify(APIView):

    def post(self, request):

        t_authority = request.data['authority']

        try:
            order = Deposit.objects.get(authority=t_authority)
        except:
            return Response({"message": "سفارش مورد نظر یافت نشد. ممکن است قبلا پرداخت شده باشد"}, status=status.HTTP_404_NOT_FOUND)

        if order.is_paid:
            return Response({"message": "این تراکنش یک بار ثبت شده"})

        req_header = {"accept": "application/json",
                        "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.amount,
            "authority": t_authority
        }

        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)

        if len(req.json()['errors']) == 0:

            t_status = req.json()['data']['code']

            if t_status == 100:

                refId = req.json()['data']['ref_id']
                order.is_paid = True
                order.paid_at = timezone.now()
                order.account.balance += order.amount
                order.save()
                order.account.save()
                    
                return Response({"message": f"تراکنش با موفقیت انجام شد. کد پیگیری: {refId}"})
            
            elif t_status == 101:
                return Response({"message": f"تراکنش ارسال شد. پیام: {req.json()['data']['message']}"})
            
            else:
                return Response({"message": f"تراکنش ناموفق. پیام: {req.json()['data']['message']}"}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return Response({"message": e_message}, status=status.HTTP_400_BAD_REQUEST)
        


