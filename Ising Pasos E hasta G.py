import numpy as np
import random
import matplotlib.pyplot as plt
import statistics as sts

N = 20
J = 1
Pasos = 2000
PasosLista = list(range(1,Pasos+1))
kbT = np.linspace(0.01,5,5)
print(kbT)

"""
def ConfInicial(N):
    espines = [1, -1]
    arreglo = []
    for i in range(N):
        k = random.choice(espines)
        arreglo.append(k)
    arreglo[0] = arreglo[N - 1]
    return arreglo
"""

def EnergíaConfInicial(arreglo):
    EnergiaInicial = 0
    for i in range(len(arreglo) - 1):
        EnergiaEspin = -J * arreglo[i] * arreglo[i + 1]
        EnergiaInicial = EnergiaInicial + EnergiaEspin
    return EnergiaInicial

def Magnetizacion(Resultado,Pasos):
    listaMag = []
    for i in range (0,Pasos):
        for j in range (len(Resultado[i])):
            suma = sum(Resultado[i])
        listaMag.append(suma)
    return listaMag

def EnergiaInterna(Resultado,Pasos):
    registroEnergia = []
    for k in range(0,Pasos):
        EnergiaEstado = 0
        for j in range (len(Resultado[k])-1):
            EnergiaEspin = -J * Resultado[k][j] * Resultado[k][j + 1]  # Se calcula la nueva energía
            EnergiaEstado = EnergiaEstado + EnergiaEspin
        registroEnergia.append(EnergiaEstado)
    return registroEnergia


def Ising(EnergiaInicial,Pasos,N,arreglo,kbT):
    MatrizEspinPaso = []
    registroEnergia = []
    for j in range(Pasos):
        EnergiaEstado = 0
        arreglo[0] = arreglo[N - 1]
        jEspin = np.random.randint(N)  # Se elige un espín aleatorio
        arreglo[jEspin] = arreglo[jEspin] * -1  # Se cambia la dirección del espín
        for k in range(len(arreglo) - 1):
            EnergiaEspin = -J * arreglo[k] * arreglo[k + 1]  # Se calcula la nueva energía
            EnergiaEstado = EnergiaEstado + EnergiaEspin
        deltaE = EnergiaEstado - EnergiaInicial
        Probabilidad = np.exp(-deltaE/kbT)  # Se calcula la probabilidad de aceptación para cambios a un estado de energía mayor
        # algoritmo metrópolis
        if deltaE < 0:
            EnergiaInicial = EnergiaEstado
        if deltaE > 0:
            if np.random.random() < Probabilidad:
                EnergiaInicial = EnergiaEstado
            else:
                arreglo[jEspin] = arreglo[jEspin] * -1
                EnergiaInicial = EnergiaInicial
        registroEnergia.append(EnergiaInicial)
        MatrizEspinPaso.append(arreglo.copy())  # Arreglo que contiene la evolución de los espines en el tiempo
    return MatrizEspinPaso

def CalorEspecifico(promEnergia,kbT,Pasos):
    promEnergiaCuadrado = promEnergia**2
    calor = (1/(Pasos/2)**2)*(sts.mean(promEnergiaCuadrado[999:1999])-sts.mean(promEnergia[999:1999])**2)/(kbT**2)
    return calor

Configuracion = np.ones(N)*-1
Energia0 = EnergíaConfInicial(Configuracion)
promMagne = []
promEner = []
MagnetismoTemperatura = []
EnergiaTemperatura = []
CalorTemperatura = []

for m in range (0,len(kbT)):
    print(m)
    Temperatura = kbT[m]
    promMagne = []
    promEner = []
    for k in range (200):
        Resultado = np.array(Ising(Energia0,Pasos,N,Configuracion.copy(),Temperatura))
        Magnetismo = Magnetizacion(Resultado,Pasos)
        EI = EnergiaInterna(Resultado, Pasos)
        promMagne.append(Magnetismo)
        promEner.append(EI)
    promMagnetismo = np.array(promMagne).mean(0)
    promEnergia = np.array(promEner).mean(0)
    MagnetismoTemperatura.append(sts.mean(promMagnetismo[999:1999]))
    EnergiaTemperatura.append(sts.mean(promEnergia[999:1999]))
    CE = CalorEspecifico(promEnergia,Temperatura,Pasos)
    CalorTemperatura.append(CE)

fig1 = plt.figure(1)
plt.imshow(Resultado.T, aspect=20, interpolation='none')
plt.xlabel('Pasos')

fig2 = plt.figure(2)
plt.plot(kbT,MagnetismoTemperatura)
plt.xlabel('kbT')
plt.ylabel('Magnetismo')

fig3 = plt.figure(3)
plt.plot(kbT,EnergiaTemperatura)
plt.xlabel('kbT')
plt.ylabel('Energía Interna')

fig4 = plt.figure(4)
plt.plot(kbT,CalorTemperatura)
plt.xlabel('kbT')
plt.ylabel('CalorEspecífico')

plt.show()


