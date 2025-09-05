#!/usr/bin/env python
# coding: utf-8

# # Initialisation

# In[ ]:


import gspread
import pandas as pd
import copy, datetime, locale, codecs
import os, os.path, re, glob

locale.setlocale(locale.LC_ALL, "fr_FR.utf8")

joursSemaine = ["lundi", "mardi", "mercredi", "jeudi", "vendredi"]


# # Fonctions et classes

# In[ ]:


def lire_google_sheet(nom_fichier_cred, nom_feuille, nom_onglet="Sheet1"):
    """
    Lit les données d'un Google Sheets et retourne un DataFrame Pandas.
    
    Args:
        nom_fichier_cred (str): Chemin vers le fichier JSON des identifiants.
        nom_feuille (str): Nom du fichier Google Sheets.
        nom_onglet (str): Nom de l'onglet à lire (par défaut "Sheet1").
        
    Returns:
        pd.DataFrame: Données de l'onglet sous forme de DataFrame.
    """
    # Authentification avec le compte de service
    gc = gspread.service_account(filename=nom_fichier_cred)
    # Ouverture du fichier Google Sheets
    sh = gc.open(nom_feuille)
    # Sélection de l'onglet
    worksheet = sh.worksheet(nom_onglet)
    # Récupération des données sous forme de liste de dictionnaires
    data = worksheet.get_all_records()
    # Conversion en DataFrame Pandas
    df = pd.DataFrame(data)
    return df


# In[ ]:


# fonction qui reduit la liste des semaines, en prenant en compte la semaine actuelle
def reduireSemaines(sems, annees):
	# calculate remaining weeks, starting with current week
	now = datetime.datetime.now()
	# current week number :
	cwn = int(now.strftime("%V"))
	# current year
	cy = now.year
	semaines_copy = []
	if (cy > annees[0]) :
		if (cy == annees[1]) :
			for s in sems:
				if (s > 30) : continue
				if (s >= cwn) : 	semaines_copy.append(s)
	else :
		if (cy == annees[0]) :
			for s in sems:
				if (s < 30) :
					semaines_copy.append(s)
					continue
				if (s >= cwn) :
					semaines_copy.append(s)

	return semaines_copy


# In[ ]:


def findDateISO(semaine, annee, jour):
    # jour : int, de 1 (lundi) à 7 (dimanche), conforme à ISO
    # semaine : int, numéro de semaine ISO (1-53)
    return datetime.date.fromisocalendar(annee, semaine, joursSemaine.index(jour)+1 )


# In[ ]:


d = findDateISO(38, 2025, "lundi")
print(d)


# In[ ]:


# Une creneau / cours (qui correspond a plusieurs instances)
class Creneau:
	def __init__(self, semestre, jour, debut, fin, code, intitule, nature, intervenant, mutualise, salle, semaines_str, nb_sem_control):
		self.semestre = semestre
		self.jour = jour
		self.debut = debut
		self.fin = fin
		self.code = code
		self.intitule = intitule
		self.nature = nature
		self.intervenant = intervenant
		self.mutualise = mutualise
		self.salle = salle
		self.semaines = []
		self.nb_sem_control = nb_sem_control
    
		# traitement des semaines :
		for s in semaines_str.split(","):
			s = s.strip()
			if (s.count("-") > 0):
				start = s[0: s.find("-")].strip()
				end = s[s.find("-")+1:].strip()
				for t in range(int(start), int(end) + 1):
					self.semaines.append(t)
			else:
				if (s != "") :
					self.semaines.append(int(s))

        # check nb semanes :
		if len(self.semaines) != nb_sem_control :
		    self.nb_sem_control = "Error: " + str(nb_sem_control)

		# population des dates :
		self.populateDates()

	def __str__(self):
		code = ""
		if (self.code != ""):
			code = " (" + self.code +") "
		salle = ""
		if (self.salle != "") :
			salle += ", " + self.salle
		intvn = ""
		if (self.intervenant != ""):
			intvn = " - " + self.intervenant
		return str(self.semaines) + " (" + str(self.nb_sem_control) + ")" + ", " + self.jour + ", " + str(self.debut) + "h-" + str(self.fin) + "h, " + self.nature + " \"" + code + self.intitule + intvn + "\"" + salle

	def printDate(self, d):
		return d.strftime("%A %d %b") + " " + self.jour

	# trouver les dates et les enregistrer
	def populateDates(self):
		self.dates = []
		for s in self.semaines:
			# si ce n'est pas dans les semaines a traiter (definis au debut du programme), passer
			if not s in semaines_a_traiter :
				continue
			annee = annees[0]
			if (s < 30):  annee = annees[1]
                
			#fDayWeek = str(annee) + "-W" + str(s-1) + "-" + str(joursSemaine.index(self.jour)+1)
			#date = datetime.datetime.strptime(fDayWeek, "%Y-W%W-%w")
            #date = findDateISO(s, annee, self.jour)
			self.dates.append( findDateISO(s, annee, self.jour) )


