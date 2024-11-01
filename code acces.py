import os

# variables globales
global nb_blocs, taille_bloc, bloc_rep_courant, pwd
nb_blocs = 32
taille_bloc = 128
bloc_rep_courant = 0
pwd = "/"


# couleurs
class couleur:
    FIC = '\033[92m' # GREEN
    REP = '\033[93m' # YELLOW
    ERR = '\033[94m' # BLUE
    RESET = '\033[0m' # RESET COLOR


# commande ls
def fat8_ls():

    # on parcourt le répertoire courant : bloc_rep_courant
    global bloc_rep_courant

    fat = open ("fat8","rb+")
    for ligne in range (taille_bloc // 16):
        fat.seek ((2 + bloc_rep_courant) * taille_bloc + ligne * 16)

        debut = fat.read (1)

        # s'il s'agit d'un un fichier
        if debut == b'\x01':

            nom = fat.read (12)
            # on enlève les caractères nuls à la fin du nom
            nom_x = nom.decode ("utf-8")
            nom_x = nom_x[: nom.find (0)]
            bloc = int.from_bytes (fat.read (1), "big")
            taille = int.from_bytes (fat.read (2), "big")

            print (couleur.FIC + nom_x + " (bloc = " + str (bloc) + ", taille = " + str (taille) + " octets)")

        # s'il s'agit d'un dossier
        if debut == b'\x02':

            nom = fat.read(12)
            # on enlève les caractères nuls à la fin du nom
            nom_x = nom.decode("utf-8")
            nom_x = nom_x[: nom.find (0)]
            bloc = int.from_bytes (fat.read (1), "big")
            taille = int.from_bytes (fat.read (2), "big")

            print (couleur.REP + nom_x + " (bloc = " + str (bloc) + ", taille = " + str (taille) + " octets)")

    print (couleur.RESET, end = "")
    fat.close ()
    

# commande cd
def fat8_cd (rep):

    # on parcourt le répertoire courant : bloc_rep_courant
    global bloc_rep_courant

    # on se place à l'endroit courant
    fat = open ("fat8", "rb+")
    for ligne in range (taille_bloc // 16):
        fat.seek ((bloc_rep_courant + 2) * taille_bloc + ligne * 16)

        type_ele = fat.read (1)
        # s'il s'agit d'un dossier
        if type_ele == b'\x02':

            octets = fat.read (12)
            # on enlève les caractères nuls à la fin du nom
            nom = str (octets.decode ("utf-8"))
            print("|" + nom + "|" + rep + "|")

            if nom == rep:
                # on cherche le bloc du nouveau dossier
                bloc = int.from_bytes (fat.read (1), "big")
                bloc_rep_courant = bloc

                # on termine la fonction
                fat.close ()
                return

    # on affiche l'erreur
    print (couleur.ERR + "Le dossier " + rep + " n'existe pas." + couleur.RESET)
    fat.close ()


# commande cat
def fat8_cat (fic):

    # on parcourt le répertoire courant : bloc_rep_courant
    global bloc_rep_courant

    # on se place à l'endroit courant
    fat = open ("fat8", "rb+")
    for ligne in range (taille_bloc // 16):
        fat.seek ((bloc_rep_courant + 2) * taille_bloc + ligne * 16)

        type_ele = fat.read (1)
        # s'il s'agit d'un fichier
        if type_ele == b'\x01':

            octets = fat.read (12)
            # on enlève les caractères nuls à la fin du nom
            nom = str (octets.decode ("utf-8"))
            print("|" + nom + "|" + fic + "|")

            if nom == fic:
                # on cherche le bloc du nouveau dossier
                bloc = int.from_bytes (fat.read (1), "big")

                while True:
                    fat.seek ((bloc + 2) * taille_bloc)
                    octets = fat.read (taille_bloc)
                    # on affiche le contenu du fichier
                    print (str (octets.decode ("utf-8")), end = "")

                    # on regarde le prochain bloc
                    fat.seek (taille_bloc)
                    _ = fat.read (bloc)
                    bloc = int.from_bytes (fat.read (1), "big")

                    if bloc == 255:
                        break
                
                # on termine la fonction
                fat.close ()
                return

    # on affiche l'erreur
    print (couleur.ERR + "Le fichier " + fic + " n'existe pas." + couleur.RESET)
    fat.close ()


# commande mkdir
def mkdir (rep):
    pass


# programme principal champosh 
# boucle infinie : invite champosh

while True:

    commande = input ("champosh # ")
    tab_commandes = commande.split ()


    if commande == 'pwd':
        print (pwd)
        continue


    if (tab_commandes[0] == 'ls'):

        if len (tab_commandes) != 1:
            print ("Il ne faut pas de paramètre à la commande ls")
            continue

        fat8_ls ()
        continue


    if tab_commandes[0] == 'cd':

        if len (tab_commandes) != 2:
            print ("Il faut un unique paramètre à la commande cd")
            continue

        #on récupère le nom en paramètre
        rep = tab_commandes[1]
        fat8_cd (rep)
        continue


    if tab_commandes[0] == 'cat':

        if len (tab_commandes) != 2:
            print ("Il faut un unique paramètre à la commande cat")
            continue

        # on récupère le nom en paramètre
        fic = tab_commandes[1]
        fat8_cat (fic)
        continue


    print (commande + " : commande inconnue")
