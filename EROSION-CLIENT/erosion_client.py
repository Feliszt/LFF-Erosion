# add paths
import sys
sys.path.append("./../UTILS/")

# utils
from erosion_utils import *
import subprocess
import cv2
import screeninfo

class Erosion_Client :

    #
    def __init__(self) :
        self.init_log()
        logging.info("[erosion_client]\tstart.")
        self.load_data()
        self.run_network()

        # play bg media
        bgmedia_abs_path = os.path.abspath("data/background/" + self.client_config["bg_media"])
        if os.path.isfile(bgmedia_abs_path) :
            play_media_command = [self.media_player, bgmedia_abs_path, str(-1), str(0.99), str(0), str(0), str(0), "video"]
            subprocess.Popen(play_media_command)
        else :
            logging.info("[__init__]\tcan't find background file.")


    #
    def load_data(self) :
        # get client config
        with open('data/config.json', 'r') as f_config :
            self.client_config = json.load(f_config)

        # get screen size
        if len(screeninfo.get_monitors()) == 0 :
            logging.info("[load_data]\tno screens connected to client. Quitting.")
            quit()
        if self.client_config["screen_id"] >= len(screeninfo.get_monitors()) :
            logging.info("[load_data]\tscreen id is too high.")
            quit()
        self.screen_width = screeninfo.get_monitors()[self.client_config["screen_id"]].width
        self.screen_height = screeninfo.get_monitors()[self.client_config["screen_id"]].height
        self.screen_offset_x = screeninfo.get_monitors()[self.client_config["screen_id"]].x
        self.screen_offset_y = screeninfo.get_monitors()[self.client_config["screen_id"]].y
        logging.info("[load_data]\tscreen size = [{}, {}] @ [{}, {}]".format(self.screen_width, self.screen_height, self.screen_offset_x, self.screen_offset_y))

        # get data list
        videos = os.listdir("./data/" + self.client_config["video_folder"])
        audios = os.listdir("./data/" + self.client_config["audio_folder"])

        # init media and media player info
        logging.info("[load_data]\tloading data.")
        self.media_player = "./tools/" + self.client_config["media_player"]
        self.videos_arg = []
        self.audios_arg = []
        self.video_sz = {}
        for el in videos :
            video_path = "./data/" + self.client_config["video_folder"] + "/" + el
            self.videos_arg.append((el, 's'))
            self.videos_arg.append((self.get_duration(video_path), 'f'))
            cv2_vid = cv2.VideoCapture(video_path)
            self.video_sz[el] = {"width" : int(cv2_vid.get(cv2.CAP_PROP_FRAME_WIDTH)), "height" : int(cv2_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))}
        for el in audios :
            self.audios_arg.append((el, 's'))
            self.audios_arg.append((self.get_duration("./data/" + self.client_config["audio_folder"] + "/" + el), 'f'))

        # debug
        logging.info("[load_data]\tdone.")

    #
    def init_log(self):
        formatter = logging.Formatter("[%(asctime)s]\t%(message)s", datefmt='%d/%m/%Y - %H:%M:%S')
        file_handler = logging.FileHandler("./data/erosion-server.log")
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logging.getLogger().setLevel(logging.INFO)
        logging.getLogger().addHandler(file_handler)
        logging.getLogger().addHandler(stream_handler)

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
            logging.info("[connect_to_server]\tAttempt connection.")
            send_osc_message(self.client, "/hello",
                (self.client_ip, 's'),
                (self.client_port, 'i'),
                (self.client_config["name"], 's'),
                (self.client_config["audio_type"], 's'))
            time.sleep(2)

    #
    def check_server_pings(self) :
        while self.client_id != -1 :
            time.sleep(10)
            time_2_last_ping = abs(self.ping_time - time.time())
            if time_2_last_ping >= 5 * self.server_ping_inter :
                logging.info("[check_server_pings]\tserver disconnect.")
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
        logging.info("[on_welcome]\t{}\t{}".format(address, args))

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
        #logging.info("[on_play]\t{}\t{}".format(address, args))

        # check media type
        media_folder = ""
        media_type = args[0]
        if media_type == "video" :
            media_folder    = self.client_config["video_folder"]
            media_width     = self.video_sz[args[1]]["width"]
            media_height    = self.video_sz[args[1]]["height"]
            limit_ratio     = random.uniform(self.client_config["size_ratio_min"], self.client_config["size_ratio_max"])
            media_scale     = math.sqrt(limit_ratio * self.screen_width * self.screen_height / (media_width * media_height))
            media_pos_x     = int(self.screen_offset_x + random.uniform(self.client_config["border_window_x"], self.screen_width - media_width * media_scale - self.client_config["border_window_x"]))
            media_pos_y     = int(self.screen_offset_y + random.uniform(self.client_config["border_window_y"], self.screen_height - media_height * media_scale - self.client_config["border_window_y"]))
            media_vol       = self.client_config["video_volume"]
        elif media_type == "audio" :
            media_folder    = self.client_config["audio_folder"]
            media_width     = self.client_config["audio_width"]
            media_height    = self.client_config["audio_height"]
            media_scale     = 1
            media_pos_x     = int((self.screen_width - media_width) * 0.5)
            media_pos_y     = int((self.screen_height - media_height) * 0.5)
            media_vol       = self.client_config["audio_volume"]
        else :
            logging.info("[on_play]\tunknown media type.")
            return

        # play media
        media_loop          = 1
        media_abs_path = os.path.abspath("data/" + media_folder + "/" + args[1])
        play_media_command  = [self.media_player, media_abs_path, str(media_loop), str(media_scale), str(media_pos_x), str(media_pos_y), str(media_vol), media_type]
        subprocess.Popen(play_media_command)

        # debug
        logging.info("[on_play]\tpos : ({:03d}, {:03d})\tscale : {:.2f}\tvol : {}\t[{}]".format(media_pos_x, media_pos_y, media_scale, media_vol, args[1]))

    # receive ping, send pong to server
    def on_ping(self, address, *args) :
        # debug
        #logging.info("[on_ping]\tclient [{}] receives ping.".format(self.client_id))
        self.ping_time = time.time()
        send_osc_message(self.client, "/pong", (self.client_id, 'i'))

# run client
erosion_client = Erosion_Client()
while True :
    continue
