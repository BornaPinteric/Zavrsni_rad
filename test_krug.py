import intenzitet as i

def nacrtaj_krug(dimenzije, udaljenost, promjer, valna_duljina, povecavanje=1, ogranicenje=1, visok_kontrast=False):
    '''dimenzije (n,m,r): matrica nxm, krug radijusa r\n
    udaljenost [m]: od pukotine do zaslona\n
    promjer [m]: promjer kruzne pukotine\n
    valna_duljina [nm]: lambda svjetlosti\n
    povecavanje k (prirodan broj): zastor k puta veci od pukotine\n
    ogranicenje M (0<M<1): sve vrijednosti veće od M*max =0\n
    visok_kontrast (bool): vrijedost True primijeni posebnu boju'''

    n,m,r = dimenzije
    papir = i.create_circle(n, m, r)

    zaslon = i.intensity_matrix(papir, udaljenost, promjer/2/r*m, valna_duljina, povecavanje, ogranicenje)
    
    boja = i.colour(valna_duljina)
    if visok_kontrast:
        boja = i.colour()
    
    i.plot_results(papir, zaslon, boja)

# udaljenost od 1m do 2m i promjer od od 1mm (postavke realnog eksperimenta)
# dimenzije (20,20,10) s povecanjem 3 (kratak run time i dovoljno preciznosti)
# ogranicenje 1 (citava slika) / od 0.1 do 0.01 (promatranje maksimuma visih redova)
# valna duljina od 380nm do 740nm

# nefizikalni uzorak za vece iznose promjera (manjak preciznosti pa razlika u fazi izmedu susjednih tocaka pre velika?)

nacrtaj_krug((20,20,10), 1.5, 0.001, 550, 3, 1)