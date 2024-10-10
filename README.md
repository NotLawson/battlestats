# BattleStats
## A Stat Tracker for [BattleTabs](https://battletabs.com)

> WIP: This app is a work in progress. Many feature haven't been implemented/don't work

> **This app will not function, as the API I have been thinking of using is an Interal one. On request of the developers, I will not use this API. For testing purposes however, I will include a mock API, which will mimic the actual one.**

## Features
- ~~Get Current Player Stats~~ Mock Current player stats
- Save player stats to a InfluxDB database
- Display Stat history using Chart.js
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

Ignore the Docker stuff; I like to containerise all my applications to run on my server. Once I finish it, I will publish is to GHCR