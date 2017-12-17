import os
import csv
import json
from tempfile import NamedTemporaryFile
import datetime
import newTwitchClient as NTC

with open('games.json') as game_data:
    games = json.load(game_data)

twitch = NTC.TwitchApi()

for file in os.listdir("./csv/"):
    print(file)
    if file.endswith(".csv"):
        with open('./csv/'+file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            # Handle headers
            header = reader.__next__()
            for row in reader:
                if row[3] != "NULL":
                    if not row[3] in games:
                        new_game = twitch.GetGames(gid=row[3])
                        games[row[3]] = new_game.json()

with open('games.json', 'w') as data_file:
        json.dump(games, data_file)