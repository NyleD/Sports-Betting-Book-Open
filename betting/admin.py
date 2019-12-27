from django.contrib import admin
from .models import APIRequest, Player, Bet, Match, Group, League

admin.site.register(APIRequest) 
admin.site.register(Player)
admin.site.register(Bet)
admin.site.register(Match)
admin.site.register(Group)
admin.site.register(League)


