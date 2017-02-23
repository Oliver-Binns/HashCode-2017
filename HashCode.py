class Video(object):
    def __init__(self, size):
        self.size = size


class CacheServer(object):
    def __init__(self, max_size, videos):
        self.max_size = max_size
        self.videos = videos

        if self.videos is None:
            self.videos = []

    def get_size(self):
        size = 0
        for i in range(len(self.videos)):
            size += self.videos[i].size

    def add_video(self, video):
        if self.get_size() + video.size <= self.max_size:
            self.videos.append(video)

