# add paths
import sys
sys.path.append("./../UTILS/")

# utils
from erosion_utils import *

class Erosion_Server :

    def __init__(self) :
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
        self.dispatcher.map("/media_duration", self.on_media_duration)

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
        time.sleep(5)
        self.media_query_duration = None
        rand_cli = random.choice(self.clients)
        rand_vid = random.choice(list(self.media["videos"].items()))[0]
        print("{}\n{}".format(rand_cli, rand_vid))

        send_osc_message(rand_cli["OSC"], "/media_duration", (rand_vid, 's'), ("video", 's'))
        return

        while True :
            print(len(self.media["videos"]))
            #print("[media_picker]\thehe")
            time.sleep(2)

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
            if(cli["missing_pongs"] >= 5) :
                print("Remove module with id [{}] and name [{}]".format(cli["ID"], cli["name"]))
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
            if args[2] == cli["name"] :
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
        send_osc_message(self.clients[-1]["OSC"], "/welcome", (self.server_ip, "s"), (self.clients[-1]["ID"], "i"))

    #
    def on_media(self, address, *args) :
        #print("[on_media]\t{}\t{}".format(address, args))
        for media in args[2:] :
            if media not in self.media[args[1]] :
                self.media[args[1]][media] = []
            self.media[args[1]][media].append(args[0])

    #
    def on_pong(self, address, *args) :
        #print("[on_pong]\tclient [{}] sends pong.".format(args[0]))
        self.get_client_by_ID(args[0])["missing_pongs"] = 0

    # receive duration query
    def on_media_duration(self, address, *args) :
        print("[on_media_duration]\t{}".format(args))


# run server
erosion_server = Erosion_Server()
while True :
    continue
