import os
import re
import datetime
import shutil

# set folders and files
fileNames = "../../DATA/facebookMP4Files.txt"
folderToSave = "../../DATA/FacebookMP4/"

# variable that will hold the total length in second of the vocal messages
totSecondsVoc = 0
noDateIncr = 0
fileTot = 0

# read file
with open(fileNames, 'r') as f :
    lines = f.readlines()

    for l in lines :
        fileTot += 1

        filePath = l.strip('\n')
        fileSplitted = filePath.split("/")

        fileName = fileSplitted[-1]
        fileName = fileName.split("_")[0]

        filePerson = fileSplitted[-3]
        filePerson = filePerson.split("_")[0]

        fileDatetime = ""
        fileType = ""
        fileLengthSeconds = -1

        match = re.match(r"([a-z]+)([0-9]+)", fileName, re.I)
        if match:
            fileName = match.groups()
            fileType = fileName[0]
            fileDateTimestamp = int(fileName[1][:10])
            fileDatetime = datetime.datetime.fromtimestamp(fileDateTimestamp).strftime("%d-%m-%Y_%Hh%M")
            if fileType == "audioclip" :
                fileLengthSeconds = int(int(fileName[1][13:-1]) / 100)
                fileDatetime += "_" + str(fileLengthSeconds)
                totSecondsVoc += fileLengthSeconds
        else:
            noDateIncr += 1
            fileDatetime = "NODATE" + str(noDateIncr)
            fileType = "video"

        #
        newFileName = "{}_{}_{}_{}.mp4".format(fileType, filePerson, fileTot, fileDatetime)

        #
        #shutil.copy(filePath, folderToSave + newFileName)

print(totSecondsVoc)
