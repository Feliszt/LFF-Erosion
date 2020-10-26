import os
import subprocess

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

# set folder
folder_to_process = "D:/PERSO/_CREA/Pleine-mer/MONTAGE/Pleine-mer_data/files_to_keep/audio/"

# get files
files_to_process = os.listdir(folder_to_process)

#
tot_seconds = 0
for file in files_to_process :
    # get length
    res = get_length(folder_to_process + file)
    print(res)

    #
    tot_seconds += res


# display result
print("{} seconds which convert to {} minutes.".format(tot_seconds, tot_seconds / 60))
