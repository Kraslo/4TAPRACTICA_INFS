import numpy as np
from scripts import crear_usuarios, insertar_entrada, insertar_salida
from scripts import calc_tmean_jornada, calc_meanUsers, calc_pct_ocupation
from scripts import calc_estadisticos
from classes import usuario1, usuario2


# Constantes:
Nens = 75 # número de ensayos inicial.
nUsuarios = 120
tEspera = 180

# Variables que necesitaremos.
usuarios_tipo_1: np.array = np.array([])
usuarios_tipo_2: np.array = np.array([])
jornada_laboral: int = 21600
politica: str = 'Least_time'
exit_flag: bool = False

# Listas de méritos:
tiempos_espera_medios: np.array = np.array([])
porcentages_ocupacion: np.array = np.array([])
n_medio_usuarios_cola: np.array = np.array([])
num_medio_uAtendidos:  np.array = np.array([])


for ensayo in range(Nens):

    usuarios_tipo_1 = crear_usuarios(tipo=usuario1,
                                     nUsuarios=nUsuarios,
                                     tEspera=tEspera
                                     )
    usuarios_tipo_2 = crear_usuarios(tipo=usuario2,
                                     nUsuarios=nUsuarios,
                                     tEspera=tEspera
                                     )

    usuarios: np.array = np.concatenate([usuarios_tipo_1, usuarios_tipo_2])
    usuarios = sorted(usuarios, key=lambda x: x.t_llegada)

    # empezamos el servicio
    # 6 horas * 3600s / 1h = 21600

    events: dict = {
        'hour': np.array([]),
        'nUsers': np.array([])
    }
    nAtendidos: int = 0
    cola: np.array = np.array([])
    anyQueue: bool = True

    match politica:

        case 'FIFO':
            previous_tSalida: int = 0
            usuarios_atendidos: np.array = np.array([])     
                
            for i in range(len(usuarios) - 1):
                
                events = insertar_entrada(user=usuarios[i], events=events)
                cola = np.append(cola, usuarios[i])
                anyQueue = bool(len(cola) == 0)
                while previous_tSalida < usuarios[i + 1].t_llegada and len(cola) != 0:
                    events = insertar_salida(user=cola[0], # fifo
                                    previous_tSalida=previous_tSalida,
                                    nUsers=len(cola), # n of cummulative users
                                    events=events,
                                    anyQueue=anyQueue
                                    )
                    usuarios_atendidos = np.append(usuarios_atendidos, cola[0])
                    nAtendidos += 1
                    previous_tSalida = cola[0].instante_servicio + cola[0].t_servicio
                    cola = np.delete(cola, 0)
                    if previous_tSalida > jornada_laboral:
                        exit_flag = True
                        break

                if exit_flag:
                    exit_flag = False
                    break
 

            tMean_espera: float = np.abs(calc_tmean_jornada(
                                            usuarios=usuarios_atendidos,
                                            ))
            
            pctg_ocupacion: float = np.abs(calc_pct_ocupation(
                                            usuarios=usuarios_atendidos,
                                            jornada_laboral=jornada_laboral
                                            ))
            
            meanUsers: float = np.abs(calc_meanUsers(events=events,
                                            jornada_laboral=jornada_laboral,
                                            ))
            # print(f'tmeanespera {tMean_espera}')
            tiempos_espera_medios = np.append(tiempos_espera_medios, 
                                              tMean_espera)
            porcentages_ocupacion = np.append(porcentages_ocupacion,
                                              pctg_ocupacion)
            n_medio_usuarios_cola = np.append(n_medio_usuarios_cola,
                                              meanUsers)
            num_medio_uAtendidos = np.append(num_medio_uAtendidos, nAtendidos)
           

        case 'Least_time':
            previous_tSalida: int = 0      
            usuarios_atendidos: np.array = np.array([])      
                
            for i in range(len(usuarios) - 1):

                events = insertar_entrada(user=usuarios[i], events=events)

                cola = np.append(cola, usuarios[i])
                tiempos_servicio: np.array = np.fromiter(
                    (usuario.t_servicio for usuario in cola),
                    dtype=int
                )    
                argsort: np.array = np.argsort(tiempos_servicio)
                cola = cola[argsort]
                anyQueue = bool(len(cola) == 0)

                while previous_tSalida < usuarios[i + 1].t_llegada and len(cola) != 0:
                    events = insertar_salida(user=cola[0],
                                    previous_tSalida=previous_tSalida,
                                    nUsers=len(cola),
                                    events=events,
                                    anyQueue=anyQueue
                                    )
                    usuarios_atendidos = np.append(usuarios_atendidos, cola[0])
                    nAtendidos += 1
                    previous_tSalida = cola[0].instante_servicio + cola[0].t_servicio
                    cola = np.delete(cola, 0)
                    if previous_tSalida >= jornada_laboral:
                        exit_flag = True
                        break

                if exit_flag:
                    exit_flag = False
                    break

            # print('#'*100)
            # print('Calculando méritos (Método LEAST_TIME)...'.center(100))
            # print('#'*100)

            tMean_espera: float = np.abs(calc_tmean_jornada(
                                            usuarios=usuarios_atendidos,
                                            ))
            
            pctg_ocupacion: float = np.abs(calc_pct_ocupation(
                                            usuarios=usuarios_atendidos,
                                            jornada_laboral=jornada_laboral
                                            ))
            
            meanUsers: float = np.abs(calc_meanUsers(events=events,
                                            jornada_laboral=jornada_laboral,
                                            ))
            
            tiempos_espera_medios = np.append(tiempos_espera_medios, 
                                              tMean_espera)
            porcentages_ocupacion = np.append(porcentages_ocupacion,
                                              pctg_ocupacion)
            n_medio_usuarios_cola = np.append(n_medio_usuarios_cola,
                                              meanUsers)
            num_medio_uAtendidos = np.append(num_medio_uAtendidos, nAtendidos)
            # print(' '*5
            #        + '· NÚMERO DE USUARIOS ATENDIDOS: '
            #        + str(nAtendidos) 
            #        )
            # print(' '*5
            #        + '· TIEMPO MEDIO DE ESPERA EN LA COLA DE LOS USUARIOS: '
            #        + str(tMean_espera) 
            #        )
            # print(' '*5
            #        + '· TANTO POR CIENTO DE OCUPACIÓN DEL SERVIDOR: '
            #        + str(pctg_ocupacion)
            #        )
            # print(' '*5
            #       + '· NÚMERO MEDIO DE USUARIOS EN LA COLA: '
            #       + str(meanUsers)
            #       )
            
        case other:
            raise Exception('Política incorrecta.')
        

