import datetime
import os, sys

month = str(datetime.datetime.now()).split()[0][:7]

for csvFile in os.listdir("../csv/"):
    print(csvFile)
    if csvFile.endswith(".csv"):
        csvFile_name = csvFile.split('.')[0]
        os.rename("../csv/"+csvFile, "../csv/"+csvFile_name + "-" + month + ".csv")