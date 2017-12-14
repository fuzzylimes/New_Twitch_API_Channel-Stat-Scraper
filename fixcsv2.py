import os
import csv
import shutil
from tempfile import NamedTemporaryFile
import datetime

UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()

for file in os.listdir("./csv/"):
    print(file)
    if file.endswith(".csv"):
        tempfile = NamedTemporaryFile(mode="w", delete=False)
        with open('./csv/'+file, 'r') as csvfile, tempfile:
            reader = csv.reader(csvfile)
            writer = csv.writer(tempfile)

            # Handle headers
            header = reader.__next__()
            writer.writerow(header)

            for row in reader:
                if not row[0].endswith("Z"):
                    string_date = datetime.datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%S.%f")
                    string_date = string_date + UTC_OFFSET_TIMEDELTA
                    row[0] = string_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                writer.writerow(row)
        shutil.move(tempfile.name, './csv/'+file)
