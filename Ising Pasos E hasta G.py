import numpy as np
import random
import matplotlib.pyplot as plt
import statistics as sts

N = 20 #Número de espines en cada configuración
J = 1 #Energía de intercambio
Pasos = 2000 #Cantidad de iteraciones para el modelo
PasosLista = list(range(1,Pasos+1))
kbT = np.linspace(0.01,5,30)  #Temperaturas a evaluar
print(kbT)

#Esta función calcula cual es la energía del estado inicial.
#Recibe el arreglo de espines y entrega la energía correspondiente.


def ConfInicial(N):
    espines = [1, -1]
    arreglo = []
    for i in range(N):
        k = random.choice(espines)
        arreglo.append(k)
    arreglo[0] = arreglo[N - 1]
    return arreglo

def EnergíaConfInicial(arreglo):
    """
    Esta función calcula cual es la energía del estado inicial.
    Recibe el arreglo de espines y entrega la energía correspondiente.
    """
    EnergiaInicial = 0
    for i in range(len(arreglo) - 1):
        EnergiaEspin = -J * arreglo[i] * arreglo[i + 1]
        EnergiaInicial = EnergiaInicial + EnergiaEspin
    return EnergiaInicial

def Magnetizacion(Resultado,Pasos):
    """
        Esta función calcula la magnetización de cada configuración de espines.
        Recibe la matriz con la evolución de la configuración inicial en el tiempo.
        Entrega una lista con la magnetización de cada configuración en el tiempo.
    """
    listaMag = []
    for i in range (0,Pasos):
        for j in range (len(Resultado[i])):
            suma = sum(Resultado[i])
        listaMag.append(suma)
    return listaMag

def EnergiaInterna(Resultado,Pasos):
    """
        Esta función calcula la energía interna a una temperatura determinada.
        Recibe la matriz con la evolución de la configuración inicial en el tiempo.
        Entrega una lista con la energía de cada configuración en el tiempo. La energía interna será el promedio de los
        valores en el equilibrio.
    """
    registroEnergia = []
    for k in range(0,Pasos):
        EnergiaEstado = 0
        for j in range (len(Resultado[k])-1):
            EnergiaEspin = -J * Resultado[k][j] * Resultado[k][j + 1]
            EnergiaEstado = EnergiaEstado + EnergiaEspin
        registroEnergia.append(EnergiaEstado)
    return registroEnergia


def Ising(EnergiaInicial,Pasos,N,arreglo,kbT):
    """
        :param EnergiaInicial: Energía de la configuración de espines iniciales
        :param Pasos: Cantidad de iteraciones que se van a realizar sobre el arreglo de espines
        :param N: Número de espines por configuración
        :param arreglo: Configuración inicial de espines
        :param kbT: Temperatura a evaluar
        :return: Una matriz que contiene la evolución del arreglo de espines a lo largo del tiempo.
    """
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

def CalorEspecifico(promEnergia,kbT,N):
    """
        Esta función calcula el calor específico a una temperatura determinada.
        Recibe una matriz que contiene la energía interna para todas las configuraciones de espines.
        Entrega el valor de calor específico correspondiente a esa temperatura.
    """
    promEnergiaCuadrado = promEnergia**2
    calor = (1/(N)**2)*(sts.mean(promEnergiaCuadrado[999:1999])-sts.mean(promEnergia[999:1999])**2)/(kbT**2)
    return calor

#Se llama a la configuración inicial
Configuracion = np.ones(N)
#Se llama a la energía de la configuración inicial
Energia0 = EnergíaConfInicial(Configuracion)
promMagne = []
promEner = []
MagnetismoTemperatura = []
EnergiaTemperatura = []
CalorTemperatura = []

#Por cada temperatura que se desea evaluar, el código encuentra los valores promedios de magnetización, energía interna
#y calor específico y las almacena en listas para posteriormente ser graficadas.
for m in range (0,len(kbT)):
    print(m+1, "de", len(kbT))
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
    CE = CalorEspecifico(promEnergia,Temperatura,N)
    CalorTemperatura.append(CE)

#Se grafican los resultados
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


