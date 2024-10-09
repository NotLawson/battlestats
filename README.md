# BattleStats
## A Stat Tracker for [BattleTabs](https://battletabs.com)

> WIP: This app is a work in progress. Many feature haven't been implemented/don't work

## Features
- Get Current Player Stats
- ~~Save player stats toa MySQL database~~
- ~~Display Stat history using Chart.js~~
- ~~Analyse Replays to find most used ships, fleets, etc~~
- ~~Yoink replays from BattleTabs Live~~
## Get Started

Install requirements in requirement.txt

Run main.py

```
pip install -r requirements.txt
python main.py
```

It will create a Flask server on [127.0.0.1:5000](http://127.0.0.1).

Ignore the Docker stuff; I like to containerise all my applications to run on my server. Once i finish it, I will publish is to GHCR

Also ignore ws.py; It's just some fiddling with GraphQL over Websockets. This will be implemented shortly as it is more effient