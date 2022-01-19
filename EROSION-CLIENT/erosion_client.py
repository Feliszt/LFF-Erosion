# add paths
import sys
sys.path.append("./../UTILS/")

# utils
from erosion_utils import *
import os
import subprocess
import cv2

class Erosion_Client :

    def __init__(self) :
        self.load_data()
        self.run_network()

    def run_network(self) :
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/welcome", self.on_welcome)
        self.dispatcher.map("/ping", self.on_ping)
        self.dispatcher.map("/media_duration", self.on_media_duration)

        # launch OSC server on client's side to receive commands
        self.client_ip = get_ip()
        self.client_id = -1
        self.client_port = 8001
        self.server = osc_server.ThreadingOSCUDPServer((self.client_ip, self.client_port), self.dispatcher)
        launch_thread(self.server.serve_forever)

        # setup connection to server
        self.server_ip = '.'.join(get_ip().split('.')[:-1] + ["255"])
        self.client = udp_client.SimpleUDPClient(self.server_ip, 8000)

        # attempt connecting to server until done
        while self.client_id == -1 :
            print("Attempt connection to server.")
            send_osc_message(self.client, "/hello",
                (self.client_ip, 's'),
                (self.client_port, 'i'),
                (self.client_config["name"], 's'))
            time.sleep(2)

    def load_data(self) :
        # get client config
        with open('data/config.json', 'r') as f_config :
            self.client_config = json.load(f_config)

        # get data list
        videos = os.listdir("./data/installationVideos/")
        audios = os.listdir("./data/installationAudios/")

        # create sendable media lists
        self.videos_arg = []
        self.audios_arg = []
        for el in videos :
            self.videos_arg.append((el, 's'))
        for el in audios :
            self.audios_arg.append((el, 's'))

    #
    def send_all_media(self) :
        # send media by chunks
        for i in range(0, len(self.videos_arg), 50) :
            send_osc_message(self.client, "/media", (self.client_id, "i"), ("videos", "s"), *self.videos_arg[i:i+50])
        for i in range(0, len(self.audios_arg), 50) :
            send_osc_message(self.client, "/media", (self.client_id, "i"), ("audios", "s"), *self.audios_arg[i:i+50])

    # function that gets the duration of a video file
    def get_duration(self, filename):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)

    # OSC commands
    def on_welcome(self, address, *args) :
        # update info on server
        print("[on_welcome]\t{}\t{}".format(address, args))
        self.server_ip = args[0]
        self.client_id = args[1]
        self.client = udp_client.SimpleUDPClient(self.server_ip, 8000)

        # sends media files to server
        self.send_all_media()

    # receive ping, send pong to server
    def on_ping(self, address, *args) :
        #print("[on_ping]\tclient [{}] receives ping.".format(self.client_id))
        send_osc_message(self.client, "/pong", (self.client_id, 'i'))

    # receive duration query
    def on_media_duration(self, address, *args) :
        # discard bad calls
        if args[1] != "video" and args[1] != "audio":
            print("[on_media_duration]\tbad arguments.")
            return

        # get duratin for media
        media_folder = "installationVideos" if args[1] == "video" else "installationAudios"
        media_path = "data/{}/{}".format(media_folder, args[0])
        media_duration = self.get_duration(media_path)

        # send back information to server
        send_osc_message(self.client, "/media_duration", (self.client_id, 'd'), (args[0], 's'), (media_duration, 'f'))

# run client
erosion_client = Erosion_Client()
while True :
    continue
