from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .forms import *

"""
from .api_connection import get_competitions, get_league_table
from .update_db import create_competition
from .tasks import bet_created
""" 

class GroupsView(ListView):
    model = Group
    template_name = "groups.html"




class GroupView(View):
    def get(self, request, id):
        group = Group.objects.get(id=id)
        leagues = League.objects.filter(group=group,
                                          active=True,
                                          )
        groups = Group.objects.all()

        # Need to Return All Groups and selected groups
        context = {"selected_group": group,
                   "leagues": leagues,
                   "groups": groups
                   }
        return render(request, 'leagues.html', context)

class LeagueView(View):
    def get(self, request, id):
        league  = League.objects.get(id=id)
        matches = Match.objects.filter(league=league,
                                          status='Pending',
                                          )
        leagues = League.objects.all()
        group = league.group
        groups = Group.objects.all()

        context = {"selected_league": league,
                   "matches": matches, 
                   "leagues": leagues, 
                   "groups": groups, 
                   "selected_group": group
                   }
        return render(request, 'matches.html', context)

def get_bet_odd(match, bet):
    if bet == 'Home':
        return match.home_odds
    elif bet == 'Away':
        return match.away_odds
    else:
        return match.draw_odds


class BetMatchView(LoginRequiredMixin, View):

    def get(self, request, id):

        match = Match.objects.get(id=id)
        player = request.user.player
        if match.status == 'Pending':
            form = BetForm
            context = {"match": match,
                       "player": player,
                       "form": form
                       }
            return render(request, "place_bet.html", context)

    def post(self, request, id):
        match = Match.objects.get(id=id)
        user = request.user
        player = Player.objects.get(user=user)
        form = BetForm(request.POST)

        # Get Bet Info
        if form.is_valid():
            bet_amount = form.cleaned_data['bet_amt']
            bet_team = form.cleaned_data['bet_team']
            bet_odd = get_bet_odd(match, bet_team)

            # Enough Money
            if player.money - bet_amount >= 0 and bet_amount >= 0.01:
                player.money -= bet_amount
                player.save()
                bet = Bet.objects.create(player=player,
                                         bet_amt=bet_amount,
                                         match=match,
                                         bet_team=bet_team,
                                         bet_odd=bet_odd
                                         )
        return redirect(reverse('mybets')) 

class BetDetailsView(LoginRequiredMixin, View):
    redirect_field_name = 'next'

    def get(self, request):
        user = request.user
        player = request.user.player 
        bets = Bet.objects.filter(player=player)
        context = {"user": user,
                   "player": player,
                   "bets": bets,
                   }
        return render(request, "my_bets.html", context)


