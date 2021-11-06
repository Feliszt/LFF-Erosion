#
#   This script copies video files found in conversastions in facebook data folders
#

import os
from datetime import datetime
from shutil import copyfile
import random

# windows to unix path
def win2unix(_pathin) :
    return "/mnt/d/" + '/'.join(_pathin.split('/')[1:])

# folders
folder_to_search_name = "13-10-2020"
media_type = "audio"
media_extension = ".mp4" if media_type == "videos" else ".wav"
folder_to_populate = "D:/PERSO/_CREA/LFF-Erosion/_DEV/DATA/allFacebookVideos/"
folder_to_search = "D:/PERSO/_DATA/FacebookData/" + folder_to_search_name + "/messages/"

# linux
if(os.name == 'posix') :
    folder_to_search = win2unix(folder_to_search)
    folder_to_populate = win2unix(folder_to_populate)

print(folder_to_search)

# recursive folder search
incr = 0
for x in os.walk(folder_to_search) :
    sub_folder = x[0].split('/')

    # videos are found for this conversation folder
    if sub_folder[-1] == media_type :
        conv_name = sub_folder[-2].split('_')[0]
        print(conv_name)

        # loop through videos
        iter = 1
        for y in x[2] :
            print(y)
            continue

            media_timestamp = int(y.split('_')[0][5:]) if media_type == "video" else int(y.split('_')[0][5:])
            video_date = datetime.fromtimestamp(video_timestamp).strftime("%d-%m-%Y_%Hh%Mm%Ss")
            rand_id = ''.join(str(i) for i in random.sample(range(0, 9), 4))
            new_filename = '_'.join(["video", conv_name, video_date, rand_id])
            print("\t" + str(iter) + "\t" + new_filename)
            #print("\t" + y + "\t" + video_date)

            full_file_path = '/'.join([x[0], y])
            new_file_path = ''.join([folder_to_populate, new_filename, media_extension])
            #copyfile(full_file_path, new_file_path)

            incr = incr + 1
            iter = iter + 1
            prev_name = new_filename

print(str(incr) + " files copied.")