# In[ ]:


# gestion d'une liste de creneaux

# extraire a partir d'un fichier Google sheets.
# La 1e feuille doit contenir les noms de colonne :
# Sem, Code, Intitule, Intervenant, Jour, Debut, Fin, Semaines, Salle
def extraireFromGS(v):

    # print(v.columns)
    lst = []

    for index, row in df.iterrows():
        # row est une Series contenant les valeurs de la ligne
        # print(f"Ligne {index} :")
        # print(row)
        # Pour accéder à une colonne spécifique : row['nom_colonne']
        # ['Sem', 'Code', 'CM maquette', 'TD maquette', 'Nat', 'Intitule',
        # 'Intervenant', 'Confirmé EDT', 'Confirmé enseignant', 'Jour', 'Debut',
        # 'Fin', 'Nb semaines', 'Semaines', 'Nb CM', 'Nb TD', 'Equipements',
        # 'Commentaire', 'Mutualise']

        semestre = row['Sem']
        if semestre not in semestres :
            continue
        
        intitule = row['Intitule'].strip()
        if not len(intitule) :
            continue # si cette celule est vide, alors il n'y a pas de creneau
        jour = row['Jour'].strip()
        if not jour in joursSemaine :
            continue
    
        debut = row["Debut"]
        fin = row["Fin"]
        if not debut or not fin :
            continue
    
        cr = Creneau(semestre, jour, debut, fin, row['Code'].strip(), intitule,
                     row['Nat'], row['Intervenant'].strip(), row["Mutualise"], 
                     str(row["Equipements"]).strip(), str(row["Semaines"]).strip(), row["Nb semaines"])
        lst.append(cr)

    return lst


# In[ ]:


class Semaine:
	def __init__(self, n, annee) :
		self.n = n # numero de la semaine
		self.annee = annee
		self.creneaux = [] # liste de creneaux
		self.date_debut_str = ""
		self.date_fin_str = ""

	# extraire les creneaux a partir d'une SousListeCreneaux
	def extraireDeListe(self, sousListeCr):
		for c in sousListeCr.lst:
			if (self.n not in c.semaines): continue
			self.creneaux.append(c)


# In[ ]:


class SousListeCreneaux:
	# Une sous-liste de creneaux definie par un filtre.
	# Un filtre se presente sous forme d'un dictionnaire avec valeurs possibles,
	# par ex. {"semestre": ["S7", "S8"], "titre": "Master 1 TAL"}, {"semestre": ["S9", "S10"], "titre": "Master 2 TAL"},
		# {"intervenant": "Iana ATANASSOVA", "titre": "I. Atanassova"}, {"salle": "salle Master TAL", "titre": "Occupation salle Master TAL"},

	def __init__(self, lstCr, filter, semaines):
		self.filter = filter
		self.lst = []
		self.conflits = dict()
		for c in lstCr :
			if (filter.__contains__("semestre") and filter["semestre"] != ""):
				if not c.semestre in filter["semestre"]: continue
			if (filter.__contains__("intervenant") and filter["intervenant"] != ""):
				if (c.intervenant != filter["intervenant"]): continue
			if (filter.__contains__("mutualise")):
				if (not filter["mutualise"].__contains__(c.mutualise)): continue
			if (filter.__contains__("salle")):
				if (filter["salle"] != c.salle): continue
			self.lst.append(c)

    	# trouve les conflits et les stoque dans self.conflits
    	# en tant que listes de creneaux dans un dictionnaire
		# if len(self.lst) == 0 :  return
		for s in semaines:
			for j in joursSemaine:
				crJour = dict()
				# verification des conflits entre 8h et 20h
				for h in range(8, 20):
					for c in self.lst:
						if (c.jour != j) : continue
						if (s not in c.semaines): continue
						if (h != c.debut) : continue
						for tmp in range(c.debut, c.fin):
									if (tmp in crJour):
										# conflit ici !
										crJour[tmp].append(c)
										self.conflits["Semaine " + str(s) + " " + str(j) + " " + str(c.debut) + "h"] = crJour[tmp]
									else:
										crJour[tmp] = [c]


