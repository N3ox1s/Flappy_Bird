import random
class Pipe(object):
    def __init__(self):
        self.pipe_scroll = 0
        self.lower_pipe_length = 0
        self.pipe_gap = random.randint(110, 150)
        self.pipe_image = None

    def move(self):
        self.pipe_scroll -= 2

    def set_pipe_length(self, lower_pipe_length):
        self.lower_pipe_length = lower_pipe_length

    def set_pipe_skin(self, pipe_image):
        self.pipe_image = pipe_image