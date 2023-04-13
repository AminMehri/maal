from kavenegar import *


def send_sms(receptor, message):
    try:
        api = KavenegarAPI('Your APIKey')
        numbers = ''
        for num in receptor:
            numbers = numbers + num + ',' 
        params = {
            'sender': '',#optional
            'receptor': numbers,
            'message': message,
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)