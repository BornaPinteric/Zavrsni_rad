import intenzitet as i
import numpy as np

# udaljenost od 1m do 2m i promjer od od 1mm (postavke realnog eksperimenta)

def pukotina(oblik):

    oblik = ("{}".format(oblik)).lower()

    if oblik in ["krug", "1"]:
        return i.create_circle(n, m, polumjer)
    
    elif oblik in ["crta", "2"]:
        return i.create_line(n, m, debljina)
    
    elif oblik in ["krugovi", "3"]:
        return i.create_circles(n, m, sredista, polumjeri)
    
    else:
        matrix = [[False,True,False,True,False]]
        matrix += [[False,True,False,True,False]]
        matrix += [[False]*5]
        matrix += [[True]+[False]*3+[True]]
        matrix += [[False]+[True]*3+[False]]
        return np.array(matrix)

n = 30
m = 30
udaljenost = 1 #[m]
sirina = 0.001 #[m]
valna_duljina = 450 #[nm]
povecavanje = 5
ogranicenja = [1, 0.1, 0.05, 0.01]

#KRUG (1)
polumjer = 15

#CRTA (2)
debljina = 2

#KRUGOVI (3)
sredista = [(10,5),(10,16)]
polumjeri = [3,4]

papir = pukotina(1) #oblik ili broj oblika

zaslon = i.intensity_matrix(papir, udaljenost, sirina, valna_duljina, povecavanje)
    
boja = i.colour(valna_duljina)
    
i.plot_results(papir, zaslon, ogranicenja, boja)