import os
import shutil
import subprocess
import cv2
import math

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

file_path = "./video.avi"  # change to your own video path


# set folder
media_folder = "../../DATA/Pleine-mer_media-files/"

# get list of files
media_files = os.listdir(media_folder)

# create temp folder
if(not os.path.exists(media_folder + "temp/")) :
    os.mkdir(media_folder + "temp/")

# loop through files
for file in media_files :
    # check if not media file
    if(file.split(".")[-1] != "mp4"):
        continue

    # get length of media file
    file_length = math.floor(get_length(media_folder + file))

    # get dimension of media file
    cv2_vid = cv2.VideoCapture(media_folder + file)
    file_width = int(cv2_vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    file_height = int(cv2_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # debug
    #print("file [{}]\tlength = {}\tdimension = ({}, {})".format(file, file_length, file_width, file_height))

    # set new file name
    new_file_name = ""
    if(file.split("_")[0] == "video") :
        new_file_name = "{}_{}_{}-{}.mp4".format(file.split(".")[0], file_length, file_width, file_height)
    else:
        new_file_name = "{}_{}-{}.mp4".format(file.split(".")[0], file_width, file_height)

    # debug
    print("new file name = [{}]".format(new_file_name))

    # copy and rename
    shutil.copy(media_folder + file, media_folder + "temp/" + new_file_name)
