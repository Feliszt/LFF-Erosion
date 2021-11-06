import os
import subprocess
import time


# function that gets the duration of a video file
def get_duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

# set folder and files
folder_to_process = "D:/PERSO/_CREA/LFF-Erosion/_DEV/DATA/installationAudios/"
files_to_process = os.listdir(folder_to_process)

# loop
duration_tot = 0
for file in files_to_process :
    media_duration = get_duration(folder_to_process + file)
    duration_tot += media_duration


# display result
print(time.strftime('%H:%M:%S', time.gmtime(duration_tot)))
#print("{} seconds which convert to {} minutes.".format(tot_seconds, tot_seconds / 60))
