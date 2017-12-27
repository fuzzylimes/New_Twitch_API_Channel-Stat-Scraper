A simple twitch scraping program that will continuously run and log information about twitch streams. All API calls use the "New" Twitch API.

## Pre-reqs
* You've aleady created a developer account on Twitch
* You've registerd your "app" and have access to a Twitch O_AUTH, SECRET, and CLIENT_ID
* Python3 is on your system

## Functionality
This README will outline the usage/functionality of the scraping script in this folder. If you're interested in the utilities that expand on the base functionality, check out the related README in this `Utils` folder.

### File Structure
The mail file that is run to collect data is `twitchCollect.py`. This file uses values from the following files in order to do it's magic:

1. `newTwitchClient.py` - Main helper file for the scraper. This contians all of the base functions for contacting the twitch server. Used to create a new `TwitchApi` object using your stored credetials from the `creds.py` file.
2. `creds.py` - Stores all of your credentails needed for contacting twitch servers. You will need to manually create this file and add the required parameters. To use the scraper, you will need three pieces of information added to this file:
   * CLIENT_ID
   * O_AUTH
   * SECRET
3. `streams.json` - List of all streams to be scanned. Provide the user name (i.e. name in the steamers url) in the list like shown in the example file.
4. `games.json` - Used to "cache" searched games. This reduces the number of REST calls to the Twitch servers to get all of the needed information.

When `newTwitchClient.py` is run, the tool will loop through each of the streams provided in the `streams.json` file one at a time. At the start of the first loop, the tool will check to see if a csv folder is present in the run folder and create one if there isn't. It will then check to see if an existing log file exists for the stream. Stream log files are saved by the month in the following format: `<stream_name>-YYYY-MM.csv`. When the month rolls over, a new file will be created. All csv files contain a hearder on the very first row. If the file already exists, the new data is appeneded to the end.

### csv format
The generated/saved csv files are created using the following csv items in the following order:
* log_time 
* channel_name
* channel_id
* game_id
* game_name
* viewers
* started
* chatters
* view_count
* follower_count

Both the `log_time` and the `started` time are saved in a shortended UTC ISO format like: `2017-12-06T02:20:09Z`.

Most of this data can only be logged if the stream is currently live. If the stream is NOT live, then NULL values will be entered into the record. These records will look like this: `2017-12-06T02:40:11Z,cirno_tv,NULL,NULL,NULL,NULL,NULL,203,12136143,NULL`.

## Usage
Running the `twitchCollect.py` script assumes that the user has installed the required packages from the `requirements.txt` file either globaly or inside of a python3 virtual environment. It is also assumed that the script is being run from within the cloned repo.

To run `twitchCollect.py`, you'll need to do the following:

1. Create a creds.py file with the following parameters defined:
  * CLIENT_ID
  * O_AUTH
  * SECRET
2. Edit the included streams.json file to include all stream names you want to collect data from
3. Run `python3 twitchCollect.py`

In my case, I have set up cronjob to run periodically to collect the data.

## Planned To-Do
1. ~~Add in support to collect follower_count once it's been added to the "New" API (twitch staff says Soon.&trade;)~~
2. ~~Add in rollowing logs for each month.~~