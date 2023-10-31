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


def fitness_3sat(solution, NOrb = 300):
    raan2  = solution[0].copy() #Raan
    raan3  = solution[1].copy() #Raan
    inc  = solution[2].copy()  #Inclinação
    alt = solution[3].copy()   #SMA


    dt = 10

    input_string = ' 11/10/2022 18:00:00'
    data_inicial = datetime.strptime(input_string, " %m/%d/%Y %H:%M:%S")

    # Satélite 1 - Raan 0 --------------
    df = LARS.propagador_orbital(data_inicial, alt, 0.002, 0, 0.0, 0.0, inc, NOrb, dt, 3.0, 0.1, 0.1, 0.2)  # (data, semi_eixo, excentricidade, Raan, argumento_perigeu, anomalia_verdadeira,
                                    # inclinacao, num_orbitas, delt, massa, largura, comprimento, altura)

    df2 = LARS.calculacomunicacao(df)

    df2 = df2[0:-1]
    index1 = df2["Contato"].tolist()

    tempo_comunicacao_simulacao1 = index1.count(1)
    tempo_comunicacao_total1 = tempo_comunicacao_simulacao1 * dt
    tempo_voo1 = len(index1) * dt
    frac1 = tempo_comunicacao_total1/tempo_voo1

    # Satélite 2 - Raan variável ---------------

    df = LARS.propagador_orbital(data_inicial, alt, 0.002, raan2, 0.0, 0.0, inc, NOrb, dt, 3.0, 0.1, 0.1, 0.2)  # (data, semi_eixo, excentricidade, Raan, argumento_perigeu, anomalia_verdadeira,
                                    # inclinacao, num_orbitas, delt, massa, largura, comprimento, altura)

    df2 = LARS.calculacomunicacao(df)

    df2 = df2[0:-1]
    index2 = df2["Contato"].tolist()

    tempo_comunicacao_simulacao2 = index2.count(1)
    tempo_comunicacao_total2 = tempo_comunicacao_simulacao2 * dt
    tempo_voo2 = len(index2) * dt
    frac2 = tempo_comunicacao_total2/tempo_voo2

    # Satélite 3 - Raan variável ---------------

    df = LARS.propagador_orbital(data_inicial, alt, 0.002, raan3, 0.0, 0.0, inc, NOrb, dt, 3.0, 0.1, 0.1, 0.2)  # (data, semi_eixo, excentricidade, Raan, argumento_perigeu, anomalia_verdadeira,
                                    # inclinacao, num_orbitas, delt, massa, largura, comprimento, altura)

    df3 = LARS.calculacomunicacao(df)

    df3 = df3[0:-1]
    index3 = df3["Contato"].tolist()

    tempo_comunicacao_simulacao3 = index3.count(1)
    tempo_comunicacao_total3 = tempo_comunicacao_simulacao3 * dt
    tempo_voo3 = len(index3) * dt
    frac3 = tempo_comunicacao_total3/tempo_voo3



    # O Fitness é a soma do tempo total de comunicação, não duplicando as intersecções 
    comunica = [int(index1[i]) or int(index2[i]) or int(index3[i]) for i in range(len(index1))]
    tempo_comunicacao = comunica.count(1)
    tempo_comunicacao_total = tempo_comunicacao * dt
    tempo_voo = len(comunica) * dt
    frac = tempo_comunicacao_total/tempo_voo


    # print("Gen ",generation,\
    #       "fitness ",inc,alt,raan2,raan3,\
    #       " results ", frac,\
    #       " - tot ",tempo_comunicacao_total2+tempo_comunicacao_total1,max(tempo_voo1,tempo_voo2),\
    #       " sat 1 ",frac1,\
    #       " sat 2 ",frac2,\
    #       " sat 3 ",frac3)

    print("fit3sat(",solution,") = ",frac)
    del df, df2
    return  frac # GA maximiza


