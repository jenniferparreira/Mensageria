class LogicalClock:
    def __init__(self):
        self.time = 0

    def increment(self):
        self.time += 1
        return self.time

    def update(self, received_time):
        self.time = max(self.time, received_time) + 1

    def get(self):
        return self.time
