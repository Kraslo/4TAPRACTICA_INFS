import numpy as np

class usuario():
    def __init__(self, t_llegada, t_servicio):
        self.t_llegada = t_llegada
        self.t_servicio = t_servicio


class usuario1(usuario):
    media = 400
    low = 30
    high = 200

    def __init__(self, t_llegada, t_servicio):
        super().__init__(t_llegada=t_llegada, t_servicio=t_servicio)


class usuario2(usuario):
    media = 1000
    low = 300
    high = 1200

    def __init__(self, t_llegada, t_servicio):
        super().__init__(t_llegada, t_servicio)
