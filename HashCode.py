import os


class DataCentre(object):
    def __init__(self, no_cache_servers, cache_server_size, no_request_descriptions, video_sizes, cache_connections):
        self.request_descriptions = no_request_descriptions

        self.cache_servers = []
        for i in range(no_cache_servers):
            self.cache_servers.append(CacheServer(cache_server_size))

        videos = []
        for i in range(len(video_sizes)):
            videos.append(Video(i, video_sizes[i]))


class Video(object):
    def __init__(self, video_id, size):
        self.video_id = video_id
        self.size = int(size)


class CacheServer(object):
    def __init__(self, max_size):
        self.max_size = max_size
        self.videos = []

    def get_size(self):
        size = 0
        for i in range(len(self.videos)):
            size += self.videos[i].size

    def add_video(self, video):
        if self.get_size() + video.size <= self.max_size:
            self.videos.append(video)


# For each file.. in the data directory
directory = "data"
# for file in os.listdir(directory):
#    if file.endswith(".in"):
f = open(os.path.join(directory, "kittens.in"), "r")
data_center_config = f.readline()

video_sizes = f.readline().split(" ")

# End Point Video Requests
cache_connections = []
for i in range(int(data_center_config[1])):
    cache_connections.append(f.readline().split())

data_center = DataCentre(
    int(data_center_config[2]), # Number of Request Descriptions
    int(data_center_config[3]), # Number of Cache Servers
    int(data_center_config[4]), # Size of Cache Server
    video_sizes   # Size of Videos
)
