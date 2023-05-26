import numpy as np
from classes import usuario


def crear_usuarios(tipo: usuario, nUsuarios: int, tEspera: int) -> np.array:
    '''
    Crea una lista de nUsuarios usuarios según su media de tiempo entre 
    usuario, teniendo en cuenta el tiempo de descanso (tEspera) del servicio.
    '''
    tiempos_entre_usuarios: np.array = np.random.exponential(tipo.media,
                                              size=nUsuarios)
    tiempos_llegada: np.array = np.cumsum(tiempos_entre_usuarios)

    tiempos_servicio: np.array = tEspera + np.random.uniform(low=tipo.low,
                                                   high=tipo.high,
                                                   size=nUsuarios)
    
    usuarios: np.array = np.array([tipo(tiempo_llegada, tiempo_servicio) 
                          for tiempo_llegada, tiempo_servicio 
                          in zip(tiempos_llegada, tiempos_servicio)
                          ])

    return usuarios


def insertar_salida(user: usuario,
                    # t: int,
                    # previousnUsers: int,
                    previous_tSalida: int,
                    nUsers: int,
                    events: dict[str:np.array],
                    anyQueue: bool
                    ):
    '''
    Inserta salidas en el diccionario de eventos de salida.
    '''
    user.instante_servicio = user.t_llegada if anyQueue else previous_tSalida
    events['hour'] = np.append(events['hour'], user.instante_servicio + user.t_servicio)
    events['nUsers'] = np.append(events['nUsers'], nUsers)
    return events


def insertar_entrada(user: usuario, events: dict[str:np.array]):
    '''
    Inserta entradas en el diccionario de eventos de entrada.
    '''
    events['hour'] = np.append(events['hour'],
                                    user.t_llegada)
    previousnUsers: int = events['nUsers'][-1] if events['nUsers'].any() else 0
    events['nUsers'] = np.append(events['nUsers'],
                                    previousnUsers + 1)
    return events

    
def calc_tmean_jornada(usuarios: usuario) -> float:
    '''
    Calcula el tiempo medio de espera en cola de un usuario promediado en una
    jornada diaria.
    '''
    tiempos_llegada: np.array = np.fromiter(
        (usuario.t_llegada for usuario in usuarios),
        dtype=int
        )
    instantes_servicio: np.array = np.fromiter(
        (usuario.instante_servicio for usuario in usuarios),
        dtype=int
        )
    
    tiempos_espera: np.array = instantes_servicio - tiempos_llegada
    medi_espera: float = np.mean(tiempos_espera)

    return medi_espera


def calc_pct_ocupation(usuarios: usuario, jornada_laboral: int) -> float:
    '''
    Calcula el tanto por ciento de ocupación del servidor.
    '''
    tiempos_servicio: np.array = np.fromiter(
        (usuario.t_servicio for usuario in usuarios),
        dtype=int
    )
    porcentaje_servido: float = (np.sum(tiempos_servicio[:-1]) / jornada_laboral) \
                                 * 100
    return porcentaje_servido

def calc_meanUsers(events: dict, jornada_laboral: int) -> float:
    '''
    Calcula el número medio de usuarios en la cola en una jornada diaria.
    '''
    time_increments: np.array = np.diff(events['hour'])
    out_mean: np.array = np.sum(np.multiply(
        events['nUsers'][:-1],
        time_increments)
        ) / jornada_laboral

    return out_mean


def calc_estadisticos(lista_valores: np.array) -> tuple:
    media_valores: float = np.mean(lista_valores)
    var_valores: float = np.var(lista_valores)
    return media_valores, var_valores