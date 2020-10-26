import vlc

#
path = "D:/PERSO/_CREA/Pleine-mer/MONTAGE/Pleine-mer_data/files_to_keep/video/"
file = "video_ble_66_01-05-2019_16h21.mp4"

# creating vlc media player object
media_player = vlc.MediaPlayer()
media = vlc.Media(path + file)
media_player.set_media(media)
media_player.play()

while True:
     pass
