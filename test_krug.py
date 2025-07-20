import intenzitet as i

#POSTAVKA REALNOG EKSPERIMENTA

udaljenost = 1 #[m]
sirina = 0.001 #[m]

ogranicenja = [0, 0.07, 0.01, 0.004]

def jedan_uzorak():

    #PARAMETRI
    n = 20
    m = 20
    povecavanje = 4

    valna_duljina = 400 #[nm]

    #GENERACIJA PUKOTINE
    polumjer = n//2
    pukotina = i.create_circle(n, m, polumjer)

    #GENERACIJA UZORKA
    difrakcijski_uzorak = i.intensity_matrix(pukotina, udaljenost, sirina/n, valna_duljina, povecavanje, approx=True)

    #USPOREDBA I PRIKAZ
    i.compare_to_theory(difrakcijski_uzorak[0], udaljenost, sirina/n, sirina*2*polumjer/n, valna_duljina)
    i.plot_results(pukotina, *difrakcijski_uzorak, ogranicenja)

def tri_uzorka():

    #PARAMETRI
    n = 20
    m = 20
    povecavanje = 3

    valne_duljine_lista = [380, 560, 740] #[nm]

    #GENERACIJA PUKOTINE
    polumjer = n//2
    pukotina = i.create_circle(n, m, polumjer)

    #GENERACIJA UZORAKA
    generirani_uzorci = i.intensity_matrix_list(pukotina, udaljenost, sirina/n, valne_duljine_lista, povecavanje)

    #PRIKAZ
    i.overlay_results(pukotina, generirani_uzorci, ogranicenja)

#jedan_uzorak()
tri_uzorka()