from django.shortcuts import render
from newsapi import NewsApiClient 
import settings
# Create your views here.

# returns  a list of num news objects (title, description, Url, ImageUrl)
def getNews(num, jsonObj):
    if jsonObj['status'] == 'ok' and jsonObj['totalResults'] > 0:
        newsList = []
        if jsonObj['totalResults'] < num: 
            num = len(jsonObj['articles'])
        
        articles = jsonObj['articles']

        for i in range(num):
            title = articles[i]['title']
            description = articles[i]['description']
            
            if description and len(description) > 150:
                description = description[:150]
                description += "..."

            url = articles[i]['url']
            urlImg = articles[i]['urlToImage']
            news = { 'title' : title, 
                     'descrip' : description,
                     'url' : url,
                     'imgUrl' : urlImg}
            newsList.append(news)
        return newsList    
    else:
        return []



'''
Based on popular bets
'''

def headings(request):

    newsapi = NewsApiClient(api_key=setting.NEW_API_KEY)
    nfl_headlines = newsapi.get_top_headlines(q='',
                                          sources='nfl-news',
                                          language='en')
    top_headlines_random_nfl = newsapi.get_top_headlines(q='nfl',
                                          category='sports',
                                          language='en',
                                          country='us')
    nhl_headlines = newsapi.get_top_headlines(q='',
                                          sources='nhl-news',
                                          language='en')
    top_headlines_random_nhl = newsapi.get_top_headlines(q='nhl',
                                          category='sports',
                                          language='en',
                                          country='us')
    top_headlines_bbc = newsapi.get_top_headlines(q='',
                                          category='sports',
                                          language='en',
                                          country='us')
    top_headlines_random = newsapi.get_top_headlines(q='',
                                          category='sports',
                                          language='en')
    soccer_headlines = newsapi.get_everything(q='barcelona, manchester city, juventus, liverpool, psg, bayern, atletico madrid, real madrid, manchester united, chelsea, arsenal, tottenham',
                                          language='en')
    
    nba_headlines = newsapi.get_everything(q="""Celtics, Nets, Knicks, Raptors, Bulls, Cavaliers, Pistons, Pacers
                                              Bucks, Hawks, Hornets, Heat, Magic, Wizards, Mavericks, Rockets, Grizzlies, 
                                              Pelicans, Spurs, Nuggets, Timberwolves, Thunder, Blazers, Jazz, Warriors, Clippers,
                                              Lakers, Suns, Kings""",
                                              language='en')
    top_headlines_odds = newsapi.get_everything(q='odds, prediction, betting odds',
                                          language='en')

    # Parse 
    topList = getNews(9, top_headlines_bbc)
    if not len(topList) == 9:
        randomSource = getNews(9 - len(topList), top_headlines_random)
        topList += randomSource
    
    nhlList = getNews(5,  nhl_headlines)
    if not len(nhlList) == 5:
        randomSource = getNews(5 - len(nhlList), top_headlines_random_nhl)
        nhlList += randomSource 
    
    nflList = getNews(5, nfl_headlines)
    if not len(nflList) == 5:
        randomSource = getNews(5 - len(nflList), top_headlines_random_nfl)
        nflList += randomSource
    
    soccerList = getNews(5, soccer_headlines)  
    nbaList = getNews(5, nba_headlines)
    oddsList = getNews(9, top_headlines_odds)
     
    print(oddsList)
    news = {'topList' : topList, 'nhlList' : nhlList, 'nflList' : nflList, 'soccerList' : soccerList, 'nbaList' : nbaList, 'oddsList' : oddsList}
    return render(request, 'sportsNews/news2.html', news) 


