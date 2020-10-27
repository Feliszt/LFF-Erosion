import os
import subprocess
import random

# set folder
media_folder = "../../DATA/Pleine-mer_media-files/"

# get list of files
media_files = os.listdir(media_folder)

# create temp folder
if(not os.path.exists(media_folder + "temp/")) :
    os.mkdir(media_folder + "temp/")

#
command = ""


#
for file in media_files :
    # set random left or right
    vol_left = 0.0
    vol_right = 1.0
    if(random.uniform(0, 1) < 0.5) :
        vol_left = 1.0
        vol_right = 0.0

    # ffmpeg command
    ffmpeg_command = 'ffmpeg -i {} -filter_complex "[0:a]amerge=inputs=1,pan=stereo|FL<{}*c0|FR<{}*c0[a]" -map 0:v -map "[a]" -c:v copy {}'.format(media_folder + file, vol_left, vol_right, media_folder + "temp/" + file)
    os.system(ffmpeg_command)
    print(ffmpeg_command)
