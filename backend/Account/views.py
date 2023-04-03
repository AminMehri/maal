from rest_framework.views import APIView
from .models import Account, User, InstagramAccount, Freelancer, Rule
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from django.shortcuts import get_object_or_404
from rest_framework import status
import random
import string
from django.utils import timezone
import datetime
from django.core.mail import send_mail
from django.template.loader import get_template
from rest_framework.permissions import IsAuthenticated
from .serializers import SignUpSerializer, SumbitInstaSerializer
from backend.settings import EMAIL_HOST_USER, base_url
from rest_framework_simplejwt.tokens import RefreshToken
import after_response


def rand_ascii(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))


def error_text(error_obj):
    text = "مقادیر نادرست برای:"
    for field, reason in error_obj.items():
        text += f"\n{field}: {reason[0]}"
    return text


@after_response.enable
def send_email(title, html_content, receiver):
    try:
        # return
        res = send_mail(title, '', EMAIL_HOST_USER, receiver, fail_silently=True, html_message=html_content)
        print(f"send mail to {receiver}: ", title, f"\nstatus: {res}")
    except Exception as e:
        print(f"error in sending email to {receiver} for reason: {str(e)}")



class UserSecThrottle(UserRateThrottle):
    scope = 'signup'


class SignUp(APIView):
    throttle_classes = [UserSecThrottle]

    def post(self, request):
        try:
            ser = SignUpSerializer(data=request.data)
            if not ser.is_valid():
                return Response({"message": "مقادیر ایمیل یا پسورد قابل قبول نیست", "detail": error_text(ser.errors)}, status=status.HTTP_400_BAD_REQUEST)
            email = request.data.get('email')
            password = request.data.get('password')

            if User.objects.filter(email=email).exists():
                return Response({"message": "این ایمیل قبلا ثبت شده"}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(username=email).exists():
                return Response({"message": "این نام کاربری قبلا ثبت شده"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=email, email=email, password=password)

            token = rand_ascii(100)
            Account(user=user, email_verify_token=token, email_verify_generate_time=timezone.now()).save()
            refresh = RefreshToken.for_user(user)

            htmly = get_template('email-confirmation.html')
            d = {'token': token, 'id': user.id}
            html_content = htmly.render(d)
            send_email.after_response("تایید ایمیل Trade", html_content, [user.email])

            return Response({"access": str(refresh.access_token), "refresh": str(refresh)}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)



class CreateEmailToken(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user = request.user
            account = Account.objects.get(user=user)
            if account.email_verified:
                return Response({"message": "ایمیل شما قبلا تایید شده"}, status=status.HTTP_400_BAD_REQUEST)
            # if account.email_verify_generate_time and account.email_verify_generate_time + datetime.timedelta(minutes=2) > timezone.now():
            #     return Response({"message": "شما هر دو دقیقه یکبار قادر به درخواست ایمیل تایید هستید.",
            #                      "detail": "لطفا کمی صبر کرده و مجددا امتحان نمایید."},
            #                     status=status.HTTP_400_BAD_REQUEST)
            token = rand_ascii(100)
            account.email_verify_token = token
            account.email_verify_generate_time = timezone.now()
            account.save()
            htmly = get_template('email-confirmation.html')
            d = {'token': token, 'id': user.id}
            print(d)
            html_content = htmly.render(d)
            send_email.after_response("تایید ایمیل botmix", html_content, [user.email])
            return Response({"message": "لینک تایید ایمیل برای شما ارسال شد.", "detail": "بخش اسپم را درصورت عدم ارسال بررسی نمایید."})

        except Exception as e:
            print(e)
        

class VerifyEmail(APIView):

    def post(self, request):
        try:
            token = request.data.get("token")
            userId = request.data.get("id")
            try:
                account = Account.objects.get(user__id=userId, email_verify_token=token)
            except:
                return Response({"message": "ایمیل مورد نظر یافت نشد", "detail": "ممکن است قبلا تایید شده باشد."}, status=status.HTTP_400_BAD_REQUEST)
            account.email_verified = True
            account.email_verify_token = None
            account.save()
            return Response()
        except Exception as e:
            print(e)
        

class ForgetPassword(APIView):
    throttle_classes = [UserSecThrottle]

    def post(self, request):
        try:
            try:
                user = User.objects.get(email=request.data.get("email"))
                account = Account.objects.get(user=user)
            except:
                return Response({"message": "ایمیل وارد شده وجود ندارد"}, status=status.HTTP_400_BAD_REQUEST)

            if account.reset_token_created_at and account.reset_token_created_at + datetime.timedelta(minutes=5) > timezone.now():
                return Response({"message": "هر پنج دقیقه یکبار قادر به درخواست بازیابی رمز عبور هستید"}, status=status.HTTP_400_BAD_REQUEST)

            token = rand_ascii(100)
            account.reset_password_token = token
            account.reset_token_created_at = timezone.now()

            htmly = get_template('email-forget.html')
            d = {'token': token, 'id': user.id}
            html_content = htmly.render(d)
            send_email.after_response("فراموشی رمز عبور Trade", html_content, [user.email])
            account.save()
            return Response()

        except Exception as e:
            print(e)
        

class SetPassword(APIView):

    def post(self, request):
        try:
            token = request.data.get("token")
            userId = request.data.get("id")
            newPass = request.data.get("password")

            try:
                user = User.objects.get(id=userId)
                account = Account.objects.get(reset_password_token=token, user=user)
            except:
                return Response({"message": "لینک فراموشی رمز منقضی یا استفاده شده, لطفا مجددا درخواست لینک بازنشانی رمز کنید."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(newPass)
            account.reset_password_token = None
            user.save()
            account.save()

            return Response()

        except Exception as e:
            print(e)        



class UserInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            account = get_object_or_404(Account, user=request.user)
            return Response({"data": {
                    "email_verified": account.email_verified,
                    "email": account.user.email,
                    }
                }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)


class InstagramAccount(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        account = Account.objects.get(user=request.user)
        if len(InstagramAccount.objects.filter(account=account, is_delete=False)) > 3:
            return Response({"message": "نمیتوانید بیشتر از ۳ اکانت اینستاگرام اضافه کنید."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        ser = SumbitInstaSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"message": "مقادیر به درستی وارد نشده.", "detail": error_text(ser.errors)}, status=status.HTTP_400_BAD_REQUEST)
        
        InstagramAccount(account=account, instagram_id=request.data.get("instagram_id")).save()
        return Response({"message": "اکانت اینستاگرام شما ثبت شد."})


    def delete(self, request):
        id = request.query_params.get("id")
        ins = InstagramAccount.objects.get(account=Account.objects.get(user=request.user), id=id, is_delete=False)
        ins.is_delete = True
        ins.delete_at = timezone.now()
        return Response({"message": "اکانت مورد نظر حذف شد", "timer": True})


    def get(self, request):
        data = [{
            "instagram_id": insta.instagram_id,
            "is_verify": insta.is_verify,
            "instagram_id": insta.instagram_id,
        } for insta in InstagramAccount.objects.filter(account=Account.objects.get(user=request.user), is_delete=False)]

        return Response(data)
    

class FreelancerSetup(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        account = Account.objects.get(user=request.user)
        id = request.query_params.get("id")
        if Freelancer.objects.filter(account=account).exists():
            return Response({"message": "شما قبلا درخواست اکانت فریلنسری خودرا ثبت کردید."}, status=status.HTTP_400_BAD_REQUEST)
        
        instaAcc = InstagramAccount.objects.get(account=account, is_delete=False, id=id)
        Freelancer(account=account, instagram_account=instaAcc).save()
        return Response({"message": "درخواست ساخت اکانت فریلنسری برای شما ثبت شد.", "detail": 
            "به محض تایید اکانت شما توسط ادمین, پیامک اطلاع رسانی برای شما ارسال شده و میتوانید از خدمات فریلنسری استفاده نمایید."})
    
    def get(self, request):
        account = Account.objects.get(user=request.user)
        if Freelancer.objects.filter(account=account).exists():
            ins = Freelancer.objects.get(account=account)
            data = {
                "is_accepted": ins.is_accepted,
                "verified_time": datetime.datetime.strftime(ins.verified_time, "%Y-%m-%d %H:%M"),
                "created_at": datetime.datetime.strftime(ins.created_at, "%Y-%m-%d %H:%M"),
                "reject_reason": ins.reject_reason
            }
            return Response(data)
        else:
            return Response({})
        

class OverviewAccount(APIView):
    def get(self, request):
        insta_id = request.query_params.get("insta_id")
        if InstagramAccount.objects.filter(instagram_id=insta_id, is_delete=False).exists():
            instaAcc = InstagramAccount.objects.get(instagram_id=insta_id, is_delete=False)
            data = {    # TODO: اگه فریلنسر بود بگه چند تا کار تاحالا انجام داده و امتیازاش چجوریه؟
                "followers": instaAcc.followers,
                "following": instaAcc.following,
                "engagement": instaAcc.engagement,
                "hashtags": instaAcc.hashtags,
                "uploads": instaAcc.uploads,
                "post_per_day": instaAcc.post_per_day,
                "profile": base_url + instaAcc.profile.url,
                "full_name": instaAcc.full_name,
                "bio": instaAcc.bio,
                "category": instaAcc.category,
                "created_at": instaAcc.created_at,
            }
            return Response(data)
        else:
            return Response({"message": "اکانت موردنظر یافت نشد!"}, status=status.HTTP_404_NOT_FOUND)
        

rulesDescription = {
    "newUser": "اکانت جدید, مجاز به پذیرش روزانه ۵ پروژه هستید. به محض تمام شدن این رول محدودیتی نخواهید داشت.",
    "Ban": "تا اتمام این رول نمیتوانید پروژه ای قبول کنید!",
    "bronzeDiscount": "از ۱۰ درصد دستمزد بیشتر در پروژه ها لذت ببرید! همچنین اولویت بالاتری برای قبول پروژه ها دارید",
    "silverDiscount": "از ۲۰ درصد دستمزد بیشتر در پروژه ها لذت ببرید! همچنین اولویت بالاتری برای قبول پروژه ها دارید",
    "goldDiscount": "از ۳۰ درصد دستمزد بیشتر در پروژه ها لذت ببرید! همچنین اولویت بالاتری برای قبول پروژه ها دارید",
}

class OwnRules(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        account = Account.objects.get(user=request.user)

        data = [{
            "name": rule.rule,
            "description": rulesDescription.get(rule.rule),
            "created_at": datetime.datetime.strftime(rule.created_at, "%Y-%m-%d %H:%M"),
            "expire_at": datetime.datetime.strftime(rule.expire_at, "%Y-%m-%d %H:%M"),
            
        } for rule in Rule.objects.filter(account=account, is_expire=False)]
        
        return Response(data)