# In[ ]:


def dateDebut(semaine, annee):
    # Lundi = 1 en norme ISO
    date_lundi = datetime.date.fromisocalendar(annee, semaine, 1)
    return date_lundi.strftime("%d/%m/%Y")

def dateFin(semaine, annee):
    # Vendredi = 5 en norme ISO
    date_vendredi = datetime.date.fromisocalendar(annee, semaine, 5)
    return date_vendredi.strftime("%d/%m/%Y")


# In[ ]:


# extrait l'EDT en HTML !
# fsname est le nom du fichier obtenu a partir du filtre
# distinction_param est "code" pour avoir des couleurs differentes selon les UE
# ou bien "semestre" pour avoir des couleurs selon les semestres (par ex. S7 ou S9)
def extractEDTenHTML(sousListe, html_rel_path, fname, titre, semaines, annees, distinction_param="code"):

    # if len(sousListe.lst) == 0 : return

    # dictionnaire pour regrouper les semaines identiques
    sem_dict = dict()

    # dictionnaire pour les classes (couleurs bootstrap) et UE
    coldict = {"1": "primary",
                "2": "danger", 
                "3": "warning", 
                "4": "success", 
                "5": "info"}

    for s in semaines:

        # objet table qui contient tous les cellules pour la table html
        # Structure : clés - heures de début, valeurs - listes 5 elems. pour chaque
        # jour de la semaine
        # Pour chaque créneau, nous avons un dictionnaire avec clés : intitule, intervenant, salle, code, 
        # type (pour le choix de la couleur), nbcells, debut, fin
        # Si intitule est "--||--", c'est que c'est le creneau de plus haut qui continue.
        # table = { 9 -> [ { "intitule" -> "...", .... }, {}, {}, {}, {} ]	}							  
        table = dict()

        for c in sousListe.lst:
            if (s not in c.semaines): continue

            jourIndex = joursSemaine.index(c.jour)
            debut = int(c.debut)
            fin = int(c.fin)
            nbcells = fin - debut

            # calcul du type (pour le choix de la couleur)
            ctype = "5"
            if (distinction_param == "code") :
                if c.code.startswith("Y4GE") :
                    ctype = c.code[6]
                    if ctype == "U" :
                        ctype = c.code[7]
            if (distinction_param == "semestre") :
                if  (c.semestre in [7, 8]) :
                    ctype = 1
                elif (c.semestre in [9, 10]) :
                    ctype = 2

            # creation d'une ligne vide si besoin
            if not debut in table:
                table[debut] = []
                for j in joursSemaine :
                    table[debut].append(dict())

            table[debut][jourIndex]["intervenant"] = c.intervenant
            table[debut][jourIndex]["intitule"] = c.intitule
            table[debut][jourIndex]["salle"] = c.salle
            table[debut][jourIndex]["code"] = c.code
            table[debut][jourIndex]["type"] = ctype
            table[debut][jourIndex]["nbcells"] = nbcells
            table[debut][jourIndex]["debut"] = c.debut
            table[debut][jourIndex]["fin"] = c.fin

            for i in range(nbcells-1):
                ind = debut + i + 1

                # creation d'une ligne vide si besoin
                if not ind in table:
                    table[ind] = []
                    for j in joursSemaine :
                        table[ind].append(dict())

                table[ind][jourIndex]["intitule"] = "--||--"

        html_tab = '<table class="table table-sm table-bordered" style="width:100%; max-width:1200px; min-width:700px;">'
        html_tab += '<tr class="table-active text-center"><th style="width:5%"></th><th style="width:19%">'
        js = '</th> <th style="width:19%">'.join(joursSemaine)
        html_tab += js + "</th></tr>\n"

        k = table.keys()
        if not len(k) :
            continue
        start = min(k)
        end = max(k)

        for h in range(start, end+1):
            ligne = '<tr><td class="table-active text-center" style="vertical-align:middle;height:70px;"><small>' 
            ligne += str(h) + "h</small></td>"

            if not h in table :
                # heure vide pour tous les jours 
                html_tab += ligne
                for j in joursSemaine:
                    html_tab += "<td></td>"
                html_tab += "</tr>"
                continue

            for i in table[h]:
                if not "intitule" in i :
                    ligne += "<td></td>"
                    continue

                if i["intitule"] == "--||--" :
                    continue

                rspan = ""
                if i["nbcells"] > 1:
                    rspan = ' rowspan="' + str(i["nbcells"])+'"'

                colclass = ' class="table-secondary"'
                if i["type"] in coldict:
                    colclass = ' class="table-' + coldict[ i["type"] ] + '"'

                sallebadgecol = 'info'
                if "!" in i["salle"] :
                    sallebadgecol = 'danger'

                ligne += "<td" + rspan + colclass + ' style="border-radius:16px;"><p class="text-primary mb-0"><small><strong>' + str(i["debut"]) + "h-" + str(i["fin"]) + 'h</strong>'
                ligne += ' <span class="badge badge-pill badge-secondary float-right">' + i["code"] + '</span></small></p>'
                ligne += '<h6 class="clearfix"><small>' + i["intitule"] + '</small></h6>'
                ligne += '<p class="text-primary mb-0 pb-0 clearfix"><small>' + i["intervenant"]
                ligne += '<span class="badge badge-' + sallebadgecol + ' float-right float-bottom m-1">' 
                ligne += i["salle"] + "</span></small></p></td>"

            ligne += "</tr>\n"
            html_tab += ligne

        html_tab += "</table>\n"

        sem_dict[s] = html_tab

    # preparation du fichier html
    htmlout = codecs.open(os.path.join(html_rel_path, fname), "w", "utf-8")
    # write header
    htmlout.write("---\nlayout: talpage\ntitle: 'Emploi de temps - " +  titre + "'\n---\n\n")

    # afficher les conflits s'il y en a : 
    htmlconf = ""
    if (len(sousListe.conflits)) :
        htmlconf = '<div class="col-3 float-right"><div class="card text-danger border-danger"> <div class="card-header fw-bold text-white bg-danger">Conflits de créneaux</div>'
        htmlconf += '<div class="card-body">'
        for k in sousListe.conflits.keys() :
            htmlconf += '<p class="fw-bold">Semaine ' + k + " :</p>"
            for c in sousListe.conflits[k]:
                htmlconf += '<p>' + str(c) + '</p>'
        htmlconf += '</div></div></div>\n\n'

    htmlout.write('# Emploi de temps : ' + titre + "\n\n")
    now = datetime.datetime.now()
    htmlout.write('<p class="text-secondary">Dernière mise à jour : ' + now.strftime("%d/%m/%Y") + "</p>\n")

    # calcul de la liste de semaines pour lesquelles nous avons un changement:
    # liste avec valeurs : 1 si modification, 0 si pas de modification, -1 si la semaine n'existe pas
    sem_change = []
    prev = ""
    for s in semaines:
        if (s in sem_dict) :
            if (sem_dict[s] == prev) :
                sem_change.append(0)
            else :
                sem_change.append(1)
                prev = sem_dict[s]
        else :
            sem_change.append(-1)
            prev = ""

    # print(sem_change)
    for i in range(len(semaines)):
        # print("semaine " + str(semaines[i]))
        if (sem_change[i] != 1) :
            continue
        # generation du document ici:

        # calcul des semaines identiques
        s_debut = semaines[i]
        if (sem_dict[s_debut] == "") :
            continue
        s_fin = semaines[-1]
        for j in range(i+1, len(semaines)):
            if (sem_change[j] != 0) :
                s_fin = semaines[j-1]
                break
    
        annee = annees[0]
        if (s_debut < 30):  annee = annees[1]
        # lundi :
        dateL = dateDebut(s_debut, annee)
        # vendredi
        dateV = dateFin(s_fin, annee)

        titreSem = ""
        if (s_debut == s_fin) :
            titreSem = "Semaine " + str(s_debut) + " : " + titre + " (" + dateL + "-" +  dateV + ")"
        else :
            titreSem = "Semaines " + str(s_debut) + "-" + str(s_fin) + " : " + titre  + " (" + dateL + "-" +  dateV + ")"

        # add to html :
        htmlout.write('#### ' + titreSem + "\n\n" + sem_dict[s_debut] + "\n\n")
        htmlout.write(htmlconf)
        htmlconf = ""

    # fermeture du fichier html
    htmlout.close()


