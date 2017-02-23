import os, math

class DataCentre(object):
    def __init__(self, no_cache_servers, cache_server_size, no_request_descriptions, video_sizes, endpoints, requests):
        self.request_descriptions = no_request_descriptions

        self.cache_servers = []
        for i in range(no_cache_servers):
            self.cache_servers.append(CacheServer(i, cache_server_size))

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

            endpoint.add_request(video, request_data["no_requests"])

    def fill_caches(self):
        for i in range(len(self.end_points)):
            endpoint = self.end_points[i]
            endpoint.video_requests.sort(key=lambda x: x.no_requests, reverse=True)
            endpoint.cache_connections.sort(key=lambda x: x.latency)

        self.fill_range(0, 0.05)
        self.fill_range(0.05, 0.25)
        self.fill_range(0.25, 0.5)
        self.fill_range(0.5, 1)

    def fill_range(self, start, finish):
        # Runs algorithm here...
        for i in range(len(self.end_points)):
            endpoint = self.end_points[i]
            num_videos = len(endpoint.video_requests)
            for j in range(int(math.floor(num_videos * start)), int(math.ceil(num_videos * finish))):
                request = endpoint.video_requests[j]
                for k in range(len(endpoint.cache_connections)):
                    cache = endpoint.cache_connections[k].cache
                    if cache.contains(request.video):
                        break
                    elif cache.can_add(request.video):
                        cache.add_video(request.video)
                        break

    def output(self, filename):
        target = open(filename + ".out", 'w')
        target.write(str(len(self.cache_servers)) + "\n")
        for i in range(len(self.cache_servers)):
            target.write(self.cache_servers[i].get_output() + "\n")
        target.close()


class Endpoint(object):
    def __init__(self, latency):
        self.latency = latency
        self.cache_connections = []
        self.video_requests = []

    def add_connection(self, cache, latency):
        self.cache_connections.append(CacheConnection(cache, latency))

    def add_request(self, video, no_requests):
        self.video_requests.append(VideoRequest(video, no_requests))


class VideoRequest(object):
    def __init__(self, video, no_requests):
        self.video = video
        self.no_requests = no_requests


class Video(object):
    def __init__(self, video_id, size):
        self.video_id = video_id
        self.size = int(size)


class CacheConnection(object):
    def __init__(self, cache, latency):
        self.cache = cache
        self.latency = latency


class CacheServer(object):
    def __init__(self, id, max_size):
        self.id = id
        self.max_size = max_size
        self.videos = []

    def contains(self, video):
        return video in self.videos

    def can_add(self, video):
        return self.get_size() + video.size <= self.max_size

    def get_size(self):
        size = 0
        for i in range(len(self.videos)):
            size += self.videos[i].size
        return size

    def add_video(self, video):
        if self.can_add(video):
            self.videos.append(video)

    def get_output(self):
        output_string = str(self.id)
        for i in range(len(self.videos)):
            output_string += " " + str(self.videos[i].video_id)
        return output_string


# For each file.. in the data directory
directory = "data"
for file in os.listdir(directory):
    if file.endswith(".in"):
        f = open(os.path.join(directory, file), "r")

        if file != "videos_worth_spreading.in":
            continue

        data_center_config = f.readline().split(" ")

        video_sizes = f.readline().split(" ")

        # End Point Video Requests
        endpoints = []
        for i in range(int(data_center_config[1])): # For each of the end points..
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
            int(data_center_config[3]),     # Number of Cache Servers
            int(data_center_config[4]),     # Size of Cache Server
            int(data_center_config[2]),     # Number of Request Descriptions
            video_sizes,                    # Size of Videos
            endpoints,
            requests
        )
        data_center.fill_caches()
        data_center.output(file)
        print "first file done"

print "finished"
