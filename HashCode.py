import os

class DataCentre(object):
    def __init__(self, no_cache_servers, cache_server_size, no_request_descriptions, video_sizes, endpoints, requests):
        self.request_descriptions = no_request_descriptions

        self.cache_servers = []
        for i in range(no_cache_servers):
            self.cache_servers.append(CacheServer(cache_server_size))

        self.videos = []
        for i in range(len(video_sizes)):
            self.videos.append(Video(i, video_sizes[i]))

        self.end_points = []
        for i in range(len(endpoints)):
            endpoint_data = endpoints[i]
            connections = endpoint_data["cache_connections"]

            endpoint_obj = Endpoint(endpoint_data["latency"])
            for j in range(len(connections)):
                cache_id = connections[j]["id"]
                endpoint_obj.add_connection(self.cache_servers[cache_id], connections[j]["latency"])
            self.end_points.append(endpoint_obj)

        for i in range(len(requests)):
            request_data = requests[i]
            endpoint = self.end_points[request_data["endpoint_id"]]
            video = self.videos[request_data["video_id"]]

            for j in range(request_data["no_requests"]):
                endpoint.add_request(video)

    def output(self):
        target = open("output.out", 'w')
        target.write(str(len(self.cache_servers)))


class Endpoint(object):
    def __init__(self, latency):
        self.latency = latency
        self.cache_connections = {}
        self.video_requests = []

    def add_connection(self, cache, latency):
        self.cache_connections[cache] = latency

    def add_request(self, video):
        self.video_requests.append(video)


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
f = open(os.path.join(directory, "me_at_the_zoo.in"), "r")
data_center_config = f.readline().split(" ")

video_sizes = f.readline().split(" ")

# End Point Video Requests
endpoints = []
for i in range(int(data_center_config[1])): # For each of the end points..
    print i
    endpoint_data = f.readline().split(" ")
    endpoint_latency = endpoint_data[0]
    no_cache_connections = endpoint_data[1]

    cache_connections = []  # Fetch each cache
    for j in range(int(no_cache_connections)):
        cache_data = f.readline().split(" ")

        cache_id = cache_data[0]
        cache_latency = cache_data[1]

        cache_connections.append({"id": int(cache_id), "latency": int(cache_latency)})
    endpoints.append({"latency": int(endpoint_latency), "cache_connections": cache_connections})

line = f.readline()
requests = []
while line != "":
    request_data = line.split(" ")
    requests.append({"video_id": int(request_data[0]), "endpoint_id": int(request_data[1]), "no_requests": int(request_data[2])})

    line = f.readline()

f.close()

data_center = DataCentre(
    int(data_center_config[2]),     # Number of Request Descriptions
    int(data_center_config[3]),     # Number of Cache Servers
    int(data_center_config[4]),     # Size of Cache Server
    video_sizes,                    # Size of Videos
    endpoints,
    requests
)

data_center.output()
print "finished"
