This is a collection of small utilities that were created while working on this project. Some have one-off uses to correct issues created in earlier versions, some are full fledged tools that enhance the project.

# Tools
## `buildHtml.py`
Used to generate html like report pages based on the data from generated csv files. This script was originally created with the intention of generating my static web pages for me, pulling the csv data after every update and regenerating the entire html page.

When run, the script will scan across all of the csv files that are in `../csv/` folder and genearte an html file of the same name as the existing csv file. If the html file already exists, the file is overwritten.

The generated html report has a summary section at the top for the stream's information, and then a series of cards below it to show all games played during a _specific game session_. The cards can then be expanded to reveal information like the play time of a specific game, the number of max numbers of viewers and chatters, and other info.

This file relies on the helper file `htmlBlocks.py` to run. Info on this helper file can be found in the next section below.

 ### Usage
The script must be run from within the Utils server folder. To use, run the following command:

`python3 buildHtml.py`

## `htmlBlocks.py`
This is a helper file for `buildHtml.py`. It provides the required class and methods needed to generate each of the pieces of the html report. Each section of the html report is broken down into sections which have each been given their own method.

The main class, `html`, creates an instance of the Twitch scraper so that it can grab extra information about the streamer as needed.

This file is used via `buildHtml.py` and is not intended to be used on its own.

## `parsecsv.py`
This file expanded on the functionality brought with `buildHtml.py`. Rather than generating an html report, this would generate json files with the data that would have been going into those html reports. This data was then posted to a remote mongodb instance.

When the script is run, it will read through each of the csv files that are present in the `.csv` folder. The script will create a python dictionary that will contain an entry for each of the stream sessions found. A session is defined by concurrent records until a NULL record was found. These records would then be written to a `.json` file with the same year and month of the original html file.

At the same time, the streamer's information will be collected and it will be saved off into a `streams.json` file. This can be used to get info on a streamer without needing to poll the twitch server for it (things like icon links that don't change as often).

### Usage
To use the script as is, a few things are needed:
* The script must be run from within the Utils server folder.
* In order to be used, the `../creds.py` file will need to be updated with extra parameters to connect to your database. This script was writen to connect to a remote mongodb instance, so the required credentials are based on that. These parameters are:
   1. MONGO_SERVER
   2. MLAB_ADMIN
   3. MLAB_ADMIN_PASS
   4. MLAB_USER
   5. MLAB_USER_PASS
* Mongodb 3.4+ has been installed on the system where this is running

> Note: If you don't want to save to a database, you can comment out the very last for loop in the file

To use, run the following command:
`python3 parsecsv.py`

## `parsehelper.py`
Helper file for `parsecsv.py`. It's entire purpose is to provide the logic for getting information about the stream that is being parsed. Using this file will return back an objet with stream specific information that will be included in the `streams.json` file.

This file is used via `buildHtml.py` and is not intended to be used on its own.

# One-Offs
## `fixcsv.py`
Script that would correct the `log_time` value in existing csv files. The `log_time` value had originally been saved in long EST format. This was later changed to match the time returned from Twitch in the `start_time` field: `2017-12-06T02:20:09Z`.

This script does exactly the same thing as `fixcsv2.py`, only it does so by using dictReader instead of csvReader.

 ### Usage
The script must be run from within the Utils server folder. To use, run the following command:

`python3 fixcsv2.py`

## `fixcsv2.py`
Script that would correct the `log_time` value in existing csv files. The `log_time` value had originally been saved in long EST format. This was later changed to match the time returned from Twitch in the `start_time` field: `2017-12-06T02:20:09Z`.

This script does exactly the same thing as `fixcsv.py`, only it does so by using csvReader instead of dictReader.

 ### Usage
The script must be run from within the Utils server folder. To use, run the following command:

`python3 fixcsv2.py`

## `fixCsvName.py`
Script that corrected the names of generated csv files. Originally csv files were generated without a month identifier on them. After implementing a roll-over system, the `YYYY-MM` were added to the end of the csv names.

### Usage
The script must be run from within the Utils server folder. To use, run the following command:

`python3 fixCsvName.py`

## `gamescan.py`
Script that was used to populate the `games.json` file with missing games found in generated `.csv` files.

This file will load the contents of the `../games.json` file, then scan through every one of the `.csv` files in the `../csv/` folder. Each line in each csv file will be scanned. If the record has a game saved to it, the script will check to see if it's saved in the games file. If not, a req is sent to the Twtich API to collect data on the game, and it will be added to the `games.json` file.

### Usage
The script must be run from within the Utils server folder. To use, run the following command:

`python3 gamescan.py`