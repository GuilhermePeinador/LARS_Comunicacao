# -*- coding: utf-8 -*-
# propagador_orbital_mk4.py>
from datetime import datetime
import numpy as np
import pandas as pd


def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("src-LARS")
    return os.path.join(base_path, relative_path)


def propagador_orbital(data: str, semi_eixo: float, excentricidade: float, raan: float, argumento_perigeu: float,
                       anomalia_verdadeira: float, inclinacao: float, num_orbitas: int, delt: float, massa: float, largura: float,
                       comprimento: float, altura: float):

    """
    :param data = inicio da simulacao
    :param semi_eixo = altitude no periapse da orbita
    :param excentricidade = e
    :param raan= Angulo da posicao do nodo ascendente
    :param argumento_perigeu = Angulo da orientacao da linha dos apses
    :param anomalia_verdadeira = algulo do vetor posicao e a linha dos apses com origem no foco
    :param inclinacao = inclinacao da orbita
    :param num_orbitas = numero de orbitas a serem simuladas
    :param delt = Time step for the integration
    :param psi = primeiro angulo de Euler
    :param teta = segundo angulo de Euler
    :param phi = terceiro angulo de Euler
    :param psip = velocidade angular do primeiro angulo de Euler
    :param tetap = velocidade angular do segundo angulo de Euler
    :param phip = velocidade angular do terceiro angulo de Euler
    :param massa = massa do cubesat
    :param largura = largura do cubsat
    :param comprimento = comprimento do cubesat
    :param altura = altura do cubesat
    :return df = Dataframe with informations about orbit and attitude
    """
    import numpy as np
    import pandas as pd
    from scipy.integrate import odeint
    from datetime import timedelta
    from nrlmsise00 import msise_model

    def propagador(q: list, t: float, rho: float, velocidade: float, massa: float, largura: float, comprimento: float,
                   altura: float, CD: float, posicao: float, Area_transversal: float):  # funcao para integrar
        import numpy as np

        # parametro gravitacional mu = GM
        mu = 398600
        # Parametro harmonico J2
        J2 = 1.08263e-3
        # Raio da Terra
        R_terra = 6371
        # vetor posicao inicial
        r = posicao
        m = massa  # massa do cubesat
        a = largura  # comprimento do sat
        b = comprimento  # largura do sat
        c = altura  # altura do sat
        Ix3 = (m / 12) * (b ** 2 + c ** 2)  # momento de inercia na direcao x
        Iy3 = (m / 12) * (a ** 2 + c ** 2)  # momento de inercia na direcao y
        Iz3 = (m / 12) * (a ** 2 + b ** 2)  # momento de inercia na direcao z

        # Condicoes inicial do propagador
        h, ecc, anomalia_verdadeira, raan, inc, arg_per = q

        # Equacoes diferenciais ordinarias
        dMdt = [r*((-1/(2*r))*h*rho*velocidade*((CD*Area_transversal)/m) - 1.5 * ((J2*mu*R_terra**2)/r**4) * np.sin(inc)**2*np.sin(2*(arg_per + anomalia_verdadeira))),

                (h/mu)*np.sin(anomalia_verdadeira)*((-1/(2*h))*mu*ecc*rho*velocidade*((CD*Area_transversal)/m)*np.sin(anomalia_verdadeira)
                - 1.5*((J2*mu*R_terra**2)/r**4)*(1 - 3*np.sin(inc)**2*np.sin(arg_per + anomalia_verdadeira)**2))
                + (((-1/(2*r))*h*rho*velocidade*((CD*Area_transversal)/m) - 1.5*((J2*mu*R_terra**2)/r**4)*np.sin(inc)**2*np.sin(2*(arg_per
                + anomalia_verdadeira)))/(mu*h))*((h**2 + mu*r)*np.cos(anomalia_verdadeira) + mu*ecc*r),

                (h/r**2 + ((h**2*np.cos(anomalia_verdadeira))/(mu*ecc*h))*((-1/(2*h))*mu*ecc*rho*velocidade*((CD*Area_transversal)/m)*np.sin(anomalia_verdadeira)
                - 1.5*((J2*mu*R_terra**2)/r**4)*(1 - 3*np.sin(inc)**2*np.sin(arg_per + anomalia_verdadeira)**2))
                - (r + h**2/mu)*(np.sin(anomalia_verdadeira)/(ecc*h))*((-1/(2*r))*h*rho*velocidade*((CD*Area_transversal)/m)
                - (1.5 * (J2*mu*R_terra**2)/r**4) * np.sin(inc)**2 * np.sin(2*(arg_per + anomalia_verdadeira)))),

                (r/(h*np.sin(inc)))*np.sin(arg_per + anomalia_verdadeira)*(- 1.5*((J2*mu*R_terra**2)/r**4)*np.sin(2*inc)*np.sin(arg_per + anomalia_verdadeira)),

                (r / (h)) * np.cos(arg_per + anomalia_verdadeira) * (- 1.5 * ((J2 * mu * R_terra ** 2) / r ** 4) * np.sin(2 * inc) * np.sin(arg_per + anomalia_verdadeira)),

                (-1/(ecc*h))*((h**2/mu)*np.cos(anomalia_verdadeira)*((-1/(2*h))*mu*ecc*rho*velocidade*((CD*Area_transversal)/m)*np.sin(anomalia_verdadeira)
                - 1.5*((J2*mu*R_terra**2)/r**4)*(1 - 3*np.sin(inc)**2*np.sin(arg_per + anomalia_verdadeira)**2))
                - (r + h**2/mu)*np.sin(anomalia_verdadeira)*((-1/(2*r))*h*rho*velocidade*((CD*Area_transversal)/m)
                - 1.5 * ((J2*mu*R_terra**2)/r**4) * np.sin(inc)**2 * np.sin(2*(arg_per + anomalia_verdadeira))))
                - ((r*np.sin(arg_per + anomalia_verdadeira))/(h*np.tan(inc)))*(- 1.5 * (J2*mu*R_terra**2)/r**4 * np.sin(2*inc) * np.sin(arg_per + anomalia_verdadeira))]
        return dMdt

    # Funcao para calcular a densidade atmosferica ao longo da orbita
    def densidade(data, altitude, latitude, longitude):
        """
        :param data: mes/dia/ano hora:minu:sec
        :param altitude: altitude da orbita
        :param latitude: latitude
        :param longitude: longitude
        :return: densidade da atmosfera em kg/m**3
        """
        densidade = msise_model(data, altitude, latitude, longitude, 150, 150, 4, lst=16)
        rho = densidade[0][5] * 1000
        return rho

    # condicoes iniciais

    SMA = float(semi_eixo)  # semi eixo maior
    ecc0 = float(excentricidade)  # ecentricidade da orbita
    raan0 = np.radians(float(raan))  # ascencao direita do nodo ascendente
    arg_per0 = np.radians(float(argumento_perigeu))  # argumento do perigeu
    true_anomaly0 = np.radians(float(anomalia_verdadeira))  # anomalia verdadeira
    inc0 = np.radians(float(inclinacao))  # inclinacao
    rp0 = SMA*(1-excentricidade) # semi eixo maior
    T_orb = periodo_orbital(SMA) # periodo medio da orbita
    mu = 398600 # parametro gravitacional mu = GM
    J2 = 1.08263e-3 # zona harmonica j2
    R_terra = 6371.0 # raio da terra
    h0 = np.sqrt(semi_eixo*mu*(1 - excentricidade**2)) # momento linear do satelite

    # Matriz de rotacao
    '''x_rot = np.cos(np.radians(argumento_perigeu)) * np.cos(np.radians(raan)) - np.cos(np.radians(inclinacao)) \
            * np.sin(np.radians(argumento_perigeu)) * np.sin(np.radians(raan))
    y_rot = np.cos(np.radians(argumento_perigeu)) * np.sin(np.radians(raan)) + np.cos(np.radians(inclinacao))\
            * np.sin(np.radians(argumento_perigeu)) * np.cos(np.radians(raan))
    z_rot = np.sin(np.radians(inclinacao)) * np.sin(np.radians(argumento_perigeu))'''

    phi = np.radians(raan)
    teta = np.radians(inclinacao)
    psi = np.radians(argumento_perigeu)

    Q_rot = np.array([[np.cos(psi) * np.cos(phi) - np.sin(psi) * np.sin(phi) * np.cos(teta),
                       np.cos(psi) * np.sin(phi) + np.sin(psi) * np.cos(teta) * np.cos(phi),
                       np.sin(psi) * np.sin(teta)],
                      [-np.sin(psi) * np.cos(phi) - np.cos(psi) * np.sin(phi) * np.cos(teta),
                       -np.sin(psi) * np.sin(phi) + np.cos(psi) * np.cos(teta) * np.cos(phi),
                       np.cos(psi) * np.sin(teta)],
                      [np.sin(teta) * np.sin(phi), -np.sin(teta) * np.cos(phi), np.cos(teta)]])
    h1 = np.sqrt(semi_eixo*mu*(1 - excentricidade**2))

    ano = [np.cos(np.radians(anomalia_verdadeira)), np.sin(np.radians(anomalia_verdadeira)), 0]
    r = [((h1**2/mu)*1/(1 + excentricidade*np.cos(np.radians(anomalia_verdadeira)))) * a for a in ano]
    # print(r)
    Posi_ini = np.dot(np.transpose(Q_rot), r)
    # print(Posi_ini)
    lamb_e = raan0  # (np.arctan2(Posi_ini[1], Posi_ini[0]))
    latitude0 = np.degrees((np.arcsin(Posi_ini[2] / np.linalg.norm(Posi_ini))))
    longitude0 = np.degrees((np.arctan2(Posi_ini[1], Posi_ini[0])))
    # print(f'latitude0: {latitude0}')
    # print(f'longitude0: {longitude0}')
    '''import pyproj
    input_proj = pyproj.CRS.from_epsg(4328)
    # Define o sistema de coordenadas de saída (geográfico)
    output_proj = pyproj.CRS.from_epsg(4326)
    # Cria um objeto Transformer para realizar a transformação de coordenadas
    transformer = pyproj.transformer.Transformer.from_crs(input_proj, output_proj)
    # Converte as coordenadas do sistema de coordenadas geocêntricas para o sistema de coordenadas geográficas
    longitude0, latitude0, alt = transformer.transform(b[0] * 1000.0, b[1] * 1000.0, b[2] * 1000.0, radians=True)'''

    lat = [latitude0]
    long = [longitude0]

    # comeco da integracao

    DELTAT = delt
    mu = 398600
    J2 = 1.08263e-3
    R_terra = 6371
    Time_step = delt
    passo = 10
    ini_date = data
    n = num_orbitas
    T = T_orb*n
    t = np.linspace(0, Time_step, passo)
    data = [ini_date]
    solution = [[h0, ecc0, true_anomaly0, raan0, inc0, arg_per0]]
    time_simu = [0]
    cont = 0
    r = []
    # while cont < T:

    for i in range(0,int(T)+1, int(delt)):
        qi = [h0, ecc0, true_anomaly0, raan0, inc0, arg_per0]
        altitude = rp0 - R_terra
        latitude = lat[-1]
        longitude = long[-1]
        posicao = (h0**2/mu)*(1/(1-ecc0*np.cos(true_anomaly0)))
        air_density = densidade(ini_date, altitude, latitude, longitude)
        velocidade = (mu/h0)*np.sqrt(np.sin(true_anomaly0)**2 + (ecc0 + np.cos(true_anomaly0))**2)*1000.0
        massa = massa
        CD = 2.2
        Area_transversal = 0.1*0.1
        largura = largura
        comprimento = comprimento
        altura = altura
        sol = odeint(propagador, qi, t, args=(air_density, velocidade, massa, largura, comprimento, altura, CD, posicao, Area_transversal))
        solution.append(sol[-1])
        h0 = sol[-1][0]
        ecc0 = sol[-1][1]
        true_anomaly0 = sol[-1][2]
        raan0 = sol[-1][3]
        inc0 = sol[-1][4]
        arg_per0 = sol[-1][5]
        SMA = (h0**2/mu) * (1 / (1 - ecc0**2))
        rp0 = SMA*(1-ecc0)
        cont = cont + Time_step
        time_simu.append(cont)
        final_date = timedelta(seconds=Time_step)
        ini_date = ini_date + final_date
        data.append(ini_date)

        # Calculo da longitude e latitude no ECEF

        xp = (h0 ** 2 / mu) * (1 / (1 + ecc0 * np.cos(true_anomaly0))) * np.cos(true_anomaly0)
        yp = (h0 ** 2 / mu) * (1 / (1 + ecc0 * np.cos(true_anomaly0))) * np.sin(true_anomaly0)
        zp = 0
        r_p = [xp, yp, zp]

        lamb_e = lamb_e - ((2*np.pi)/(23*3600 + 56*60 + 4))*DELTAT

        '''X_ECEF = ((np.cos(lamb_e) * np.cos(arg_per0) - np.sin(lamb_e) * np.sin(arg_per0) * np.cos(inc0)) * xp
                 + (-np.cos(lamb_e) * np.sin(arg_per0) - np.sin(lamb_e) * np.cos(inc0) * np.cos(arg_per0)) * yp
                 + np.sin(lamb_e) * np.sin(inc0) * zp)
        Y_ECEF = ((np.sin(lamb_e) * np.cos(arg_per0) + np.cos(lamb_e) * np.cos(inc0) * np.sin(arg_per0)) * xp
                 + (-np.sin(lamb_e) * np.sin(arg_per0) + np.cos(lamb_e) * np.cos(inc0) * np.cos(arg_per0)) * yp
                 - np.cos(lamb_e) * np.sin(inc0) * zp)
        Z_ECEF = (np.sin(inc0) * np.sin(arg_per0) * xp
                 + np.sin(inc0) * np.cos(arg_per0) * yp
                 + np.cos(inc0) * zp)'''

        phi = lamb_e
        teta = inc0
        psi = arg_per0

        Q_rot = np.array([[np.cos(psi) * np.cos(phi) - np.sin(psi) * np.sin(phi) * np.cos(teta),
                           np.cos(psi) * np.sin(phi) + np.sin(psi) * np.cos(teta) * np.cos(phi),
                           np.sin(psi) * np.sin(teta)],
                          [-np.sin(psi) * np.cos(phi) - np.cos(psi) * np.sin(phi) * np.cos(teta),
                           -np.sin(psi) * np.sin(phi) + np.cos(psi) * np.cos(teta) * np.cos(phi),
                           np.cos(psi) * np.sin(teta)],
                          [np.sin(teta) * np.sin(phi), -np.sin(teta) * np.cos(phi), np.cos(teta)]])
        R_ECEF = np.dot(np.transpose(Q_rot), r_p)
        r.append(np.array(R_ECEF))

        latitude = (np.arcsin(R_ECEF[2]/np.linalg.norm(R_ECEF)))

        longitude = (np.arctan2(R_ECEF[1], R_ECEF[0]))

        '''import pyproj
        input_proj = pyproj.CRS.from_epsg(4328)
        # Define o sistema de coordenadas de saída (geográfico)
        output_proj = pyproj.CRS.from_epsg(4326)
        # Cria um objeto Transformer para realizar a transformação de coordenadas
        transformer = pyproj.transformer.Transformer.from_crs(input_proj, output_proj)
        # Converte as coordenadas do sistema de coordenadas geocêntricas para o sistema de coordenadas geográficas
        longitude, latitude, alt = transformer.transform(X_ECEF*1000.0, Y_ECEF*1000.0, Z_ECEF*1000.0, radians=True)'''

        lat.append(np.degrees(latitude))
        long.append(np.degrees(longitude))
    import os.path
    r = pd.DataFrame(r, columns=['rx', 'ry', 'rz'])
    dfdata = pd.DataFrame(data, columns=['Data'])
    r = pd.concat([r, dfdata], axis=1)
    r['latitude'] = np.degrees(np.arcsin(r['rz'] / (r['rx']**2 + r['ry']**2 + r['rz']**2)**0.5))
    r['longitude'] = np.degrees(np.arctan2(r['ry'], r['rx']))
    r['r'] = np.sqrt(r['rx']**2 + r['ry']**2 + r['rz']**2)
    r['end'] = 'end'
    # r.to_csv(os.path.join('./results/', 'ECEF_R.csv'), sep=',')

    return r


