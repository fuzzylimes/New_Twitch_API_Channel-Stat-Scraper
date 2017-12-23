import csv, itertools
import os, sys
import htmlBlocks
import datetime
import json

if not os.path.exists('../html'):
    os.makedirs('../html')

if not os.path.exists('../json'):
    os.makedirs('../json')

with open('../games.json') as game_data:
    games = json.load(game_data)

month = str(datetime.datetime.now()).split()[0][:7]

for file in os.listdir("../csv/"):
    print(file)
    if file.endswith(month+".csv"):
        json_records = []
        json_day_records = []
        f_name = file.split('-')[0]
        html_file_name = file.split('.')[0]
        with open('../csv/'+file, 'r') as csvfile:
            games_played = []
            last_played = "NULL"
            last_data = ""
            start_time = ""
            end_time = ""
            max_views = 0
            max_chat = 0
            game_number = 0
            group_date = ""
            log_dict = {}
            temp = csv.reader(csvfile)
            temp.__next__()
            # for line in itertools.islice(temp, 260):
            for line in temp:
                key_date = line[0]
                if line[4] != last_played:

                    # Previous record was NULL
                    if last_played == "NULL":
                        group_date = key_date
                        log_dict[group_date] = {}
                        game_number += 1
                        last_played = line[4]
                        last_data = line
                        start_time = line[0]
                        end_time = line[0]
                        max_views = max(0, int(line[5]))
                        max_chat = max(0, int(line[7]))
                        log_dict[group_date][game_number] = {}
                        log_dict[group_date][game_number]['game_name'] = line[4]
                        log_dict[group_date][game_number]['game_number'] = line[3]
                        log_dict[group_date][game_number]['start_time'] = start_time
                        log_dict[group_date][game_number]['end_time'] = end_time
                        log_dict[group_date][game_number]['max_views'] = max_views
                        log_dict[group_date][game_number]['max_chat'] = max_chat
                    # Previous record was NOT null (i.e. game change or stream end)
                    else:
                        if line[4] != "NULL":
                            log_dict[group_date][game_number]['end_time'] = line[0]
                            game_number += 1
                            last_played = line[4]
                            last_data = line
                            start_time = line[0]
                            end_time = line[0]
                            max_views = max(0, int(line[5]))
                            max_chat = max(0, int(line[7]))
                            log_dict[group_date][game_number] = {}
                            log_dict[group_date][game_number]['game_name'] = line[4]
                            log_dict[group_date][game_number]['game_number'] = line[3]
                            log_dict[group_date][game_number]['start_time'] = start_time
                            log_dict[group_date][game_number]['end_time'] = end_time
                            log_dict[group_date][game_number]['max_views'] = max_views
                            log_dict[group_date][game_number]['max_chat'] = max_chat
                        else:
                            log_dict[group_date][game_number]['end_time'] = line[0]
                            game_number = 0
                            last_played = "NULL"
                else:
                    if line[4] != "NULL":
                        last_played = line[4]
                        end_time = line[0]
                        log_dict[group_date][game_number]['end_time'] = end_time
                        max_views = max(max_views, int(line[5]))
                        max_chat = max(max_chat, int(line[7]))
                        log_dict[group_date][game_number]['max_views'] = max_views
                        log_dict[group_date][game_number]['max_chat'] = max_chat

        with open("../html/"+html_file_name+'.html', 'w') as html_doc:
            html = htmlBlocks.html(f_name)
            html_doc.write(html.header(html_file_name))
            html_doc.write(html.streamer())
            for day in sorted(list(log_dict.keys()))[::-1]:
                start_time = ""
                end_time = ""
                game_list = []
                for game in log_dict[day].keys():
                    game_number = log_dict[day][game]['game_number']
                    box = games[game_number]['data'][0]['box_art_url'].format(width="87", height="121")
                    game_list.append(box)
                    if game == 1:
                        stream_start_time = log_dict[day][game]['start_time']
                    end_time = log_dict[day][game]['end_time']
                start_time = datetime.datetime.strptime(stream_start_time, "%Y-%m-%dT%H:%M:%SZ")
                end_time = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
                uptime = str(end_time - start_time)

                html_doc.write(html.body_one(day, uptime, game_list))

                for game in log_dict[day].keys():
                    game_name = log_dict[day][game]['game_name']
                    game_number = log_dict[day][game]['game_number']
                    box = games[game_number]['data'][0]['box_art_url'].format(width="87", height="121")
                    start_time = log_dict[day][game]['start_time']
                    end_time = log_dict[day][game]['end_time']
                    stream_start_time2 = datetime.datetime.strptime(stream_start_time, "%Y-%m-%dT%H:%M:%SZ")
                    start_time2 = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
                    end_time2 = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
                    playtime = str(end_time2 - start_time2)
                    start_time_in_stream = str(start_time2 - stream_start_time2)
                    end_time_in_stream = str(end_time2 - stream_start_time2)

                    html_doc.write(html.body_two(box, game_name, playtime, start_time, start_time_in_stream, end_time, end_time_in_stream, log_dict[day][game]['max_views'], log_dict[day][game]['max_chat']))

                    json_records.append({
                        'start_time': start_time,
                        'end_time': end_time,
                        'game_name': game_name,
                        'game_number': game_number,
                        'playtime': playtime,
                        'box': box,
                        'start_tis': start_time_in_stream,
                        'end_tis': end_time_in_stream,
                        'max_views': max_views,
                        'max_chat': max_chat
                    })
                
                html_doc.write(html.body_three())

                json_day_records.append({'session': day, 'uptime': uptime, 'data': json_records})
                json_records = []

            html_doc.write(html.footer())
        
        with open("../json/"+html_file_name+'.json', 'w') as json_doc:
            json.dump(json_day_records, json_doc)