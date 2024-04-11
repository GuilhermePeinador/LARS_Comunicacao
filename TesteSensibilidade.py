import sys
import argparse
import pickle
import pandas as pd
import numpy as np
import LARS
#import Fit_Func
from datetime import datetime
from pyDOE import *

# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../src-LARS')

parser = argparse.ArgumentParser(description='Implementação para analise de sensibilidade da orbita lançada em 2024')

parser.add_argument("--file",  default="SensitID0.case", type=str)
parser.add_argument("--ID",    default="ID0", type=str)
parser.add_argument("--sma1",  metavar='sma1',  default=6900, type=float, help='Semi-Major Axis do satélite 1')
parser.add_argument("--sma2",  metavar='sma2',  default=6900, type=float, help='Semi-Major Axis do satélite 2')
parser.add_argument("--sma3",  metavar='sma3',  default=6900, type=float, help='Semi-Major Axis do satélite 3')
parser.add_argument("--inc1",  metavar='inc1',  default=98,   type=float, help='Inclinação do satélite 1')
parser.add_argument("--inc2",  metavar='inc2',  default=98,   type=float, help='Inclinação do satélite 2')
parser.add_argument("--inc3",  metavar='inc3',  default=98,   type=float, help='Inclinação do satélite 3')
parser.add_argument("--raan1", metavar='raan1', default=0,    type=float, help='Longitude of the ascending node do satélite 1')
parser.add_argument("--raan2", metavar='raan2', default=0,    type=float, help='Longitude of the ascending node do satélite 2')
parser.add_argument("--raan3", metavar='raan3', default=0,    type=float, help='Longitude of the ascending node do satélite 3')
parser.add_argument("--samples", type=int, default=50)
parser.add_argument("--njobs",   type=int, default=1)

filename =  parser.parse_args().file
ID    = parser.parse_args().ID
sma1  = parser.parse_args().sma1
sma2  = parser.parse_args().sma2
sma3  = parser.parse_args().sma3
inc1  = parser.parse_args().inc1
inc2  = parser.parse_args().inc2
inc3  = parser.parse_args().inc3
raan1 = parser.parse_args().raan1
raan2 = parser.parse_args().raan2
raan3 = parser.parse_args().raan3
nsamples = parser.parse_args().samples
njobs    = parser.parse_args().njobs

ub = np.array([360, 360, 180, 7000])
lb = np.array([0,   0,     0,  6850])
Sampling = lhs(n=4, samples=nsamples)*(ub-lb)+lb

arraydeentrada = (ID, sma1, sma2, sma3, inc1, inc2, inc3, raan1, raan2, raan3)


def Sampling(arraydeentrada):

    ID    = arraydeentrada[0]
    sma1  = arraydeentrada[1]
    sma2  = arraydeentrada[2]
    sma3  = arraydeentrada[3]
    inc1  = arraydeentrada[4]
    inc2  = arraydeentrada[5]
    inc3  = arraydeentrada[6]
    raan1 = arraydeentrada[7]
    raan2 = arraydeentrada[8]
    raan3 = arraydeentrada[9]

    norbs = 10
    # data_inicial = datetime.strptime('11/01/2024 18:00:00', " %m/%d/%Y %H:%M:%S")
    data = datetime(2024, 11, 1, 18, 0, 0)

    print('Runing Sat 1')
    df1 = LARS.propagador_orbital(data, sma1, 0.002, raan1, 0.0, 0.0, inc1, norbs, 10, 3.0, 0.1, 0.1, 0.2)
    print('Runing Sat 2')
    df2 = LARS.propagador_orbital(data, sma2, 0.002, raan2, 0.0, 0.0, inc2, norbs, 10, 3.0, 0.1, 0.1, 0.2)
    print('Runing Sat 3')
    df3 = LARS.propagador_orbital(data, sma3, 0.002, raan3, 0.0, 0.0, inc3, norbs, 10, 3.0, 0.1, 0.1, 0.2)

    file = open(filename, 'wb')
    pickle.dump([ID, df1, df2, df3, [sma1, sma2, sma3], [inc1, inc2, inc3], [raan1, raan2, raan3]], file)
    file.close()

    # Dataframe para o cálculo dos parâmetros de comunicação -------------------

    dfcomunicacao1 = LARS.calculacomunicacao(df1)
    dfcomunicacao2 = LARS.calculacomunicacao(df2)
    dfcomunicacao3 = LARS.calculacomunicacao(df3)

    # Salvando dados de comunicação -------

    dfcomunicacao1.drop(["rx", "ry", "rz", "end"], axis=1, inplace=True)
    dfcomunicacao2.drop(["rx", "ry", "rz", "end"], axis=1, inplace=True)
    dfcomunicacao3.drop(["rx", "ry", "rz", "end"], axis=1, inplace=True)

    pd.to_pickle(dfcomunicacao1, "dataframecomunicacao")
    pd.to_pickle(dfcomunicacao2, "dataframecomunicacao")
    pd.to_pickle(dfcomunicacao3, "dataframecomunicacao")

    tempodecontato, npassagens, passagens, datasunicas, passagenspordia = LARS.tempocontato(dfcomunicacao1)
    np.savez('dadoscomunicacao1',temcaonta=tempodecontato, npass=npassagens, passa=passagens, datas=datasunicas, passperday=passagenspordia)

    tempodecontato, npassagens, passagens, datasunicas, passagenspordia = LARS.tempocontato(dfcomunicacao2)
    np.savez('dadoscomunicacao2', temcaonta=tempodecontato, npass=npassagens, passa=passagens, datas=datasunicas, passperday=passagenspordia)

    tempodecontato, npassagens, passagens, datasunicas, passagenspordia = LARS.tempocontato(dfcomunicacao3)
    np.savez('dadoscomunicacao3', temcaonta=tempodecontato, npass=npassagens, passa=passagens, datas=datasunicas, passperday=passagenspordia)

    return


'''
 To load the data
file = open(filename,'rb')
a = pickle.load(file)
file.close()
'''