def periodo_orbital(Perigeu):
    """
    Perigeu = Altitude Inicial do Satelite no perigeu
    """
    import numpy as np
    mu = 398600
    T_orb = float(((2 * np.pi) / (np.sqrt(mu))) * (Perigeu ** (3 / 2)))
    return (T_orb)


def calculacomunicacao(df, lat_gs, long_gs, elev):
    """
    :param df: DataFrame de rx, ry e rz do CubeSat:
    :param lat_gs: Latitude da Groundd Station em Graus (Norte)
    :param long_gs: Longitude da Groundd Station em Graus (Leste)
    :param elev: Elevação mínima para comunicação da antena em graus
    :return: df + Ângulo de elevação, Vetor de contato e a Distância sat-gs
    """

    Contato = []
    for i in range(df[df.columns[0]].count()):
        dt = 10
        R_E = 6371.00  # raio da Terra em km

        VetorTerraEstacao = np.array([R_E * np.cos(lat_gs) * np.cos(long_gs), R_E * np.cos(lat_gs) * np.sin(long_gs), R_E * np.sin(lat_gs)])

        VetorSatelite = np.array([df.iloc[i, df.columns.get_loc('rx')], df.iloc[i, df.columns.get_loc('ry')], df.iloc[i, df.columns.get_loc('rz')]])

        VetorSateliteEstacao = VetorSatelite - VetorTerraEstacao

        # Critério de Comunicação
        AComunicacao = np.pi \
                - np.arccos((np.dot(VetorSatelite, VetorSateliteEstacao))/(np.linalg.norm(VetorSatelite)*np.linalg.norm(VetorSateliteEstacao))) \
                - np.arccos((np.dot(VetorTerraEstacao, VetorSatelite))/(np.linalg.norm(VetorTerraEstacao)*np.linalg.norm(VetorSatelite)))

        if AComunicacao >= np.radians(90+elev):
            Contato.append(1)
        else:
            Contato.append(0)

        df6 = pd.DataFrame(AComunicacao, columns=['Ângulo Elevação'])
        df = pd.concat([df, df6], axis=1)
        df7 = pd.DataFrame(Contato, columns=['Contato'])
        df = pd.concat([df, df7], axis=1)
        df8 = pd.DataFrame(VetorSateliteEstacao, columns=['Distância'])
        df = pd.concat([df, df8], axis=1)
        df["end"] = None
        df.to_csv("Tempo de comunicação.csv", sep=',')

        return df


