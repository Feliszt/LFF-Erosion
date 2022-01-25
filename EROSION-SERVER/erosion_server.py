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

            # get start time and pick video
            loop_time_start = time.time()
            video_to_read = ""
            while (video_to_read in video_history) or video_to_read == "":
                video_to_read = random.choice(list(self.media["videos"].items()))

            # append to history
            video_history.append(video_to_read)
            if(len(video_history) > self.server_config["video_history_size"]) :
                video_history = video_history[1:]

            # pick a random client to play video on and wait
            video_name = video_to_read[0]
            video_client = random.choice(video_to_read[1]["clients"])
            video_duration = video_to_read[1]["duration"]

            # send play command to client
            send_osc_message(self.get_client_by_ID(video_client)["OSC"], "/play", ("video", 's'), (video_name, 's'))

            # debug
            print("[media_picker]\tclient [{}]\tvideo [{}]".format(video_client, video_name))
            print("[media_picker]\twait {:.2f}".format(video_duration))
            time.sleep(video_duration + self.server_config["video_player_time_launch"])

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
                self.clients.remove(cli)

    #
    def load_data(self) :
        # get client config
        with open('data/config.json', 'r') as f_config :
            self.server_config = json.load(f_config)

    # OSC commands
    def on_hello(self, address, *args) :
        print("[on_hello]\t{}\t{}".format(address, args))

        # check if client is known
        for cli in self.clients :
            if args[2] == cli["name"] and args[1] == cli["ID"]:
                print("[on_hello]\tclient already connected.")
                return

        # store new client
        self.clients.append({"OSC" : udp_client.SimpleUDPClient(args[0], args[1]),
        "IP" : args[0],
        "ID" : len(self.clients),
        "name" : args[2],
        "missing_pongs": 0
        }
        )

        # respond back with welcome
        send_osc_message(self.clients[-1]["OSC"], "/welcome", (self.server_ip, "s"), (self.clients[-1]["ID"], "i"), (self.server_config["ping_pong_interval"], 'f'))

    # receiving media info from a client
    def on_media(self, address, *args) :
        print("[on_media]\t{}".format(address))
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
