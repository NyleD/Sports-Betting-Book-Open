from django.db import models
import json
from django.core.cache import cache
from .data import boolTimeComp, boolDateComp
from django.contrib.auth.models import User
from datetime import datetime



ACCOUNT_TYPE = ((1, "FREE"),
              (2, "BRONZE"),
              (3, "SILVER"), 
              (4, "GOLD"))

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField("The player's money.", default=1000)
    rank = models.IntegerField("The player's rank", default=1)
    account_type = models.IntegerField(choices=ACCOUNT_TYPE, default=1)
    
    def add_money(money):
        self.money = self.money + money


    def make_bet(self, event, amount, team):

        if amount > self.money: 
            return {"bet_result" : 'out of money'}
        else: 
            self.money = self.money - amount

            match = Match.objects.filter(eventID=event)
            bet = Bet.objects.create(player=self,match=match,bet_amt=amount,bet_team=team)
            self.bets_set.add(bet)
        return {"bet_result" : 'sucess'}
    
    def update_bets(self):

        bets = self.bets_set.all() 

        for bet in bets:
            if gamePassed(bet.match.gameTime,bet.match.gameDate):
               bet.updateBet()
               bet.delete()
        

    def __unicode__(self):
        return self.user.username


class Group(models.Model):
    name = models.CharField(max_length=50)
    players = models.ManyToManyField(Player, 'groups')

    def __str__(self):
        return self.name

class League(models.Model):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,related_name="group")
    active = models.BooleanField(default=True)

MATCH_STATUS = (('Pending','Pending'),
                ('Complete', 'Complete'),
                ('Live', 'Live'))

# Matches that don't belong anywhere, just go in here
DEFAULT_LEAGUE_ID = 1 

class Match(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league', default=DEFAULT_LEAGUE_ID)
    time = models.TimeField(max_length=100, default=datetime.now)
    date = models.DateField(max_length=100, default=datetime.now)
    home_team = models.CharField(max_length=100) 
    away_team = models.CharField(max_length=100)
    home_odds = models.FloatField(default=1)
    away_odds = models.FloatField(default=1)
    draw_odds = models.FloatField(default=1)
    goals_home = models.IntegerField(default=0)
    goals_away = models.IntegerField(default=0)
    status = models.CharField(choices=MATCH_STATUS, max_length=100, default='Pending') 
    event_id = models.TextField(default='')

    def __str__(self):
        return str(self.home_team + " vs " + self.away_team)

BET_ON = (('Home', "Home"),('Away', "Away"),('Draw', "Draw")) 

BET_OUTCOME = (('Lost','Lost'),
                ('Won', 'Won'), 
                ('Pending', 'Pending'))


# Error Bets, go to Match One, which doesn't result in a bet
DEFAULT_ERROR_BET_ID = 1

class Bet(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bets', default=DEFAULT_ERROR_BET_ID)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match')
    bet_amt = models.IntegerField(default=0)
    bet_team = models.CharField(choices=BET_ON, max_length=50)
    bet_result = models.CharField(choices=BET_OUTCOME, default='Pending', max_length=25)
    bet_odd = models.FloatField(default=1)

    def updatePlayerMoney(self):
        odds = 0 
        if bet_team == 'Home':
            odds = match.homeOdds
        elif bet_team == 'Away':
            odds = match.awayOdds
        else:
            odds = match.drawOdds 
        
        player.add_money(bet_amt * odds)
       
    def updateBet(self):

        eventID = match.eventID
        eventDetailsURL = 'https://www.thesportsdb.com/api/v1/json/1/lookupevent.php?id'

        r = requests.get(eventDetailsURL + eventID)
        eventJ = r.json

        if evenntJ:
            homeScore = int(eventJ["intHomeScore"])
            awayScore = int(eventJ["intAwayScore"])

            if homeScore > awayScore and bet.bet_team == 'home' or \
            homeScore == awayScore and bet.bet_team == 'draw' or \
            homeScore < awayScore and bet.bet_team == 'away':
                bet.UpdatePlayerMoney()
            





class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)

class APIRequest(SingletonModel):
    # stores in "HH:MM"
    lastRequestHour = models.IntegerField(default=0) # Max Value 23
    lastRequestMinute = models.IntegerField(default=0) # Max Value 59
    remainingRequests = models.IntegerField(default=150)
    usedRequests = models.IntegerField(default=0)

