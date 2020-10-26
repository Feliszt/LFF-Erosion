import os
import random
import time
import subprocess

# init files and folder
media_folder = "../../DATA/Pleine-mer_media-files/"
oF_app = "D:/PERSO/_CREA/Pleine-mer/_DEV/VISUALS/Pleine-mer_videoPlayer/bin/Pleine-mer_videoPlayer.exe"

# get list of files
media_files = os.listdir(media_folder)

while True:
    # pick video
    file_to_read = random.choice(media_files)
    file_length = int(file_to_read.split("_")[-2])

    # set loop number
    num_loop = 1
    if (file_length <= 5):
    	num_loop = 3
    elif (file_length > 5 and file_length <= 10):
    	num_loop = 2

    # debug
    print("[runInstallation]\tsending [{}] to oF with {} loops".format(file_to_read, num_loop))

    # run command
    video_command = "{} {} {}".format(oF_app, file_to_read, num_loop)
    subprocess.Popen([oF_app, file_to_read, str(num_loop)])

    # set wait time
    wait_ratio = random.uniform(0.5, 0.8)
    wait_time = num_loop * file_length * wait_ratio

    # debug
    print("[runInstallation]\twait [{}] seconds".format(wait_time))

    # wait
    time.sleep(wait_time)
