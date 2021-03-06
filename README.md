# Open Source Betting Platform
**Selected prototyped parts of the Sports Betting Book platform are open sourced**
<br/>
<br/>
**If you would like to learn more about our full-development platform or need guidance with software related issues, please contact nyle.dharani@gmail.com for questions and concerns**
<br/>
## Technologies Used
- Python Backend with Django Framework
- ODDS and THESPORTSDB API's
- Microsoft's Cognitive API
- ESPN NEWS API
- Celery
- Twilio
- JQuery
## Demo

The Betting Platform's front-page is a newsfeed. It's based on popular bets, top news from ESPN NEWS API, popular predicition articles, and sport categories. (Soccer, Football, Hockey, Basketball) 

![](newsfeed.gif)

You can bet on different sports and leagues. Select a match, choose a team to bet on and the amount of tokens you want to bet. Your bet will be added to your "My Bets Table". 

![](making_a_bet.gif)

You might've noticed that the Manchester vs Newcastle game was live, all Odds get updated every 2 hours with Celery. This is provided by the ODDS API https://the-odds-api.com/liveapi/guides/v3/, 500 free requests a month. Based on bet outcomes, the table automatically updates, and user balances also get updated. 

![](tablelivegame.png)   ![](tablecompleted.png)

All matches are updated every hour with Celery, using the THESPORTSDB API https://www.thesportsdb.com/api/, which is free! When betting, matches automatically are removed from selection once they go live and new ones take thier place. Max 10 are displayed. 

![](CompletedGames.png) 
![](NewGames.png) 

Players are authenticated to chat in selected rooms based on what type of sport groups they have bet on. We want to encourage chat amongst betters that are betting on common teams, like the english premier league. 

![](chat.gif)

Players also get a personal profile with thier information. We have also added a face-verfication for security purposes, so that betters are who they say they are. This reduces the risk of invalid information for personal gain, and helps betters feel safe when talking with friends online. 

![](profile.gif)
![](face_verification.gif)
![](face_verification.png)

Authentication

![](authenticated.gif)


**Please feel free to play with code, add new features, and learn from existing code**


