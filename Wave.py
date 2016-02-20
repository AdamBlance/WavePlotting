class Wave:
    all_waves = []
    wave_range = range(0, 720 + 1)  # Add 1 to last number to include it

    def __init__(self, function):
        self.function = function
        self.surface = 'display_surface'

        self.all_waves.append(self)

    def add_wave_to_queue(self, queue, surface):
        wave_points = []

        for x in self.wave_range:
            wave_points.append((x, int(eval(self.function))))

        queue[surface].append(wave_points)
