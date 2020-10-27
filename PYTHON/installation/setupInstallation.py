import os
import subprocess
import json
import cv2
import math

# function that gets the duration of a video file
def get_duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

# set baseDebug from name of file
baseDebug = "[{}]\t".format(__file__.split(".")[1][1:])

# read json config file
with open('../../DATA/installationData/config.json', 'r') as f:
    config = json.load(f)

# get list of files
media_files = os.listdir(config["media_folder"])

# init variables
media_files_info_json = {}
media_files_info = []

# loop through all files
for file in media_files :
    # check if not media file
    if(file.split(".")[-1] != "mp4"):
        continue

    # get file type
    file_type = file.split("_")[0]

    # get length of media file
    file_duration = get_duration(config["media_folder"] + file)

    # get size of media file
    cv2_vid = cv2.VideoCapture(config["media_folder"] + file)
    file_width = int(cv2_vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    file_height = int(cv2_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # set json data
    file_info = {}
    file_info["name"]       = file
    file_info["type"]       = file_type
    file_info["duration"]   = file_duration
    file_info["width"]      = file_width
    file_info["height"]     = file_height
    media_files_info.append(file_info)

    # debug
    print("{}[{}]".format(baseDebug, file))
    print("{}type = {}".format(baseDebug, file_type))
    print("{}duration = {}".format(baseDebug, file_duration))
    print("{}size = ({}, {})".format(baseDebug, file_width, file_height))
    print("{}".format(baseDebug))

# set json data
media_files_info_json["media_files_info"] = media_files_info

# wrote json info file
with open('../../DATA/installationData/info.json', 'w') as f:
    json.dump(media_files_info_json, f)
