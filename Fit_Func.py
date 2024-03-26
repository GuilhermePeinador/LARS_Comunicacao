'''

##          ###    ########   ######
##         ## ##   ##     ## ##    ##
##        ##   ##  ##     ## ##             Universidade Federal de Santa Catarina
##       ##     ## ########   ######        Laboratory of Applications and Research in Space
##       ######### ##   ##         ##       Orbital Mechanics Division
##       ##     ## ##    ##  ##    ##
######## ##     ## ##     ##  ######

Título do Algoritmo: Algoritmo Genético acoplado ao propagador orbital
Autor: Guilherme Peinador Gomes

'''

from datetime import datetime
import LARS
import numpy as np


def fitness_3sat(solution, NOrb = 300):
    raan2 = solution[0].copy()  # Raan
    raan3 = solution[1].copy()  # Raan
    inc = solution[2].copy()    # Inclinação
    alt = solution[3].copy()    # SMA

    dt = 10

    input_string = ' 11/10/2022 18:00:00'
    data_inicial = datetime.strptime(input_string, " %m/%d/%Y %H:%M:%S")

    # Satélite 1 - Raan 0 --------------

    df = LARS.propagador_orbital(data_inicial, alt, 0.002, 0, 0.0, 0.0, inc, NOrb, dt, 3.0, 0.1, 0.1, 0.2)
    # (data, SMA, exc, Raan, arg_perigeu, anom_verdadeira,inc, n_orbitas, delt, mass, larg, comprimento, altura)
    df2 = LARS.calculacomunicacao(df, lat_gs=np.radians(-5.871778), long_gs=np.radians(-35.206864), R_E=6371.00)
    sluntrange[i] # Distância do satélite

    tempodecontato, npassagens, passagens, datasunicas, passagenspordia = LARS.tempocontato(df2)

    # Satélite 2 - Raan variável ---------------

    df = LARS.propagador_orbital(data_inicial, alt, 0.002, raan2, 0.0, 0.0, inc, NOrb, dt, 3.0, 0.1, 0.1, 0.2)
    # (data, SMA, exc, Raan, arg_perigeu, anom_verdadeira,inc, n_orbitas, delt, mass, larg, comprimento, altura)
    df3 = LARS.calculacomunicacao(df, lat_gs=np.radians(-5.871778), long_gs=np.radians(-35.206864), R_E=6371.00)


    tempodecontato2, npassagens2, passagens2, datasunicas2, passagenspordia2 = LARS.tempocontato(df3)

    # Satélite 3 - Raan variável ---------------

    df = LARS.propagador_orbital(data_inicial, alt, 0.002, raan3, 0.0, 0.0, inc, NOrb, dt, 3.0, 0.1, 0.1, 0.2)
    # (data, SMA, exc, Raan, arg_perigeu, anom_verdadeira,inc, n_orbitas, delt, mass, larg, comprimento, altura)
    df4 = LARS.calculacomunicacao(df, lat_gs=np.radians(-5.871778), long_gs=np.radians(-35.206864), R_E=6371.00)


    tempodecontato3, npassagens3, passagens3, datasunicas3, passagenspordia3 = LARS.tempocontato(df4)


    print("fit3sat(", solution, ") = ", frac)

    del df, df2
    return   # GA maximiza
    # Objetivo: Maximizar o número de passagens penalizando com base na distância
