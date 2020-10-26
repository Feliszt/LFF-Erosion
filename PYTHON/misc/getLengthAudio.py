import os

# set folder
folder_to_process = "D:/PERSO/_CREA/Pleine-mer/MONTAGE/Pleine-mer_data/"

# get files
files_to_process = os.listdir(folder_to_process)

#
tot_seconds = 0
for file in files_to_process :
    # get number of second
    file_length = file.split("_")[-1]
    file_length = file_length.split(".")[0]

    #
    tot_seconds += int(file_length)


# display result
print("{} seconds which convert to {} minutes.".format(tot_seconds, tot_seconds / 60))
