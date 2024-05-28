import time

class Example:
    def __init__(self):
        self.current_generation = 0
        self.current_step = 0

    def update(self):
        for _ in range(10):  # Simulate 10 updates
            self.current_generation += 1
            self.current_step += 1
            print(f'\rgen: {self.current_generation} | step: {self.current_step}', end='', flush=True)
            time.sleep(0.5)  # Pause for half a second to simulate work

example = Example()
example.update()
