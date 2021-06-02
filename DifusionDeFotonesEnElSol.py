# Importación de librerías

import numpy as np
import matplotlib.pyplot as plt

# Parámetros globales

l = 5 * 10 ** (-5)  # camino libre medio del fotón, en metros
R = 5 * 10 ** (-3)  # radio máximo que alcanzan los fotones, en metros
c = 299792458  # velocidad de los fotones, en metros por segundo


# Definición de funciones

def PasosCaminoLibreMedio():
    """
    Genera los componentes x,y,z de un paso aleatorio del tamaño del camino libre medio
    :return: tres floats que corresponden a los componentes del paso en x,y,z
    """

    # Genera componentes aleatorias
    deltaX = (np.random.random() - 0.5) * 2
    deltaY = (np.random.random() - 0.5) * 2
    deltaZ = (np.random.random() - 0.5) * 2

    # Normaliza para crear un paso unitario, dividiendo entre la norma
    L = (deltaX ** 2 + deltaY ** 2 + deltaZ ** 2) ** (1 / 2)
    deltaXNorm = deltaX / L
    deltaYNorm = deltaY / L
    deltaZNorm = deltaZ / L

    # Multiplica el paso unitario por la magnitud del camino libre
    return deltaXNorm * l, deltaYNorm * l, deltaZNorm * l


def DarPaso(lista_Pos, guardarPaso=True):
    """
    Genera un par ordenado aleatorio respecto al punto anterior
    :param lista_Pos: lista que almacena las componentes x,y,z para todas las iteraciones
    :param guardarPaso: booleano, indica si se van a guardar todas las posiciones del camino o no
    :return: lista_Pos actualizada con las coordenadas del par ordenado de la nueva posición
    """

    # Calcula los componentes del paso
    deltaX, deltaY, deltaZ = PasosCaminoLibreMedio()

    # A la posición anterior le suma el paso en cada componente para obtener la nueva posición
    nuevaXPos = lista_Pos[0][- 1] + deltaX
    nuevaYPos = lista_Pos[1][- 1] + deltaY
    nuevaZPos = lista_Pos[2][- 1] + deltaZ

    if guardarPaso==True:
        # Se almacenan las componentes del par ordenado obtenido en esta iteración
        lista_Pos[0].append(nuevaXPos)
        lista_Pos[1].append(nuevaYPos)
        lista_Pos[2].append(nuevaZPos)
    else:
        lista_Pos[0][0]=nuevaXPos
        lista_Pos[1][0]=nuevaYPos
        lista_Pos[2][0]=nuevaZPos
    return lista_Pos


def CalcularR2(lista_Pos):
    """
    Calcula el R cuadrado para el último par ordenado de lista_Pos
    :param lista_Pos: lista que almacena las componentes x,y,z para todas las iteraciones
    :return: float R cuadrado
    """
    x = lista_Pos[0][-1]
    y = lista_Pos[1][-1]
    z = lista_Pos[2][-1]
    R2 = x ** 2 + y ** 2 + z ** 2
    return R2

def CaminarHastaR(guardarCamino=True):
    """
    Realiza un camino aleatorio hasta que el fotón llegue a R
    :param guardarCamino: booleano, indica si se van a guardar todas las posiciones del camino o no
    :return:    lista caminoFoton, lista con las posiciones del fotón en cada paso
                entero N, número de pasos que debe hacer el fotón para llegar a R
    """
    # Se inicializa la lista que almacena las posiciones del fotón durante el camino aleatorio
    caminoFoton = [[0.],[0.],[0.]]
    # Se calcula el radio inicial
    rFoton = np.sqrt(CalcularR2(caminoFoton))
    # Se inicializa el contador de pasos
    N = 0

    # Se realizan pasos hasta llegar a R
    while rFoton < R:
        N += 1
        caminoFoton = DarPaso(caminoFoton,guardarCamino)
        rFoton = np.sqrt(CalcularR2(caminoFoton))
    return caminoFoton, N


def EstimarN(k):
    """
    :param k: número de caminos a realizar para calcular el N promedio
    Camina hasta R k veces y calcula el número de pasos promedio
    :return: float NProm, número de pasos promedio para llegar a R
    """
    # Crea la lista donde se almacenarán los k N
    listaN = []

    for i in range(0,k):
        caminoFoton, kN = CaminarHastaR(False)
        listaN.append(kN)

    NProm = sum(listaN)/len(listaN)
    return NProm


def GraficarCamino(camino):
    """
    Grafica en 3D el camino del fotón
    :param camino: Lista con todos los pares ordenados del fotón durante el camino aleatorio
    :return: Muestra gráfica del camino del fotón
    """
    # Para graficar una esfera de radio R
    u = np.linspace(0, np.pi, 30)
    v = np.linspace(0, 2 * np.pi, 30)
    x = np.outer(np.sin(u), np.sin(v)) * R
    y = np.outer(np.sin(u), np.cos(v)) * R
    z = np.outer(np.cos(u), np.ones_like(v)) * R

    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_zlabel("z (m)")
    # Esfera
    ax.plot_wireframe(x, y, z, color='y', alpha=0.2)
    # Camino aleatorio
    ax.plot3D(camino[0], camino[1], camino[2], linewidth=0.4)
    # Posición inicial
    ax.scatter(camino[0][0], camino[1][0], camino[2][0], color='g')
    #Posición final
    ax.scatter(camino[0][-1], camino[1][-1], camino[2][-1], color='r')
    ax.set_title("Camino aleatorio 3D del fotón")
    plt.show()

def main():
    # Estimación del número de pasos N de longitud l que debe dar un fotón hasta alcanzar el radio R usando Rrms

    # Se despeja N de la ecuación Rrms = np.sqrt(N)*rrms
    rrms = l
    Rrms = R
    NRrms = Rrms**2/rrms**2
    print('Estimación de la cantidad de pasos N en llegar a R (analítica): '+str(NRrms))

    # Se estima con simulación computacional
    k = int(np.sqrt(NRrms))+1  # Para calcular la cantidad de trials a hacer su utiliza el N obtenido por métodos analíticos
    NSimulacion = EstimarN(k)
    print('Estimación de la cantidad de pasos N en llegar a R (simulación): '+str(NSimulacion))

    # Se calcula la diferencia porcentual entre los dos valores encontrados para N
    diferenciaN = 100*(NSimulacion-NRrms)/NRrms
    print('Diferencia porcentual N: '+str(diferenciaN)+' %')

    # Se calcula la cantidad de años en llegar a R
    añosRrms = (NRrms*l)/(c*31536000)
    añosSimulacion = (NSimulacion*l)/(c*31536000)
    print('Estimación del tiempo en llegar a R en años (analítica): '+str(añosRrms))
    print('Estimación del tiempo en llegar a R en años (simulación): '+str(añosSimulacion))

    # Se grafica un camino aleatorio hasta R
    caminoFoton, N = CaminarHastaR()
    GraficarCamino(caminoFoton)


if __name__ == '__main__':
    main()