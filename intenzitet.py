import numpy as np
import matplotlib.pyplot as plt

def intensity_matrix(boolean_matrix, distance, width, wavelength, upscale):
    '''distance[m]\nwidth[m]\nwavelength[nm]'''

    delta = lambda dL: dL*2*np.pi/wavelength*10**9

    n,m = boolean_matrix.shape
    matrix = np.zeros((n*upscale,m*upscale))

    dx = width/m
    z = distance

    for i_main in range(n*upscale):
        for j_main in range(m*upscale):

            sum_cos = 0
            sum_sin = 0

            for i_bool in range(n):
                for j_bool in range(m):

                    if boolean_matrix[i_bool][j_bool]:

                        x = abs(i_bool+(upscale-1)/2*n-i_main)*dx
                        y = abs(j_bool+(upscale-1)/2*m-j_main)*dx
                        xyz = np.sqrt(x**2+y**2+z**2)
                        d = delta(xyz-z)
                        sum_cos += np.cos(d)/xyz
                        sum_sin += np.sin(d)/xyz
            
            matrix[i_main][j_main] = sum_cos**2+sum_sin**2
            normalizer = np.max(matrix)

    return np.divide(matrix, normalizer)

def __scaled_matrix(matrix, limit):
    
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):

            if matrix[i][j] > limit:
                matrix[i][j] = 0
    
    return matrix

def create_circle(n, m, r):

    matrix = np.zeros((n,m), dtype=bool)

    center_i = (n-1)/2
    center_j = (m-1)/2
    
    for i in range(n):
        for j in range(m):

            if np.sqrt((i-center_i)**2+(j-center_j)**2) <= r:

                matrix[i][j] = True

    return matrix

def create_circles(n, m, c, r):

    matrix = np.zeros((n,m), dtype=bool)
    
    for i in range(n):
        for j in range(m):

            for k, center in enumerate(c):

                if np.sqrt((i-center[0])**2+(j-center[1])**2) <= r[k]:

                    matrix[i][j] = True

    return matrix

def create_line(n, m, k):

    matrix = np.zeros((n,m), dtype=bool)

    center_i = (n-1)//2
    
    for i in range(n):
        
        if abs(i-center_i-0.25) < k*0.5:

            for j in range(m):

                matrix[i][j] = True

    return matrix

def colour(wavelength=0):
    '''wavelength[nm]: omit for best visibility'''

    cmap="viridis"
    if 380<=wavelength<=440:
        cmap="Purples"
    elif 440<wavelength<=520:
        cmap="Blues"
    elif 520<wavelength<=590:
        cmap="Greens"
    elif 590<wavelength<=630:
        cmap="Oranges"
    elif 630<wavelength<=740:
        cmap="Reds"
    return cmap

def plot_results(boolean_matrix, intensity_matrix, limits, intensity_cmap):

    plt.imshow(boolean_matrix, cmap="gray")
    plt.title("Pukotina")
    plt.xticks([])
    plt.yticks([])
    plt.show()

    for lim in limits:

        plt.imshow(__scaled_matrix(intensity_matrix, lim), cmap=intensity_cmap)
        plt.title("Difrakcijski uzorak (relativni intenzitet<={})".format(lim))
        plt.xticks([])
        plt.yticks([])
        plt.show()