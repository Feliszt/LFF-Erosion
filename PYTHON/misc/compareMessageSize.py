import os
import json

def get_folders(_path) :
    list_dir = os.listdir(_path)
    for el in list_dir :
        new_path = _path + el + "/"
        new_file = _path + el
        if(os.path.isdir(new_path)) :
            get_folders(new_path)
        else:
            file_ext = el.split('.')[-1]
            file_name = el.split('.')[0]

            if(file_ext == "json" and file_name[:-1] == "message_"):
                name = _path.split("/")[-2]
                name = name.split("_")[0]

                messages_file_array.append((name, _path + file_name + "." + file_ext))

# set folders and files
folder_to_process = "D:/PERSO/_DATA/FacebookData/13-10-2020/"
messages_file_array = []
messages_count_dict = {}

get_folders(folder_to_process)

# init dict
for el in messages_file_array:
    messages_count_dict[el[0]] = 0

# count all messages
for el in messages_file_array:
    with open(el[1], 'r') as f:
        data = json.load(f)
        messages_count_dict[el[0]] += len(data["messages"])

messages_count_dict_sorted = sorted(messages_count_dict.items(), key=lambda kv: kv[1])

for el in messages_count_dict_sorted:
    print(el)
