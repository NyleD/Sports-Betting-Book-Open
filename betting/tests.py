from django.test import TestCase
from django.contrib.auth.models import User
from betting.models import Player, Match
from betting.data import getBettingData


class MakeBetTest(TestCase):
    def setUp(self):
        print("setUp: Make Bet.")
        nyle = User.objects.get(username='nyle')
        Player.objects.create(user=nyle)

        gameTime = "00:00:00"
        gameDate = "2018-08-01"
        homeTeam = "Arsenal"
        awayTeam = "Chelsea"
        betType = "h2h"
        eventID = "598606"
        homeOdds = 3.0
        awayOdds = 1.5
        drawOdds = 2
        
    Match.objects.create()
        

    def test1(self):
        print("test1")
        nyle = User.objects.get(username='nyle')
        nyle = Player.objects.get(user=nyle)

        event = "598606"
        amount = 100
        result = nyle.make_bet(event,amount,'home')


        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)

class GetBetsTest(TestCase):
    def setUp(self):
        getBettingData()
        
    def test1(self):
        print("Method: is anything in Matches objects")
        val = False
        if Match.objects.count > 0 
            val = True
        self.assertTrue(val)
