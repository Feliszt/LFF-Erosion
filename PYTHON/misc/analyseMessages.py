#!/usr/bin/env python
# coding: utf-8

from datetime import datetime
import json
import math
import ftfy
import os

# function
def getReadableTime (tt):
    dd = math.floor(tt / (3600*24))
    rem = tt % (3600*24)
    hh = math.floor(rem / 3600)
    rem = rem % 3600
    mm = math.floor(rem / 60)
    ss = math.floor(rem % 60)
    res = '%02d:%02d:%02d:%02d' % (dd, hh, mm, ss)
    return res

# init variables
folderName = "D:/PERSO/_DATA/FacebookData/13-10-2020/messages/inbox/ninamo_iq95yegzaw/"
data = []
limit = "05:00:00:00"
limit_ms = 0
sendersGlobal = {}
sendersWords = {}
sendersOverLimit = {}
responseTimes = {}
averageResponseTimes = {}
maxTime = 0
numOverLimit = 0

# process limit
temp = limit.split(":")
limit_ms = int(temp[0]) * 86400 + int(temp[1]) * 3600 + int(temp[2]) * 60 + int(temp[3])
limit_ms *= 1000

# get json files
json_files = []
for file in os.listdir(folderName) :
    if file.endswith(".json") :
        json_files.append(folderName + file)

# concatenate json data
messages_data = []
for file in json_files :
    with open(file, 'r') as f:
        data = json.load(f)
        for mess in data["messages"]:
            messages_data.append(mess)

nbMess = len(messages_data)

for x in range(nbMess-1):
    # get times
    timestamp1 = messages_data[x]['timestamp_ms']
    timestamp2 = messages_data[x+1]['timestamp_ms']

    # get senders
    messSender = ftfy.fix_text(messages_data[x]['sender_name'])
    prevmessSender = ftfy.fix_text(messages_data[x+1]['sender_name'])

    # get number of words
    message = ""
    if('content' in messages_data[x]) :
        message = ftfy.fix_text(messages_data[x]['content'])

    # update global senders
    if(messSender not in sendersGlobal):
        sendersGlobal[messSender] =  1
        sendersWords[messSender] = 0
    else:
        sendersGlobal[messSender] = sendersGlobal[messSender] + 1
        sendersWords[messSender] = sendersWords[messSender] + len(message.split())

    # compute diff
    diff = timestamp1 - timestamp2

    # append response times
    if(messSender != prevmessSender):
        if(messSender not in responseTimes):
            responseTimes[messSender] = [diff]
        else:
            responseTimes[messSender].append(diff)

    if(diff > limit_ms):
        # increment ind
        numOverLimit += 1

        # get timestamp and senders
        timestamp_s = math.floor(diff / 1000)

        # get max
        if(timestamp_s > maxTime):
            maxTime  = timestamp_s

        # update senders
        if(messSender not in sendersOverLimit):
            sendersOverLimit[messSender] =  1
        else:
            sendersOverLimit[messSender] = sendersOverLimit[messSender] + 1

        # compute readable diff
        res = getReadableTime(timestamp_s)

        # print diff
        print(res)

        # print previous message
        date = datetime.fromtimestamp(math.floor(timestamp2/1000))
        print("\t" + prevmessSender + " @ " + str(date))
        if('content' in messages_data[x+1]) :
            print("\t-> " + ftfy.fix_text(messages_data[x+1]['content']))
        else:
            print("\t-> NO TEXT MESSAGE")

        print("\t|----------------|")

        # print message
        date = datetime.fromtimestamp(math.floor(timestamp1/1000))
        print("\t" + messSender + " @ " + str(date))
        if('content' in messages_data[x]) :
            print("\t-> " + ftfy.fix_text(messages_data[x]['content']))
        else:
            print("\t-> NO TEXT MESSAGE")

        print()

# compute average response times
for x in responseTimes:
    av = 0
    for el in responseTimes[x]:
        av += el
    averageResponseTimes[x] = getReadableTime(math.floor(av / (1000 * len(responseTimes[x]))))

print()
print("NUMBER OF MESSAGES TOTAL")
print(nbMess)
print()
print("NUMBER OF MESSAGES OVER LIMIT")
print(numOverLimit)
print()
print("NUMBER OF MESSAGES SENT")
print(sendersGlobal)
print()
print("NUMBER OF WORDS SENT")
print(sendersWords)
print()
print("FIRST SENDERS")
print(sendersOverLimit)
print()
print("LONGEST TIME WITH NO MESSAGES")
print(getReadableTime(maxTime))
print()
print("AVERAGE RESPONSE TIMES")
print(averageResponseTimes)