print('#'*100)
print(f'Calculando méritos (Método {politica})...'.center(100))
print(f'Número de ensayos: {Nens}'.center(100))
print('#'*100)

error_relativo = lambda nens, mean, var : np.sqrt(var/nens)/mean

media_t_espera, var_t_espera = calc_estadisticos(tiempos_espera_medios)
media_pctg_ocupacion, var_pctg_ocupacion = calc_estadisticos(
                                            porcentages_ocupacion)
media_nUsers_cola, var_nUsers_var = calc_estadisticos(n_medio_usuarios_cola)
titles: np.array = np.array(['Tiempo medio de espera en cola',
                             'Porcentaje de ocupación',
                             'Número medio de usuarios en cola'])
media_usuarios_atendidos: float = np.mean(num_medio_uAtendidos)
print_iterable: np.array = np.array(
    [(titles[0], media_t_espera, var_t_espera),
     (titles[1], media_pctg_ocupacion, var_pctg_ocupacion),
     (titles[2], media_nUsers_cola, var_nUsers_var)])
print('-'*100)
print(' '*5
        + '· Número de usuarios atendidos: '
        + str(media_usuarios_atendidos) 
        )
print('-'*100)
for title, media, varianza in print_iterable: 
    print(' '*5
        + f'· {title}: '
        + str(media) 
        )
    print(' '*5
        + f'· Varianza: {varianza}'
        )
    print('-'*100)
    print(' '*5
        + f'ERROR RELATIVO: \
        {error_relativo(Nens, float(media), float(varianza))}')
    print('-'*100)