def tempocontato(df):

    Contato = df['Contato'].tolist()

    if Contato[0] == 1:
        start = np.concatenate((np.array([-1]), np.where(np.diff(Contato) == 1)[0]))
    else:
        start = np.where(np.diff(Contato) == 1)[0]

    if Contato[-1] == 1:
        end = np.concatenate((np.where(np.diff(Contato) == -1)[0], np.array([len(Contato)-1])))
    else:
        end = np.where(np.diff(Contato) == -1)[0]

    tempodecontato = end-start                              # Tempo de contato
    npassagens = len(start)                                 # Número de passagens

    datas = [x.date() for x in df['Data']]
    dias = np.unique(datas)

    passagens = []
    for dia in dias:
        count = 0
        for passagem, comunica in zip(datas, Contato):
            if passagem == dia and comunica == 1:
                count += 1
        passagens.append(count)


    return


if __name__ == '__main__':
    from datetime import datetime
    import numpy as np
    import pandas as pd
    import os
    import sys

    input_string = ' 11/10/2022 18:00:00'
    data = datetime.strptime(input_string, " %m/%d/%Y %H:%M:%S")
    df = propagador_orbital(data, 7000.0, 0.002, 0.0, 0.0, 0.0, 38.30837095, 2, 10, 3.0, 0.1, 0.1, 0.2)

# (data, SMA, e, Raan, argumento_perigeu, anomalia_verdadeira, inc, n_orb, delt, massa, largura, comprimento, altura)
    """
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)
    """

    '''
    # plt3d(df)
    # plot_groundtrack_2D(df)
    # print(list(r.columns.values))
    print(list(df.columns.values))
    print(df)
    '''

    '''
    df2 = calculacomunicacao(df, -5.871778, -35.206864,15)

    df2 = df2[0:-1]
    index = df2["Contato"].tolist()
    Tempo = df2["Data"].tolist()

    index = df2["Contato"].tolist()
    Tempo = df2["Data"].tolist()
    dias = [x for x in Tempo.date()]
    
    passagens = []
    for dia in dias:
        count = 0
        for passagem, comunica in zip(datas, index):
            if passagem == dia and comunica == 1:
                count += 1
        passagens.append(count)
    '''