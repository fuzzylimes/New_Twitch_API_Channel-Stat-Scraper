A simple twitch scraping program that will continuously run and log information about twitch streams. All API calls use the "New" Twitch API.

## Pre-reqs
* You've aleady created a developer account on Twitch
* You've registerd your "app" and have access to a Twitch O_AUTH, SECRET, and CLIENT_ID

## Usage
All collected data will be placed into a generated csv file with the name of corresponding stream. Data from each polling period is added to the end of the file.

1. Create a creds.py file with the following parameters defined:
  * CLIENT_ID
  * O_AUTH
  * SECRET
2. Edit the included streams.json file to include all stream names you want to collect data from
3. Schedule a task to start the script every 5 minutes to collect data

## Collected data
Currently the script is set up to log the following items for each steam in the streams.json file:
* log_time 
* channel_name
* channel_id
* game_id
* game_name
* viewers
* started
* chatters
* view_count
* follower_count (currently not supported by "New API")

## Planned To-Do
1. Add in support to collect follower_count once it's been added to the "New" API (twitch staff says Soon.&trade;)
2. Add in rollowing logs for each month.