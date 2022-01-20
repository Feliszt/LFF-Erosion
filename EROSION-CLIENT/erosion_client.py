# add paths
import sys
sys.path.append("./../UTILS/")

# utils
from erosion_utils import *
import os
import subprocess
import cv2

class Erosion_Client :

    #
    def __init__(self) :
        print("[erosion_client]\tstart.")
        self.load_data()
        self.run_network()

        # play bg media
        play_media_command = [self.media_player, "background/bg_media.mp4", str(-1), str(0.99), str(0), str(0), str(0), "video"]
        subprocess.Popen(play_media_command)

    #
    def load_data(self) :
        # debug
        print("[load_data]\tloading data.")

        # get client config
        with open('data/config.json', 'r') as f_config :
            self.client_config = json.load(f_config)

        # get data list
        videos = os.listdir("./data/video/")
        audios = os.listdir("./data/audio/")

        # create sendable media lists
        self.videos_arg = []
        self.audios_arg = []
        for el in videos :
            self.videos_arg.append((el, 's'))
            self.videos_arg.append((self.get_duration("data/video/" + el), 'f'))
        for el in audios :
            self.audios_arg.append((el, 's'))
            self.audios_arg.append((self.get_duration("data/audio/" + el), 'f'))

        # set
        self.media_player = "./tools/" + self.client_config["media_player"]

        # debug
        print("[load_data]\tdone.")

    #
    def run_network(self) :
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/welcome", self.on_welcome)
        self.dispatcher.map("/play", self.on_play)
        self.dispatcher.map("/ping", self.on_ping)

        # launch OSC server on client's side to receive commands
        self.client_ip = get_ip()
        self.client_id = -1
        self.client_port = 8001
        self.server = osc_server.ThreadingOSCUDPServer((self.client_ip, self.client_port), self.dispatcher)
        launch_thread(self.server.serve_forever)

        # connect to server
        launch_thread(self.connect_to_server)

    #
    def connect_to_server(self) :
        # setup connection to server
        self.server_ip = '.'.join(get_ip().split('.')[:-1] + ["255"])
        self.client = udp_client.SimpleUDPClient(self.server_ip, 8000)

        # attempt connecting to server until done
        while self.client_id == -1 :
            print("[connect_to_server]\tAttempt connection.")
            send_osc_message(self.client, "/hello",
                (self.client_ip, 's'),
                (self.client_port, 'i'),
                (self.client_config["name"], 's'))
            time.sleep(2)

    #
    def check_server_pings(self) :
        while self.client_id != -1 :
            time.sleep(10)
            time_2_last_ping = abs(self.ping_time - time.time())
            if time_2_last_ping >= 5 * self.server_ping_inter :
                print("[check_server_pings]\tserver disconnect.")
                self.client_id = -1
        launch_thread(self.connect_to_server)

    #
    def send_all_media(self) :
        # send media by chunks
        for i in range(0, len(self.videos_arg), 100) :
            send_osc_message(self.client, "/media", (self.client_id, "i"), ("videos", "s"), *self.videos_arg[i:i+100])
        for i in range(0, len(self.audios_arg), 100) :
            send_osc_message(self.client, "/media", (self.client_id, "i"), ("audios", "s"), *self.audios_arg[i:i+100])

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
        # debug
        print("[on_welcome]\t{}\t{}".format(address, args))

        #
        self.server_ip = args[0]
        self.client_id = args[1]
        self.client = udp_client.SimpleUDPClient(self.server_ip, 8000)
        self.server_ping_inter = args[2]
        self.ping_time = time.time()
        launch_thread(self.check_server_pings)

        # sends media files to server
        self.send_all_media()

    # command to play media
    def on_play(self, address, *args) :
        # debug
        print("[on_play]\t{}\t{}".format(address, args))

    # receive ping, send pong to server
    def on_ping(self, address, *args) :
        # debug
        #print("[on_ping]\tclient [{}] receives ping.".format(self.client_id))
        self.ping_time = time.time()
        send_osc_message(self.client, "/pong", (self.client_id, 'i'))

# run client
erosion_client = Erosion_Client()
while True :
    continue
