import time


class Physics(object):
    def __init__(self):
        self.pos_y = 135
        self.gravity = 800
        self.velocity = 0
        self.pipe_distance = 300
        self.score = 0
        self.counter = - self.pipe_distance - 20
        self.dt = 0

    def jump(self, interface):
        if interface.jumped:
            self.velocity = 350
            interface.jumped = False

    def reset(self, interface):
        interface.clock.tick(60)
        self.pos_y = 100
        self.velocity = 0
        self.score = 0
        self.counter = - self.pipe_distance - 20
        self.dt = 0

    def physics_loop(self, interface):
        self.dt = interface.clock.tick(60) / 1000
        self.jump(interface)
        self.velocity -= self.gravity * self.dt
        self.pos_y -= self.velocity * self.dt
        self.counter += 2
        if self.pos_y <= 0:
            self.pos_y = 0
            self.velocity = 0
        if self.counter == self.pipe_distance:
            self.counter = 0
            self.score += 1
