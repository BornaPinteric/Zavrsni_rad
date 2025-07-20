import numpy as np
import matplotlib.pyplot as plt

def intensity_matrix(boolean_matrix, distance, width, wavelength, upscale, approx=True):
    '''distance[m]\nwidth[m]\nwavelength[nm]'''

    k = 2*np.pi/wavelength*10**9*width
    z = distance / width

    n,m = boolean_matrix.shape
    matrix = np.zeros((n*upscale, m*upscale))
    mid=(n*upscale - 1) / 2

    progress = (n*upscale) // 4

    normalizer = 0

    for i_main in range(n*upscale):

        if (i_main+1) % progress == 0:
            print("{}%".format(25 * (i_main+1) / progress))

        for j_main in range(m*upscale):

            I_sin = 0
            I_cos = 0

            x_main = i_main - mid
            y_main = j_main - mid
            xyz_main = np.sqrt(x_main**2 + y_main**2 + z**2)

            for i_bool in range(n):
                for j_bool in range(m):

                    if boolean_matrix[i_bool][j_bool]:

                        x_bool = i_bool + (upscale-1) / 2 * n - mid
                        y_bool = j_bool + (upscale-1) / 2 * m - mid
                        xyz_bool = np.sqrt((x_bool-x_main)**2 + (y_bool-y_main)**2 + z**2)

                        if approx:
                            dL = x_bool*x_main/xyz_main + y_bool*y_main/xyz_main
                        else:
                            dL = xyz_bool - xyz_main

                        I_sin += np.sin(k*dL)
                        I_cos += np.cos(k*dL)
            
            matrix[i_main][j_main] = I_sin**2 + I_cos**2
            normalizer = np.max(matrix)

    return np.divide(matrix, normalizer), __colour(wavelength=wavelength)

def intensity_matrix_list(boolean_matrix, distance, width, wavelength_list, upscale, approx=True):

    generated_list = []

    for wavelength in wavelength_list:

        generated_list.append(intensity_matrix(boolean_matrix, distance, width, wavelength, upscale, approx=approx))
    
    return generated_list

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

def create_circles(n, m, r):

    matrix = np.zeros((n,m), dtype=bool)
    
    center_i = (n-1)/2
    center_j = [r[0], m-1-r[1]]

    for i in range(n):
        for j in range(m):

            for k in range(2):

                if np.sqrt((i-center_i)**2+(j-center_j[k])**2) <= r[k]:

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

def __extremes(A):

    minima = []
    maxima = []

    for i in range(len(A)//2-1, len(A)-1):
        
        if A[i] <= A[i-1] and A[i] <= A[i+1]:
            minima.append(i)

        if A[i] >= A[i-1] and A[i] >= A[i+1]:
            maxima.append(i)
    
    return __reduced(minima), __reduced(maxima)

def __reduced(A):

    B = [A[0]]

    for i in range(1, len(A)):

        if A[i] != A[i-1]+1:
            B.append(A[i])

    return B

def compare_to_theory(intensity_matrix, distance, width, diameter, wavelength):

    middle = intensity_matrix[(len(intensity_matrix)-1)//2]

    rel_int_T = [1, 0.0175, 0.0042, 0.0016, 0.00078]

    dy = lambda m: round(distance * m * wavelength*10**(-7) / diameter, 5)
    dy_min_T = [dy(m) for m in [1.22, 2.233, 3.238, 4.241]]
    dy_max_T = [dy(m) for m in [1.635, 2.679, 3.699, 4.710]]

    i_min, i_max = __extremes(middle)

    rel_int_N = [round(middle[i], 6) for i in i_max]
    
    dy_min_N = [round(100 * width * (i_min[j] - i_max[0]), 5) for j in range(0, len(i_min))]
    dy_max_N = [round(100 * width * (i_max[j] - i_max[0]), 5) for j in range(1, len(i_max))]

    print("-Relative intensity-")
    print("T: " + "%-9g" * 5 % tuple(rel_int_T))
    print("N: " + "%-9g" * len(i_max) % tuple(rel_int_N))
    print("-Minima displacement [cm]-")
    print("T: " + "%-9g" * 4 % tuple(dy_min_T))
    print("N: " + "%-9g" * (len(i_min)) % tuple(dy_min_N))
    print("-Maxima displacement [cm]-")
    print("T: " + "%-9g" * 4 % tuple(dy_max_T))
    print("N: " + "%-9g" * (len(i_max)-1) % tuple(dy_max_N))

def __colour(wavelength=0):
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

def plot_results(boolean_matrix, intensity_matrix, intensity_cmap, limits):

    plt.imshow(boolean_matrix, cmap="gray")
    plt.title("Pukotina")
    plt.xticks([])
    plt.yticks([])
    plt.show()

    for lim in limits:

        if lim==0:
            plt.imshow(intensity_matrix, cmap=intensity_cmap)
            plt.title("Difrakcijski uzorak")
            plt.xticks([])
            plt.yticks([])
            plt.show()

        else:
            plt.imshow(__scaled_matrix(intensity_matrix, lim), cmap=intensity_cmap)
            plt.title("Difrakcijski uzorak (relativni intenzitet<={})".format(lim))
            plt.xticks([])
            plt.yticks([])
            plt.show()

def overlay_results(boolean_matrix, generated_matrix_list, limits):
    
    plt.imshow(boolean_matrix, cmap="gray")
    plt.title("Pukotina")
    plt.xticks([])
    plt.yticks([])
    plt.show()

    for lim in limits:

        if lim==0:

            a = 1
            for intensity_matrix, intensity_cmap in generated_matrix_list:

                plt.imshow(intensity_matrix, cmap=intensity_cmap, alpha=a)
                a -= 0.4

            plt.title("Difrakcijski uzorak")
            plt.xticks([])
            plt.yticks([])
            plt.show()

        else:
            
            a = 1
            for intensity_matrix, intensity_cmap in generated_matrix_list:

                plt.imshow(__scaled_matrix(intensity_matrix, lim), cmap=intensity_cmap, alpha=a)
                a -= 0.4
                
            plt.title("Difrakcijski uzorak (relativni intenzitet<={})".format(lim))
            plt.xticks([])
            plt.yticks([])
            plt.show()