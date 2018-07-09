#!/usr/bin/python
import sys
import re
import requests
import json
import datetime
import dateutil.relativedelta
r"""
Title: TimeCamp API
Author: Alex Cooper
Date: 07/09/2018
"""

def set_dates():

    ###########################
    # Set start and end dates #
    ###########################
    now = datetime.datetime.now()
    start_date = now - dateutil.relativedelta.relativedelta(months=1)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = now
    end_date = end_date.strftime("%Y-%m-%d")
    return start_date,end_date

def create_url(url,ids,apikey,start_date,end_date):

    ############
    # Make URL #
    ############
    url = url.replace("{apikey}", apikey)
    url = url.replace("{user_ids}", ids)
    url = url.replace("{start_date}", str(start_date))
    url = url.replace("{end_date}", str(end_date))
    return url

def parse_json(json_string,report):

    #####################
    # Parse JSON object #
    #####################
    user_name = ""
    delim = "|"
    parsed_json = json.loads(json_string)
    for line in parsed_json:
        user_name = line['user_name']
        start = line['start_time']
        end = line['end_time']
        name = line['name']
        date = line['date']
        duration = datetime.datetime.strptime(end, "%H:%M:%S") - datetime.datetime.strptime(start, "%H:%M:%S")
        duration = duration / 60
        duration = str(duration)
        report.append(user_name + delim + date + delim + name + delim + start + delim + end + delim + duration)
    return report

def main():

    url = "https://www.timecamp.com/third_party/api/entries/format/json/api_token/{apikey}/from/{start_date}/to/{end_date}/user_ids/{user_ids}"
    elizabeth_id = elizabeth_api = alex_id = alex_api = lisa_id = lisa_api = ""
    report = []
    delim = "|"
    report.append("User Name" + delim + "Date" + delim + "Task Name" + delim + "Start Time" + delim + "End Time" + delim + "Duration")
    ###########################
    # Read configuration file #
    ###########################
    config = open("/home/alex/bincustom/files/timecamp_apis.cfg", "r")
    pat = re.compile("(.*?)=(.*)")
    for line in config:
        line = line.rstrip("\n")
        m = pat.match(line)
        if m:
            if m.group(1) == "lisa_id":
                lisa_id = m.group(2)
            if m.group(1) == "lisa_api":
                lisa_api = m.group(2)
            if m.group(1) == "alex_id":
                alex_id = m.group(2)
            if m.group(1) == "alex_api":
                alex_api = m.group(2)
            if m.group(1) == "elizabeth_id":
                elizabeth_id = m.group(2)
            if m.group(1) == "elizabeth_api":
                elizabeth_api = m.group(2)
    start_date,end_date = set_dates()
    if lisa_id and lisa_api:
        url1 = create_url(url,lisa_id,lisa_api,start_date,end_date)
        r = requests.get(url1)
        result = parse_json(r.text,report)
    if alex_id and alex_api:
        url2 = create_url(url,alex_id,alex_api,start_date,end_date)
        r = requests.get(url2)
        result = parse_json(r.text,report)
    if elizabeth_id and elizabeth_api:
        url3 = create_url(url,elizabeth_id,elizabeth_api,start_date,end_date)
        r = requests.get(url3)
        result = parse_json(r.text,report)
    for line in result:
        print line

if __name__=="__main__":
    sys.exit(main())
