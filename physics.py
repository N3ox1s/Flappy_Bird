from interface import Interface


class Physics(object):
    def __init__(self):
        self.pos_y = 100
        self.gravity = 9.81
        self.tube_distance = 100
        self.velocity = 0
        self.score = 0
        self.counter = 0
    def jump(self):
        if interface.jumped:
            self.velocity += 10
            interface.jumped = False

    def physics_loop(self):
        self.velocity -= self.gravity
        self.pos_y += self.velocity
        self.counter += 1
        if self.counter == self.tube_distance:
            self.counter = 0
            self.score += 1