# # Git push commandes

# In[ ]:


import subprocess

def git_push(repo_path=".", commit_message="Mise à jour automatique site web"):
    try:
        # Ajouter tous les fichiers modifiés dans le repo spécifié
        subprocess.run(["git", "-C", repo_path, "add", "."], check=True)
        
        # Faire un commit avec le message dans le repo spécifié
        subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message], check=True)
        
        # Pousser vers la branche distante dans le repo spécifié
        subprocess.run(["git", "-C", repo_path, "push"], check=True)
        
        print(f"Mise à jour Git effectuée avec succès dans {repo_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la mise à jour Git dans {repo_path}: {e}")


# # Programme principal

# In[ ]:


# calendrier de l'annee
semaines = [37, 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 	2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]
annees = [2025, 2026]
semestres = [3, 4, 5, 6, 7, 8, 9, 10]

# filtres pour verifier la coherence de l'EDT et generer les tableaux separees
filters = [
           {"semestre": [7, 8], "titre": "M1 TAL"},
           {"semestre": [9, 10], "titre": "M2 TAL"},
           {"intervenant": "Iana ATANASSOVA", "titre": "Iana"},
           {"intervenant": "Aurélie NOMBLOT", "titre": "Aurelie"},
           {"intervenant": "Panggih Kusuma NINGRUM", "titre": "Ning"},
            {"intervenant": "Pierre Mercuriali", "titre": "Pierre"},
            {"intervenant": "Mounir Zrigui", "titre": "Mounir"},
           {"salle": "Salle Master TAL", "titre": "Salle Master TAL"}
           ]

