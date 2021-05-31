import numpy as np
import matplotlib.pyplot as plt

def EnergiaInterna (kbT,N,J):
    """
    Landau, ecuación 15.7
    :param kbT:Temperatura
    :param N: Número de espines
    :param J: Energía de intercambio
    :return: Energía interna
    """
    U = -N*np.tanh(J**2/kbT)
    return U

def CalorEspecifico (kbT,J):
    """
    Landau, ecuación 15.8
    :param kbT: Temperatura
    :param J: Energía de intercambio
    :return: Carlor Específico
    """
    C = ((J/kbT)**2)/(np.cosh(J/kbT)**2)
    return C

def Magnetismo (kbT,N,B,J):
    """
    Landau, ecuación 15.9
    :param kbT: Temperatura
    :param N: Número de espines
    :param B: Campo magnético
    :param J: Energía de intercambio
    :return: Magnetizacion
    """
    M = (-N*np.exp(J/kbT)*np.sinh(B/kbT))/(np.exp(2*J/kbT)*np.sinh(B/kbT)**2+np.exp(-2*J/kbT))**(1/2)
    return M

N = 20
J = 1
kbT = kbT = np.linspace(0.01,5,100)
B = 0.01
uLista = []
cLista = []
mLista = []
#Calcula la energía interna, el calor específico y el magnetismo en función de la temperatura
for i in range(0, len(kbT)):
    uLista.append(EnergiaInterna (kbT[i],N,J))
    cLista.append(CalorEspecifico(kbT[i],J))
    mLista.append(Magnetismo (kbT[i],N,B,J))

#Grafica los resultados
fig1 = plt.figure(1)
plt.plot(kbT,uLista)
plt.xlabel('kbT')
plt.ylabel('Energía Interna')

fig2 = plt.figure(2)
plt.plot(kbT,cLista)
plt.xlabel('kbT')
plt.ylabel('Calor Específico')

fig3 = plt.figure(3)
plt.plot(kbT,mLista)
plt.xlabel('kbT')
plt.ylabel('Magnetización')
plt.show()