#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zenghanming@kuailekaigong.com'
__version__ = '$Rev$'
__doc__ = """functions for getting specific data """

import re
import test_agent

def get_platform(line):
    """
    Input: string
    Processing: Get platform from the string
    Output: return a platform list
    """
    platform_list= []
    a = test_agent.test_platform(line)
    platform_list += [a]
    return platform_list[0]

def get_browser(line):
    """
    Input: string
    Processing: Get browser from the string
    Output: return a browser list
    """
    browser_list = []
    a = test_agent.test_browser(line)
    browser_list += [a]
    return browser_list[0]

def get_URI(line):
    """
    Input: line
    Processing: get the URI from each string in the list
    Output: return a URI list
    """
    pattern = re.compile(r'".* (?P<path>[^ ]+) .*"')
    m = pattern.match(line)
    if m:
        path = m.groupdict()['path']
        return path
    return ''

def get_request_body(line):
    """
    Input: one request body
    Processing: extract the elment and its value and make the whole thing into a dictionary
    Output: a dictionary
    """
    if "\\x" in line:
        return{}
    #rule that gets the key
    r1 = r'([^\'\[\]]+)=.*'
    rule1 = re.compile(r1)
    #rule that gets the value
    r2 = r'.+=([^\[\'\]]*)'
    rule2 = re.compile(r2)
    #split into a list
    new_list = line.split("&")
    key_list = []
    value_list = []
    request_body = {}
    for item in new_list:
        key_list += rule1.findall(item)
        value_list += rule2.findall(item)

    request_body = {}

    if "=" in line:
        for j in value_list:
            if "head_image" in j or len(j)>1500:
                loc = value_list.index(j)
                value_list.remove(j)
                key_list.remove(key_list[loc])
        for k in key_list:
            if "." in k or len(k)>50:
                loc = key_list.index(k)
                key_list.remove(k)
                value_list.remove(value_list[loc])
        for k in key_list:
            if "." in k or len(k)>40:
                loc= key_list.index(k)
                key_list.remove(k)
                value_list.remove(value_list[loc])
        for i in range(len(key_list)):
            request_body[key_list[i]] = value_list[i]
            i = i+1
        return request_body
    else:
        return request_body

def get_referer(line):
    """
    Input: log file line
    Processing: extract referer from item
    Output: a referer list
    """
    #rule that gets the referer's url
    url_rule = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.IGNORECASE)
    if ("weibo" in line) or ("Weibo" in line):
        return "Weibo"
    else:
        referer_list = url_rule.findall(line)
        if referer_list != []:
            referer =referer_list[0]
            return referer
        else:
            return "[-]"

