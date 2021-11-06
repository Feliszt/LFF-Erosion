import os
import noise
import random
import math
import time
import datetime
import subprocess
import json
import cv2

# function that gets the duration of a video file
def get_duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

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

# read json config file
with open('../../DATA/installationData/config.json', 'r') as f:
    config = json.load(f)

# init variables
time_to_end         = 0.0
video_iter          = 0
audio_iter          = 0
time_iter           = 0
wait_ratio_x        = random.uniform(0, 999)
video_history       = []
audio_history       = []
pick_audio          = False
time_2_audio        = random.uniform(config["time_2_audio_min"], config["time_2_audio_max"])
time_audio_prev     = 0.0

# transform paths to unix path if unix is detected
video_folder = config["video_folder"]
audio_folder = config["audio_folder"]
oF_app = config["oF_app"]

# get list of files
video_files = os.listdir(video_folder)
audio_files = os.listdir(audio_folder)

# play background
video_command = [oF_app, video_folder + "../bg_sun_1280x720.mp4", str(-1), str(0.99), str(config["offset_x"]), str(0), str(0), "video"]
subprocess.Popen(video_command)
time.sleep(2)

# installation loop
print("Starting loop.\ttime_2_audio = {}".format(time_2_audio))
while True:
    # get timing
    loop_time_start = time.time()

    # pick video
    video_to_read = ""
    while (video_to_read in video_history) or video_to_read == "":
        video_to_read = random.choice(video_files)

    # append to history
    video_history.append(video_to_read)
    if(len(video_history) > config["video_history_size"]) :
        video_history = video_history[1:]

    # get video info
    video_file_duration = get_duration(video_folder + video_to_read)
    cv2_vid = cv2.VideoCapture(video_folder + video_to_read)
    video_width = int(cv2_vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cv2_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # compute scale and position
    limit_ratio = random.uniform(config["size_ratio_min"], config["size_ratio_max"])
    video_scale = math.sqrt(limit_ratio * config["screen_width"] * config["screen_height"] / (video_width * video_height))
    video_pos_x = int(config["offset_x"] + random.uniform(config["border_window_x"], config["screen_width"] - video_width * video_scale - config["border_window_x"]))
    video_pos_y = int(config["offset_y"] + random.uniform(config["border_window_y"], config["screen_height"] - video_height * video_scale - config["border_window_y"]))

    # compute ratio of time to end before next launch
    wait_ratio = (config["wait_ratio_max"] - config["wait_ratio_min"]) * 0.25 * (math.sin(2 * wait_ratio_x) + math.sin(math.pi * wait_ratio_x)) + (config["wait_ratio_max"] + config["wait_ratio_min"]) * 0.5
    wait_ratio_x = wait_ratio_x + 0.1

    # compute time until end of all videos and wait time
    time_to_end += max(0.0, video_file_duration + config["video_player_time_launch"] - time_to_end)
    wait_time = time_to_end * random.uniform(wait_ratio, wait_ratio)

    # small probability of audio
    pick_audio = False
    audio_info = ""
    if abs(time_audio_prev - time_iter) >= time_2_audio:
        audio_info = "=> next is audio"
        pick_audio = True
        wait_time = time_to_end

    # debug
    print("#{}\t{:.4f}\t({}, {})\tx {:.2f}\t@ ({}, {})\tnext in {:.4f}\ttime_to_end = {:.4f}\twait_ratio = {:.3f}\t[{}]\t{}".format(video_iter,
                                                                                                        video_file_duration,
                                                                                                        video_width,
                                                                                                        video_height,
                                                                                                        video_scale,
                                                                                                        video_pos_x,
                                                                                                        video_pos_y,
                                                                                                        wait_time,
                                                                                                        time_to_end,
                                                                                                        wait_ratio,
                                                                                                        video_to_read,
                                                                                                        audio_info))

    # run video player
    video_command = [oF_app,
                    video_folder + video_to_read,
                    str(1),
                    str(video_scale),
                    str(video_pos_x),
                    str(video_pos_y),
                    str(config["video_volume"]),
                    "video"]
    subprocess.Popen(video_command)
    #subprocess.Popen([oF_app])

    # wait and update variables
    time.sleep(wait_time)

    # update variables
    loop_time_end =  time.time()
    loop_duration = loop_time_end - loop_time_start
    time_iter = time_iter + loop_duration
    time_to_end -= loop_duration
    time_to_end = max(0.0, time_to_end)
    video_iter = video_iter + 1

    # if audio
    if pick_audio :
        # set position and size


        # set command
        audio_command = [oF_app,
                        audio_folder + audio_files[audio_iter],
                        str(1),
                        str(1),
                        str(config["offset_x"] + (config["screen_width"] - 400) * 0.5),
                        str(config["offset_y"] + (config["screen_height"] - 200) * 0.5),
                        str(config["audio_volume"]),
                        "audioclip"]
        subprocess.Popen(audio_command)

        # get timings
        audio_duration = get_duration(audio_folder + audio_files[audio_iter])
        time_2_audio = random.uniform(config["time_2_audio_min"], config["time_2_audio_max"])

        # info
        print("#{}/{}\t{:.4f}\t\t\t\t\t\tnext in {:.4f}\t\t\t\t\t\t\t[{}]".format(audio_iter,
                                                                  len(audio_files),
                                                                  audio_duration,
                                                                  time_2_audio,
                                                                  audio_files[audio_iter]))

        # update variables
        audio_iter = audio_iter + 1
        if audio_iter >= len(audio_files) :
            audio_iter = 0

        # sleep
        time.sleep(audio_duration)
        time_audio_prev = time_iter

    #print(str(datetime.timedelta(seconds=time_iter)))
