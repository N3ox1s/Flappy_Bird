class Physics(object):
    def __init__(self):
        self.pos_y = 100
        self.gravity = 500
        self.tube_distance = 100
        self.velocity = 0
        self.score = 0
        self.counter = 0
        self.dt = 0

    def jump(self, interface):
        if interface.jumped:
            self.velocity = 300
            interface.jumped = False

    def physics_loop(self, interface):
        self.dt = interface.clock.tick(60) / 1000
        self.jump(interface)
        self.velocity -= self.gravity * self.dt
        self.pos_y -= self.velocity * self.dt
        self.counter += 1
        if self.counter == self.tube_distance:
            self.counter = 0
            self.score += 1
            print(self.score)