outputDir = "/home/iana/CLOUDS/travail/10-Espace-de-travail-perso/mastertalumlp.github.io/"

# Lecture du Google Sheet : 
df = lire_google_sheet("edt-master-tal-27f3c1946ece.json", "Donnees-Master-TAL", "EDT-2025-2026")
# print(df.head())

# print(df.columns)
# print(df)


# In[ ]:


semaines_a_traiter = reduireSemaines(semaines, annees)
print("Semaines à traiter :" + str(semaines_a_traiter))


# In[ ]:


creneaux = extraireFromGS(df)
for c in creneaux :
    # print(c)
    if type(c.nb_sem_control)==str :
        print("ERREUR nb semaines")
        print(c)


# In[ ]:


# extraction des filtres et AFFICHAGE DES CONFLITS :
for f in filters:
    print(f)
    sl = SousListeCreneaux(creneaux, f, semaines_a_traiter)
    for k in sl.conflits :
        print(k)
        for c in sl.conflits[k]:
            print(c)
    
    # export en HTML
    fname = "edt-"+ f["titre"].replace(" ", "") + ".md"
    d_param = "code"
    if ("salle" in f) :
        d_param = "semestre"
    extractEDTenHTML(sl, outputDir, fname, f["titre"], semaines_a_traiter, annees, d_param)
    print(fname)
    print("---")

print("Done")


# In[ ]:


# Sync with github
git_push(outputDir)