def fitness_2sat(solution,NOrb = 300):
    """
    3 variáveis
    """
    #alt = 7000

    raan2  = solution[0].copy() #Raan
    inc  = solution[1].copy()  #Inclinação
    alt = solution[2].copy()   #SMA
    #print("Calculando ",[raan2,inc,alt])


    dt = 10

    input_string = ' 11/10/2022 18:00:00'
    data_inicial = datetime.strptime(input_string, " %m/%d/%Y %H:%M:%S")

    # Satélite 1 - Raan 0 --------------
    df = LARS.propagador_orbital(data_inicial, alt, 0.002, 0, 0.0, 0.0, inc, NOrb, dt, 3.0, 0.1, 0.1, 0.2)  # (data, semi_eixo, excentricidade, Raan, argumento_perigeu, anomalia_verdadeira,
                                    # inclinacao, num_orbitas, delt, massa, largura, comprimento, altura)

    df2 = LARS.calculacomunicacao(df)

    df2 = df2[0:-1]
    index1 = df2["Contato"].tolist()

    tempo_comunicacao_simulacao1 = index1.count(1)
    tempo_comunicacao_total1 = tempo_comunicacao_simulacao1 * dt
    tempo_voo1 = len(index1) * dt
    frac1 = tempo_comunicacao_total1/tempo_voo1

    # Satélite 2 - Raan variável ---------------

    df = LARS.propagador_orbital(data_inicial, alt, 0.002, raan2, 0.0, 0.0, inc, NOrb, dt, 3.0, 0.1, 0.1, 0.2)  # (data, semi_eixo, excentricidade, Raan, argumento_perigeu, anomalia_verdadeira,
                                    # inclinacao, num_orbitas, delt, massa, largura, comprimento, altura)

    df2 = LARS.calculacomunicacao(df)

    df2 = df2[0:-1]
    index2 = df2["Contato"].tolist()

    tempo_comunicacao_simulacao2 = index2.count(1)
    tempo_comunicacao_total2 = tempo_comunicacao_simulacao2 * dt
    tempo_voo2 = len(index2) * dt
    frac2 = tempo_comunicacao_total2/tempo_voo2

    #print("tamanhos de comunicação ",len(index1),len(index2))

    # print(index1)
    # print(index2)

    # O Fitness é a soma do tempo total de comunicação, não duplicando as intersecções 
    comunica = [int(index1[i]) or int(index2[i]) for i in range(len(index1))]
    tempo_comunicacao = comunica.count(1)
    tempo_comunicacao_total = tempo_comunicacao * dt
    tempo_voo = len(comunica) * dt
    frac = tempo_comunicacao_total/tempo_voo


    #print("Gen ",generation,\
    #      "fitness ",inc,alt,raan2,\
    #      " results ", frac,\
    #      " - tot ",tempo_comunicacao_total2+tempo_comunicacao_total1,max(tempo_voo1,tempo_voo2),\
    #      " sat 1 ",frac1,\
    #      " sat 2 ",frac2)

    print("fit2sat(",solution,") = ",frac)

    del df, df2
    return  frac # GA maximiza

def fitness_func(solution):
    raan = solution[0] #Raan
    inc  = solution[1]  #Inclinação
    alt  = solution[2]   #SMA

    print(raan, inc, alt)

    dt = 10

    input_string = ' 11/10/2022 18:00:00'
    data_inicial = datetime.strptime(input_string, " %m/%d/%Y %H:%M:%S")
    df = LARS.propagador_orbital(data_inicial, alt, 0.002, 0, 0.0, raan, inc, 300, dt, 3.0, 0.1, 0.1, 0.2)  # (data, semi_eixo, excentricidade, Raan, argumento_perigeu, anomalia_verdadeira,
                                    # inclinacao, num_orbitas, delt, massa, largura, comprimento, altura)

    df2 = LARS.calculacomunicacao(df)

    df2 = df2[0:-1]
    index = df2["Contato"].tolist()

    tempo_comunicacao_simulacao = index.count(1)
    tempo_comunicacao_total = tempo_comunicacao_simulacao * dt
    tempo_voo = len(index) * dt
    frac = tempo_comunicacao_total/tempo_voo

    #print("fitness ", solution," results ", tempo_comunicacao_total/tempo_voo)
    #print("fitness ",inc," results ", frac," - ",tempo_comunicacao_total,tempo_voo)

    del df, df2
    return  frac # GA maximiza

