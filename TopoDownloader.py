#!/usr/bin/python3

# TopoDownloader.py

import pandas as pn
import numpy as np
import subprocess
import datetime
import time
import os.path
import logging
import requests
from weightfunctions import read_scale, write_file, get_weather, requests_retry_session, IFTTTmsg, calculate, check_web_response, weather_date_only

try:
    LogFileName = "/home/pi/Documents/Code/Log/Topo.log"
    logger = logging.getLogger("Topo")
    # logger.setLevel(logging.INFO)

    # create the logging file handler
    LogHandler = logging.FileHandler(LogFileName)
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
    LogHandler.setFormatter(formatter)

    # # add handler to logger object
    logger.addHandler(LogHandler)
    logger.info("Program started")

    searchfilepath = "/home/pi/Documents/Code/Topo/LinksbyState/"
    for root, dirs, files in os.walk(searchfilepath):               # gives (dirpath, dirnames, filenames)
        print(root, dirs, files)
        for file in files:
            INPUTFILEPATH = searchfilepath + file
            print(INPUTFILEPATH)
            # INPUTFILEPATH = '/home/pi/Documents/Code/Topo/LinksbyState/topomaps_DC.csv'
            inputfilestatename = INPUTFILEPATH.split("_")
            inputfilestatename = inputfilestatename[1].split(".")
            inputfilestatename = inputfilestatename[0]
            print(inputfilestatename)
            OUTPUTFILEPATH = "/home/pi/Desktop/BOXYtemp/Maps/" + str(inputfilestatename) + "/"
            print(OUTPUTFILEPATH)
            if not os.path.exists(OUTPUTFILEPATH):
                os.makedirs(OUTPUTFILEPATH)
            # use inputfilestatename with index

            filecontents = pn.read_csv(INPUTFILEPATH, delimiter=',')  # , parse_dates=True, dayfirst=False)     #nrows=5
            # print(type(filecontents))
            filecontents.columns = [c.replace(' ', '_') for c in filecontents.columns]      #replace spaces with underscore in column names
            # print(filecontents.columns)
            # print(filecontents.loc[:,["Download GeoPDF"]])

            URL = []
            for row in filecontents.loc[:, ["Download_GeoPDF"]].itertuples():     # get URLs via tuples
                URL.append(row[1])
                # print(URL)

            filecontents = filecontents.loc[(filecontents['Primary_State'] == inputfilestatename) & (filecontents['Version'] == 'Current')]
            # df.loc[(df['column_name'] == some_value) & df['other_column'].isin(some_values)]
            # print(filecontents.info())

            for row in filecontents.itertuples():
                print(row.Version)
                print(row.Primary_State)
                URL = row.Download_GeoPDF
                print(URL)
                outputfile = OUTPUTFILEPATH + str(row.Series) + " " + inputfilestatename + " " + str(row.Date_On_Map) + " " + str(row.Map_Name) + " " + str(row.Scale) + " " + str(row.Cell_ID) + ".pdf"
                print(outputfile)
                if not os.path.exists(outputfile):
                    print(str(row.Map_Name) + "File not already Downloaded")
                    print("Open Website")
                    TopoStringOpen = requests_retry_session().get(URL, timeout=15)
                    # TopoStringOpen=requests.get(URL, stream=True, timeout=15)          #might be less reliable
                    print(TopoStringOpen.status_code)
            #       add error handle for ConnectionTimeout
                    # print(TopoStringOpen.content)
                    if TopoStringOpen:
                        print("Save File")
                        with open(outputfile, 'wb') as file:
                            file.write(TopoStringOpen.content)     # this works with requests_retry_session
                            logger.info(str(row.Map_Name) + "Map Saved")
                            #    Use this for large files
                            # i = 0
                            # for chunk in TopoStringOpen.iter_content(chunk_size=1048576):
                            #     if chunk:
                            #         file.write(chunk)
                            #         print(i)
                            #         i = i + 1
                        print("Wait")
                        time.sleep(5)       # in seconds and accepts floats
                        # break       #use to only download one file for testing
                else:
                    print(str(row.Map_Name) + "File already Downloaded")

except:
    IFTTTmsg("TopoDownloader Exception")
    logging.exception("TopoDownloader Exception")
    raise
    # print("Exception")

finally:
    print("Done")