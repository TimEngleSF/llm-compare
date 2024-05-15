class Client:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.temp = 1.0
        self.temp_max = 2.0
        self.temp_min = 0.0
        self.top_k = 0

    def get_temp(self):
        return self.temp

    def set_temp(self, temp):
        if temp < self.temp_min:
            self.temp = self.temp_min
        elif temp > self.temp_max:
            self.temp = self.temp_max
        else:
            self.temp = temp
