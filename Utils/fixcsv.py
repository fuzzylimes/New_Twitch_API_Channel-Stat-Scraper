import os
import csv
import shutil
from tempfile import NamedTemporaryFile
import datetime

UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()

for file in os.listdir("../csv/"):
    print(file)
    if file.endswith(".csv"):
        tempfile = NamedTemporaryFile(mode="w", delete=False)
        with open('../csv/'+file, 'r') as csvfile, tempfile:
            fieldnames = ["log_time", "channel_name", "channel_id", "game_id", "game_name", "viewers", "started", "chatters", "view_count", "follower_count"]
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            writer = csv.DictWriter(tempfile, fieldnames=fieldnames)

            # Handle headers
            reader.__next__()
            writer.writeheader()

            for row in reader:
                if not row['log_time'].endswith("Z"):
                    string_date = datetime.datetime.strptime(row['log_time'], "%Y-%m-%dT%H:%M:%S.%f")
                    string_date = string_date + UTC_OFFSET_TIMEDELTA
                    row['log_time'] = string_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                row = {"log_time": row["log_time"], "channel_name": row["channel_name"], "channel_id": row["channel_id"], "game_id": row["game_id"], "game_name": row["game_name"], "viewers": row["viewers"], "started": row["started"], "chatters": row["chatters"], "view_count": row["view_count"], "follower_count": row["follower_count"]}
                writer.writerow(row)
        shutil.move(tempfile.name, '../csv/'+file)
