import requests
import datetime
from celery import shared_task

      

def boolTimeComp(str):

    ''' True When Game Active 
        False When Game Passed
    ''' 

    hour_now = int(datetime.datetime.now().hour) # for hour
    minute_now = int(datetime.datetimgetTimeStame.now().minute) # for minute

    hour = int(str[:2])
    minute = int(str[3:5])
    
    if hour > hour_now:
        return True
    elif hour == hour_now: 
        if minute > minute_now:
            return True
    return False 
    

def boolDateComp(str):
    
    ''' True When Date Active 
        Equal When same Date
        False when Date Passed
    ''' 

    year = int(str[:4])
    month = int(str[5:7])
    day = int(str[8:])

    year_now = int(datetime.datetime.now().year())
    month_now = int(datetime.datetime.now().month())
    day_now = int(datetime.datetime.now().day())

    if year > year_now:
        return {'result': 'true'}
    elif year == year_now: 
        if month > month_now:
            {'result': 'true'}
        elif month == month_now: 
            if day > day_now:
                {'result': 'true'}
            elif day == day_now:
                {'result': 'equal'}
    return {'result': 'false'} 




def getAllTeamEvents(eventList):

    
    activeEventList = []


    for eventsObj in eventList: 

            home_team  = eventsObj["strHomeTeam"]
            away_team = eventsObj["strAwayTeam"]
            date = eventsObj["dateEvent"]
            time = eventsObj["strTime"]
            idEvent =  eventsObj["idEvent"]

            activeEvent = boolDateComp(date)
            
            if activeEvent['result'] == 'true': #Active
                event = {' homeTeam': home_team, 'awayTeam': away_team, 'date':date, 'time':time, 'eventID':idEvent }
                activeEventList.append(event)
            elif activeEvent['result'] == 'equal': #Equal
                boolactiveEvent = boolTimeComp(time)
                if boolactiveEvent:
                    event = {' homeTeam': home_team, 'awayTeam': away_team, 'date':date, 'time':time, 'eventID':idEvent }
                    activeEventList.append(event)
            # Game Has Completed Update Status
                else: # 
                    m = Matches.objects.filter(event_id=idEvent)
                    if m:
                        m.status = 'Complete'
                        m.save() 
            else: 
                m = Matches.objects.filter(event_id=idEvent)
                if m:
                    m.status = 'Complete'
                    m.save()

    return activeEventList



'''When User Goes to thier bets that's when we 
check time stamps and see the results using the other api
'''
def getTimeStamp(homeTeam, awayTeam):

    # PROBLEM: Need to know what game in the series

    event_lookup_URL = 'https://www.thesportsdb.com/api/v1/json/1/searchevents.php?e='

    search_team_details_URL = 'https://www.thesportsdb.com/api/v1/json/1/searchteams.php?t='

    next_5_events_by_team_id_URL = 'https://www.thesportsdb.com/api/v1/json/1/eventsnext.php?id='

    # Try one a direct event lookup 
    eventStr =  homeTeam + '_vs_' + awayTeam

    r = requests.get(event_lookup_URL + eventStr)
    eventJ = r.json
    if eventJ["event"]:
        # Double Check the JSON MIGHT BE LAYERED
        # Calling a function to loop over all the games being played

        activeEvents = getAllTeamEvents(eventJ["event"])

    # Need to look up team names properly
    
    else: 
        # If one team doesn't work might need to try a different team. try the rugby dragons example 
        # Still need to identify the other team name properly 

        r1 = requests.get(search_team_details_URL + homeTeam)
        hometeamJ = r1.json
        r2 = requests.get(search_team_details_URL + awayTeam)
        awayteamJ = r2.json


        if hometeamJ["teams"] and awayteamJ['teams']:
            homeTeamsList = hometeamJ["teams"]
            home_team = homeTeamsList[0]['strTeam']
            awayTeamsList = awayteamJ["teams"]
            away_team = awayTeamsList[0]['strTeam']
            
            # Get Event Details
            eventStr =  home_team + '_vs_' + away_team
            r = requests.get(event_lookup_URL + eventStr)
            eventJ = r.json
            if eventJ["event"]:
                    activeEvents = getAllTeamEvents(eventJ["event"])
            else:
                return False
            
        else:
            return False
    
        # Return a List of these items
    return activeEvents


