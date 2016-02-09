#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zenghanming@kuailekaigong.com'
__version__ = '$Rev$'
__doc__ = """ parse and add data to mongodb m"""

import pymongo
import re
import json
import sys
import logging
import os
import datetime
import schema
import datetime
from django.conf import settings
from config import codes
import tailer
import time

logger = logging.getLogger(__name__)

#get date in the filename
today = datetime.date.today()
today = today.strftime("%Y%m%d")
client = pymongo.MongoClient()
#creat database and collection
db = client['log']
col = 'event_'+ today
pattern = re.compile(r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (?P<request_time>[0-9\.]+|-) (?P<response_time>[0-9\.]+|-) (?P<local_time>\[[0-9a-zA-z:/+ ]+\]) (?P<host>[0-9a-zA-z\.]+) (?P<request>\".+\") (?P<status>[0-9]+|-) (?P<bytes>[0-9]+|-) (?P<request_body>\[.+\]) (?P<referer>\[.+\]) (?P<agent>\[.+\]) (?P<forward>\[.+\])')

def parse_log_file(filename):
    num = 0
    f = open(filename)
    while True:
        line = f.readline()
        if not line:
            break
        else:
            parse_line(line)
            num += 1
    f.close()

def parse_real_time(filename):
    num = 0
    for line in tailer.follow(open(filename)):
        parse_line(line)
        num = num + 1
        logger.info("Successfully imported",num,"lines to mongo")

def parse_line(line):
    record = {}
    line = line.strip()
    # add the parser function
    result = pattern.match(line)
    if result:
        parameter = result.groupdict()
        if not parameter:
            return
        if parameter:
            # filter invalid domain
            domain = parameter['host']
            if domain not in ['api.kuailekaigong.com', 'www.kuailekaigong.com']:
                return
            # merge
            record.update(parameter)
            del record['request']
            del record['request_body']
            del record['agent']
            del record['referer']
            # parse path
            path = parameter['request']
            new_path = schema.get_URI(path)
            if not new_path:
                return
            record['path'] = new_path
            #parse request_body
            request_body = parameter['request_body']
            new_request_body = schema.get_request_body(request_body)
            record.update(new_request_body)
            #parse browser
            browser = parameter['agent']
            browser_name = schema.get_browser(browser)
            browser_os = schema.get_platform(browser)
            if not browser_name or not browser_os:
                return
            record['browser_name'] = browser_name
            record['browser_os'] = browser_os
            # convert time string to float
            time1 = record['request_time']
            time2 = record['response_time']
            if time1.replace('.','').replace('-','').isdigit():
                record['request_time'] = float(time1)
            if time2.replace('.','').replace('-','').isdigit():
                record['response_time'] = float(time2)
            #parse referer
            referer = parameter['referer']
            new_referer = schema.get_referer(referer)
            record['referer'] = new_referer
            db[col].insert(record)
    else:
        return
