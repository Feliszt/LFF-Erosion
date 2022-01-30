# add paths
import sys
sys.path.append("./../UTILS/")

# utils
from erosion_utils import *

class Erosion_Server :

    def __init__(self) :
        print("[erosion_server]\tstart.")
        self.load_data()
        self.run_network()

    def run_network(self) :
        # init client and media array
        self.clients = []
        self.media = {"videos" : {}, "audios" : {}}

        # set dispatcher for server
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/hello", self.on_hello)
        self.dispatcher.map("/media", self.on_media)
        self.dispatcher.map("/pong", self.on_pong)

        # launch OSC server on server's side to receive connection messages from clients
        self.server_ip = get_ip()
        self.server = osc_server.ThreadingOSCUDPServer((self.server_ip, 8000), self.dispatcher)
        launch_thread(self.server.serve_forever)

        # launch ping pong loop
        self.ping_pong()

        # launch main loop
        launch_thread(self.media_picker())

    # media picker loop
    def media_picker(self) :
        # init stuff
        video_history       = []

        while True :
            # skip loop as long as no media is present
            if len(self.media["videos"]) == 0 :
                #print("[media_picker]\tmedia list is empty.")
                time.sleep(5)
                continue

            # get time to compute duration of loop later
            loop_time_start = time.time()

            # pick video
            video_to_read = ""
            no_items = False
            while (video_to_read in video_history) or video_to_read == "":
                items = list(self.media["videos"].items())
                if len(items) == 0 :
                    no_items = True
                    break
                video_to_read = random.choice(items)
            if no_items :
                break

            # append to history
            video_history.append(video_to_read)
            if(len(video_history) > self.server_config["video_history_size"]) :
                video_history = video_history[1:]

            # pick a random client to play video on and wait
            video_name = video_to_read[0]
            video_client = random.choice(video_to_read[1]["clients"])
            video_duration = video_to_read[1]["duration"]

            # compute ratio of time to end before next launch
            wait_ratio = (self.server_config["wait_ratio_max"] - self.server_config["wait_ratio_min"]) * 0.25 * (math.sin(2 * self.wait_ratio_x) + math.sin(math.pi * self.wait_ratio_x)) + (self.server_config["wait_ratio_max"] + self.server_config["wait_ratio_min"]) * 0.5
            self.wait_ratio_x = self.wait_ratio_x + 0.1

            # compute time until end of all videos and wait duration
            self.time_to_end += max(0.0, video_duration + self.server_config["video_player_time_launch"] - self.time_to_end)
            wait_duration = self.time_to_end * wait_ratio

            # check if audio
            pick_audio = False
            audio_info = ""
            if (self.client_id_felix != -1 or self.client_id_ophelie != -1) and abs(self.time_audio_prev - self.time_iter) >= self.time_2_audio:
                audio_info = "=> next is audio"
                pick_audio = True
                wait_duration = self.time_to_end

            # send play command to client
            send_osc_message(self.get_client_by_ID(video_client)["OSC"], "/play", ("video", 's'), (video_name, 's'))

            # debug
            print("[media_picker]\tclient [{}]\ttime_to_end = {:.2f}\twait = {:.2f}\tduration {:.2f}\t[{}] {}".format(video_client, self.time_to_end, wait_duration, video_duration, video_name, audio_info))
            time.sleep(wait_duration)

            # compute time until end of videos
            loop_time_end =  time.time()
            loop_duration = loop_time_end - loop_time_start
            self.time_iter =  self.time_iter + loop_duration
            self.time_to_end -= loop_duration
            self.time_to_end = max(0.0, self.time_to_end)

            # if audio
            if pick_audio :
                # get audio info
                audio_name = list(self.media["audios"].items())[self.audio_file_ind][0]
                audio_duration = list(self.media["audios"].items())[self.audio_file_ind][1]["duration"]
                self.time_2_audio = random.uniform(self.server_config["time_2_audio_min"], self.server_config["time_2_audio_max"])

                # update variables
                self.audio_file_ind = self.audio_file_ind + 1
                if self.audio_file_ind >= len(list(self.media["audios"].items())) :
                    self.audio_file_ind = 0

                # send play command to client
                if "felix" in audio_name :
                    audio_client = self.client_id_felix
                elif "ophelie" in audio_name :
                    audio_client = self.client_id_ophelie
                if audio_client == -1 :
                    print("[media_picker]\tcan't play media because no client is set for this media.")
                    self.time_audio_prev = self.time_iter
                    continue

                print("[media_picker]\tclient [{}]\tduration {:.2f}\t[{}]".format(audio_client, audio_duration, audio_name))
                send_osc_message(self.get_client_by_ID(audio_client)["OSC"], "/play", ("audio", 's'), (audio_name, 's'))

                # sleep
                time.sleep(audio_duration)
                self.time_audio_prev = self.time_iter

    # return a client object from an ID
    def get_client_by_ID(self, _id) :
        for cli in self.clients :
            if cli["ID"] == _id :
                return cli
        return None

    # method that regularly checks if clients are alive
    def ping_pong(self) :
        # set ping pong thread
        t = threading.Timer(self.server_config["ping_pong_interval"], self.ping_pong)
        t.daemon = True
        t.start()

        print("felix id = [{}]\tophelie id = [{}]".format(self.client_id_felix, self.client_id_ophelie))

        # ping all modules
        for cli in self.clients :
            send_osc_message(cli["OSC"], "/ping")
            cli["missing_pongs"] += 1

            # check if client missed pings for
            if(cli["missing_pongs"] >= 5) :
                # debug
                print("[ping_pong]\tRemove client with id [{}] and name [{}]".format(cli["ID"], cli["name"]))

                # remove all media related to this client
                for media_type in self.media :
                    media_to_remove = []
                    for media_name in self.media[media_type] :
                        media_clients = self.media[media_type][media_name]["clients"]
                        if cli["ID"] in media_clients :
                            media_clients.remove(cli["ID"])
                            if len(media_clients) == 0 :
                                media_to_remove.append(media_name)
                    for media in media_to_remove :
                        self.media[media_type].pop(media)

                # remove client
                if cli["audio_type"] == "felix" :
                    self.client_id_felix = -1
                if cli["audio_type"] == "ophelie" :
                    self.client_id_ophelie = -1
                if cli["audio_type"] == "both" :
                    self.client_id_felix = -1
                    self.client_id_ophelie = -1
                    self.audio_file_ind = 0
                self.clients.remove(cli)

    #
    def load_data(self) :
        # get client config
        with open('data/config.json', 'r') as f_config :
            self.server_config = json.load(f_config)

        # init variables
        self.next_id                = -1
        self.wait_ratio_x           = random.uniform(0, 999)
        self.time_iter              = 0.0
        self.time_audio_prev        = 0.0
        self.time_2_audio           = random.uniform(self.server_config["time_2_audio_min"], self.server_config["time_2_audio_max"])
        self.time_to_end            = 0.0
        self.client_id_felix        = -1
        self.client_id_ophelie      = -1
        self.audio_file_ind         = 0

    # OSC commands
    def on_hello(self, address, *args) :
        print("[on_hello]\t{}\t{}".format(address, args))

        # check if client is known
        for cli in self.clients :
            if args[2] == cli["name"] and args[1] == cli["ID"]:
                print("[on_hello]\tclient already connected.")
                return

        # store new client
        self.next_id += 1
        self.clients.append({"OSC" : udp_client.SimpleUDPClient(args[0], args[1]),
        "IP" : args[0],
        "ID" : self.next_id,
        "name" : args[2],
        "audio_type" : args[3],
        "missing_pongs": 0
        }
        )

        # check audio type
        if self.clients[-1]["audio_type"] == "felix" :
            self.client_id_felix    = self.clients[-1]["ID"]
        if self.clients[-1]["audio_type"] == "ophelie" :
            self.client_id_ophelie  = self.clients[-1]["ID"]
        if self.clients[-1]["audio_type"] == "both" :
            self.client_id_felix    = self.clients[-1]["ID"]
            self.client_id_ophelie  = self.clients[-1]["ID"]

        # respond back with welcome
        send_osc_message(self.clients[-1]["OSC"], "/welcome", (self.server_ip, "s"), (self.clients[-1]["ID"], "i"), (self.server_config["ping_pong_interval"], 'f'))

    # receiving media info from a client
    def on_media(self, address, *args) :
        print("[on_media]\treceive media info from client [{}]".format(args[0]))
        #print("[on_media]\t{}\t{}".format(address, args))
        for media in zip(args[2::2], args[3::2]) :
            if media[0] not in self.media[args[1]] :
                self.media[args[1]][media[0]] = {}
                self.media[args[1]][media[0]]["clients"] = []
                self.media[args[1]][media[0]]["duration"] = media[1]
            self.media[args[1]][media[0]]["clients"].append(args[0])

    #
    def on_pong(self, address, *args) :
        #print("[on_pong]\tclient [{}] sends pong.".format(args[0]))
        self.get_client_by_ID(args[0])["missing_pongs"] = 0


# run server
erosion_server = Erosion_Server()
while True :
    continue
