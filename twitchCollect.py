import requests, json, csv
import os.path, datetime
import newTwitchClient as NTC

with open('streams.json') as json_data:
    channels = json.load(json_data)

twitch = NTC.TwitchApi()
for stream in channels['channels']:
    status = twitch.GetChannelInfo(login=stream)
    if not "response" in status:
        status = status['data'][0]
        info = {
            "channel_name": stream,
            "channel_id": status['user_id'],
            "game_id": status['game_id'],
            "game_name": twitch.GetGames(gid="{}".format(status['game_id'])).json()['data'][0]['name'],
            "viewers": status['viewer_count'],
            "started": status['started_at'],
            "chatters": twitch.GetChatters(stream)['chatter_count'],
            "log_time": datetime.datetime.now().isoformat()
        }

        file_exists = os.path.isfile("csv/{}.csv".format(stream))
        with open('csv/{}.csv'.format(stream), 'a') as csvfile:
            fieldnames = ["log_time", "channel_name", "channel_id", "game_id", "game_name", "viewers", "started", "chatters"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(info)