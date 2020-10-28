import os
import noise
import random
import math
import time
import subprocess
import json

# map function
def map(_in, _in_min, _in_max, _out_min, _out_max, _clamp) :
    if(_in_min == _in_max) :
        return None
    if(_clamp) :
        if(_in <= _in_min) :
            return _in_min
        if(_in >= _in_max) :
            return _in_max
    return ((_out_max-_out_min) * _in + _out_min * _in_max - _in_min * _out_max) / (_in_max - _in_min)

# set baseDebug from name of file
baseDebug = "[{}]\t".format(__file__.split(".")[1][1:])

# read json config file
with open('../../DATA/installationData/config.json', 'r') as f:
    config = json.load(f)

# read json info file and store data
with open('../../DATA/installationData/info.json') as f:
    media_files_info = json.load(f)["media_files_info"]

# init variables
time_to_end         = 0.0
loop_count          = 0
noise_x             = random.uniform(0, 9999)
video_history       = []
audio_history       = []
pick_audio          = False
wait_time           = config["wait_min"]
wait_step_num       = int(random.uniform(config["wait_step_min"], config["wait_step_max"]))
wait_time_target    = random.uniform(config["wait_min"], config["wait_max"])
wait_step           = (wait_time_target - wait_time) / wait_step_num
wait_step_count     = 0

# get list of files
media_files = os.listdir(config["media_folder"])

# check if all media files in info file are indeed in media folder
missing_media = False
missing_media_count = 0
for info in media_files_info :
    if(not os.path.exists(config["media_folder"] + info["name"])) :
        missing_media = True
        missing_media_count += 1
        print("{}WARNING!\t[{}] is not present in media folder.".format(baseDebug, info["name"]))

# abort if there is a missing media
if(missing_media) :
    print("{}Can't run installation because there are {} missing media.".format(baseDebug, missing_media_count))
    exit()

# split media in 2 audioclip and video
video_files_info = []
audio_files_info = []
for media in media_files_info :
    if(media["type"] == "video") :
        video_files_info.append(media)
    if(media["type"] == "audioclip") :
        audio_files_info.append(media)

# installation loop
while True:
    # get timing
    loop_time_start = time.time()

    # pick video
    file_name = ""
    first_pass = True
    while (file_name in video_history) or first_pass:
        first_pass = False
        file_to_read = random.choice(video_files_info)
        file_name = file_to_read["name"]

    # pick audio if boolean has been set
    if(pick_audio) :
        first_pass = True
        while (file_name in audio_history) or first_pass:
            first_pass = False
            file_to_read = random.choice(audio_files_info)
            file_name = file_to_read["name"]

        # add audio to history
        audio_history.append(file_name)
        if(len(audio_history) > config["audio_history_size"]) :
            audio_history = audio_history[1:]
    else :
        # add video  to history
        video_history.append(file_name)
        if(len(video_history) > config["video_history_size"]) :
            video_history = video_history[1:]

    # get info about file
    file_duration = file_to_read["duration"]

    # get file size
    file_width = file_to_read["width"]
    file_height = file_to_read["height"]

    # set ratio
    limit_ratio = random.uniform(config["ratio_min"], config["ratio_max"])

    # compute size of window and scale
    video_scale = math.sqrt(limit_ratio * config["screen_width"] * config["screen_height"] / (file_width * file_height))
    if(file_to_read["type"] == "audioclip") :
        video_scale = 1.0

    # compute position of window
    video_pos_x = int(random.uniform(config["border_window_x"], config["screen_width"] - file_width * video_scale - config["border_window_x"]))
    video_pos_y = int(random.uniform(config["border_window_y"], config["screen_height"] - file_height * video_scale - config["border_window_y"]))
    if(file_to_read["type"] == "audioclip") :
        print("audio")
        video_pos_x = int((config["screen_width"] - file_width) * 0.5)
        video_pos_y = int((config["screen_height"] - file_height) * 0.5)

    # set loop number
    num_loop = 1
    if (file_duration <= 5):
    	num_loop = 3
    elif (file_duration > 5 and file_duration <= 10):
    	num_loop = 2

    # run video player
    video_command = [config["oF_app"], file_name, str(num_loop), str(video_scale), str(video_pos_x), str(video_pos_y)]
    subprocess.Popen(video_command)
    #print(video_command)

    # set times
    video_duration = num_loop * file_duration
    time_to_end += max(0.0, video_duration + config["video_player_time_launch"] - time_to_end)

    # if we are playing an audio file, we wait until the end of the file 2 times in a row
    if(pick_audio) :
        wait_time_actual = time_to_end
    else :
        # perform wait time increase
        wait_time += wait_step
        wait_step_count += 1

        # if we arrived at destination, reset target
        if(wait_step_count == wait_step_num + 1) :
            wait_time           = wait_time_target
            wait_step_num       = int(random.uniform(config["wait_step_min"], config["wait_step_max"]))
            wait_time_target    = random.uniform(config["wait_min"], config["wait_max"])
            wait_step           = (wait_time_target - wait_time) / wait_step_num
            wait_step_count     = 0

        #
        wait_time_actual = wait_time

    # reset pick_audio
    pick_audio = False

    # low probability of audio file
    if(random.uniform(0, 1) < config["audio_prob"]) :
        pick_audio = True
        wait_time_actual = time_to_end

    # debug
    print("{}[{}]\tduration = {}\tloops = {}\ttotal duration = {}".format(baseDebug, file_name, file_duration, num_loop, video_duration))
    #print("{}[{}]\tdimension = ({}, {})".format(baseDebug, file_name, file_width, file_height))
    #print("{}[{}]\tscale = {}".format(baseDebug, file_name, video_scale))
    print("{}[{}]\ttime to end = {}".format(baseDebug, file_name, time_to_end))
    print("{}[{}]\twaiting {} seconds".format(baseDebug, file_name, wait_time_actual))
    if(pick_audio):
        print("{}[{}]\tnext media is audio".format(baseDebug, file_name))
    #print("[runInstallation]\twait [{}] seconds".format(wait_time))

    # wait
    time.sleep(wait_time_actual)

    # get timing
    loop_time_end =  time.time()
    loop_duration = loop_time_end - loop_time_start
    time_to_end -= loop_duration
    time_to_end = max(0.0, time_to_end)
