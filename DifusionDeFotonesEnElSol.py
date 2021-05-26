# Importación de librerías

import numpy as np
import matplotlib.pyplot as plt

# Parámetros globales

l = 5 * 10 ** (-5)  # camino libre medio del fotón, en metros
R = 5 * 10 ** (-3)  # radio máximo que alcanzan los fotones, en metros ¡¡¡¡¡¡CAMBIAR!!!!!
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


def DarPaso(lista_Pos, nIter):
    """
    Genera un par ordenado aleatorio respecto al punto anterior
    :param lista_Pos: lista que almacena las componentes x,y,z para todas las iteraciones
    :param nIter: iteración para la cual se está calculando el par ordenado
    :return: lista_Pos actualizada con las posiciones del par ordenado para esta iteración
    """

    # Calcula los componentes del paso
    deltaX, deltaY, deltaZ = PasosCaminoLibreMedio()

    # A la posición anterior le suma el paso en cada componente para obtener la nueva posición
    nuevaXPos = lista_Pos[0][nIter - 1] + deltaX
    nuevaYPos = lista_Pos[1][nIter - 1] + deltaY
    nuevaZPos = lista_Pos[2][nIter - 1] + deltaZ

    # Se almacenan las componentes del par ordenado obtenido en esta iteración
    lista_Pos[0].append(nuevaXPos)
    lista_Pos[1].append(nuevaYPos)
    lista_Pos[2].append(nuevaZPos)
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

def CaminarHastaR():
    """
    Realiza un camino aleatorio hasta que el fotón llegue a R
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
        caminoFoton = DarPaso(caminoFoton,N)
        rFoton = np.sqrt(CalcularR2(caminoFoton))
    return caminoFoton, N


def EstimarN(k):
    """
    Camina hasta R k veces y calcula el número de pasos promedio
    :return: float NProm, número de pasos promedio para llegar a R
    """
    # Crea la lista donde se almacenarán los k N
    listaN = []
    for i in range(0,k):
        caminoFoton, kN = CaminarHastaR()
        listaN.append(kN)
    NProm = sum(listaN)/len(listaN)
    return NProm


def GraficarCamino(camino):
    """
    Grafica en 3D el camino del fotón
    :param camino: Lista con todos los pares ordenados del fotón durante el camino aleatorio
    :return: Muestra gráfica del camino del fotón
    """
    u = np.linspace(0, np.pi, 30)
    v = np.linspace(0, 2 * np.pi, 30)
    x = np.outer(np.sin(u), np.sin(v)) * R
    y = np.outer(np.sin(u), np.cos(v)) * R
    z = np.outer(np.cos(u), np.ones_like(v)) * R

    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.plot_wireframe(x, y, z, color='y', alpha=0.2)
    ax.plot3D(camino[0], camino[1], camino[2])
    ax.set_title("Camino aleatorio 3D")
    plt.show()

def main():
    # Estimación del número de pasos N de longitud l que debe dar un fotón hasta alcanzar el radio R usando Rrms

    # Se despeja N de la ecuación Rrms = np.sqrt(N)*rrms
    rrms = l
    Rrms = R
    NRrms = Rrms**2/rrms**2
    print('Estimación para N según la ecuación para Rrms: '+str(NRrms))

    # Se estima con simulación computacional
    k = 50
    NSimulacion = EstimarN(k)
    print('Estimación para N por simulación computacional: '+str(NSimulacion))

    # Se calcula la diferencia porcentual entre los dos valores encontrados para N
    diferencia = 100*(NSimulacion-NRrms)/NRrms
    print('Diferencia porcentual: '+str(diferencia)+' %')


    # Se grafica un camino aleatorio hasta R
    caminoFoton, N = CaminarHastaR()
    GraficarCamino(caminoFoton)


if __name__ == '__main__':
    main()