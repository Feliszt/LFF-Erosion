import os

def get_folders(_path) :
    list_dir = os.listdir(_path)
    for el in list_dir :
        new_path = _path + el + "/"
        new_file = _path + el
        if(os.path.isdir(new_path)) :
            get_folders(new_path)
        else:
            file_ext = el.split('.')[-1]
            if(file_ext == "mp4") :
                #print(new_file)
                with open(data_folder + "facebookMP4Files.txt", 'a') as f :
                    f.write(new_file + "\n")

# set folders and files
folder_to_process = "D:/MISC/FacebookData/13-10-2020/"
data_folder = "../../DATA/"


get_folders(folder_to_process)
