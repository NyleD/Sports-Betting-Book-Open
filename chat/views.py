from django.shortcuts import render

from.models import Room 
from django.http import JsonResponse
from django.conf import settings
from django.views import View
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

fake = Faker()

class AllRoomsView(View): 
    def get(self,request):
        '''All groups member has betted on'''
        rooms = Room.objects.all()
        return render(request, 'rooms.html', {'rooms' : rooms})

class RoomDetailView(View):
    def get(self,request,id):
        room = Room.objects.get(group_id=id)
        return render(request, 'room.html', {'room' : room})

def token(request):
    identity = request.user.username
    device_id = request.GET.get('device', 'default')
    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID


    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                            service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    response = {
        'identity': identity,
        'token': token.to_jwt().decode('utf-8')
    }

    return JsonResponse(response)

