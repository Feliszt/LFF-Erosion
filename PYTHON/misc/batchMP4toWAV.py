import os

# set folders and files
folder_to_process = "D:/PERSO/_CREA/Pleine-mer/_DEV/DATA/videoFiles/test/"

# get files
files_to_process = os.listdir(folder_to_process)

# convert all files
for file in files_to_process:
    # get full path
    file_full = folder_to_process + file
    file_full_out = folder_to_process + file.split(".")[0] + ".wav"

    # set ffmpeg command
    ffmpeg_cmd = "ffmpeg -i {} -ac 2 -f wav {}".format(file_full, file_full_out)
    os.system(ffmpeg_cmd)
