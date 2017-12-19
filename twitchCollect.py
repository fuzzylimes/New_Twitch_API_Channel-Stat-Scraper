import requests, json, csv
import os.path, datetime
import newTwitchClient as NTC

with open('streams.json') as json_data:
    channels = json.load(json_data)

with open('games.json') as game_data:
    games = json.load(game_data)

rec_length = len(games)

twitch = NTC.TwitchApi()
for stream in channels['channels']:
    print("Collecting " + stream)
    status = twitch.GetChannelInfo(login=stream)
    if not "response" in status:
        status = status['data'][0]
        game_id = status['game_id']
        count = twitch.GetFollowers(status['user_id'])

        # Check to see if the game is already in our saved games list
        if game_id in games:
            game_name = games[game_id]['data'][0]['name']
        else:
            game_res = twitch.GetGames(gid=game_id)
            games[game_id] = game_res.json()
            game_name = game_res.json()['data'][0]['name']
        
        info = {
            "channel_name": stream,
            "channel_id": status['user_id'],
            "game_id": game_id,
            "game_name": game_name,
            "viewers": status['viewer_count'],
            "started": status['started_at'],
            "chatters": twitch.GetChatters(stream)['chatter_count'],
            "log_time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "view_count": twitch.GetUserInfo(stream)['data'][0]['view_count'],
            "follower_count": count
        }
    else:
        info = {
            "channel_name": stream,
            "channel_id": "NULL",
            "game_id": "NULL",
            "game_name": "NULL",
            "viewers": "NULL",
            "started": "NULL",
            "chatters": twitch.GetChatters(stream)['chatter_count'],
            "log_time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "view_count": twitch.GetUserInfo(stream)['data'][0]['view_count'],
            "follower_count": "NULL"
        }

    if not os.path.exists("csv"):
        os.makedirs("csv")
    file_name = stream + "-" + str(datetime.datetime.now()).split()[0][:7]
    file_exists = os.path.isfile("csv/{}.csv".format(file_name))
    with open('csv/{}.csv'.format(file_name), 'a') as csvfile:
        fieldnames = ["log_time", "channel_name", "channel_id", "game_id", "game_name", "viewers", "started", "chatters", "view_count", "follower_count"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(info)
    
    print("Finished " + stream)

if len(games) > rec_length:
    with open('games.json', 'w') as data_file:
        json.dump(games, data_file)