@shared_task()
def updateBets():

    resolve_bets = Bets.objects.filter(Q(match__status='Complete') & Q(bet_result='Pending'))
    
    for bet in resolve_bets:
        m = bet.match

        if m.goals_home > m.goals_away: # Home Won
            if bet.bet_team == 'Home': # Get Odds Multiple Money
                bet.player.money +=  bet.bet_amt * bet.match.home_odds
                bet.bet_result = 'Won'
            else:
                bet.bet_result = 'Lost'

        elif m.goals_home < m.goals_away: # Away Won
            if bet.bet_team == 'Away': # Get Odds Multiple Money
                bet.player.money +=  bet.bet_amt * bet.match.away_odds
                bet.bet_result = 'Won'
            else:
                bet.bet_result = 'Lost'

        else: # Draw
            if bet.bet_team == 'Draw': # Get Odds Multiple Money
                bet.player.money +=  bet.bet_amt * bet.match.draw_odds
                bet.bet_result = 'Won'
            else:
                bet.bet_result = 'Lost'
        
        bet.save()




@shared_task()
def updateMatches():
    api = APIRequest.load()
    sportURL = 'api.the-odds-api.com/v3/sports/?apiKey='

    # URL
    r = requests.get(sportsURL + settings.BETTING_API_PASSWORD)
    sportsJ = r.json
    sportsH = r.headers

    # Assign Headers
    api.remainingRequests = sportsH['x-requests-remaining ']
    api.usedRequests = sportsH['x-requests-used']
    api.save()

    if api.remainingRequests > 0:

        # Get Odds
        oddsURL = 'https://api.the-odds-api.com/v3/odds/?region=us&mkt=h2h&apiKey='
        r = requests.get(oddsURL + settings.BETTING_API_PASSWORD) 
        oddsJ = r.json
        oddsH = r.headers
        eventList = oddsJ['data']

        if eventList:

            for event in eventList: 
                ''' Odds List in same order as team names '''
                ''' Home Team is not always first '''

                if event['sites']:  # Odds Exist
                    homeTeam = event['home_team']
                    teamsList = event['teams']    
                    oddsList = event['sites'][0]['odds']['h2h']
                    if teamList[0] == homeTeam: 
                        awayTeam = teamsList[1]
                        homeOdd = oddsList[0]
                        awayOdd = oddsList[1]
                    else: 
                        awayTeam = teamsList[0]
                        homeOdd = oddsList[1]
                        awayOdd = oddsList[0]
                    drawOdd = oddsList[2]
                    betType = 'h2h'

                    # Scalability Reasons
                    # eventDetails is a List incase multiple games are going to happen
                    eventDetails = getTimeStamp(homeTeam, awayTeam)

                    for event in eventDetails:
                        if event: 
                            gameTime = event['time']
                            gameDate = event['date']
                            eventID = event['eventID']

                            # According to sportsdb api
                            homeTeam = event['homeTeam']
                            awayTeam = event['awayTeam']
                    
                            # Check if Already exists
                            if Match.objects.filter(eventID=eventID).count() != 0: 
                                
                                # Already Exists
                                betEvent = Match.objects.filter(eventID=eventID)
                                # Add New Odds
                                betEvent.homeOdds = homeOdd
                                betEvent.awayOdds = awayOdd
                                betEvent.drawOdds = drawOdd
                                betEvent.save()
                            else:
                                # Add The Game
                                b = Match.objects.create(gameTime=gameTime, gameDate=gameDate, homeTeam=homeTeam, 
                                        awayTeam=awayTeam, betType=betType, eventID=eventID, homeOdds=homeOdd, 
                                        awayOdds=awayOdd, drawOdds=drawOdd)

        # Add Current Time
        # IF SUCCESSFUL CALL
        hour_now = int(datetime.datetime.now().hour) # for hour
        minute_now = int(datetime.datetime.now().minute) # for minute
        api.lastRequestHour = hour_now
        api.lastRequestMinute = minute_now
        api.remainingRequests = oddsH['x-requests-remaining']
        api.usedRequests = oddsH['x-requests-used']
        api.save()
    

        