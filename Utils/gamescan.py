import os, sys
import csv
import json
from tempfile import NamedTemporaryFile
import datetime
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import newTwitchClient as NTC

parser = argparse.ArgumentParser()
parser.add_argument('--all', action='store_true', help="Run against ALL csv files.")
args = parser.parse_args()

month = str(datetime.datetime.now()).split()[0][:7]

if args.all:
    scan = ".csv"
else:
    scan = month+".csv"

with open('../games.json') as game_data:
    games = json.load(game_data)

twitch = NTC.TwitchApi()

for f in os.listdir("../csv/"):
    if f.endswith(scan):
        print(f)
        with open('../csv/'+f, 'r') as csvfile:
            reader = csv.reader(csvfile)
            # Handle headers
            header = reader.__next__()
            for row in reader:
                if row[3] != "NULL":
                    if not row[3] in games:
                        new_game = twitch.GetGames(gid=row[3])
                        games[row[3]] = new_game.json()

with open('../games.json', 'w') as data_file:
        json.dump(games, data_file)