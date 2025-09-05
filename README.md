# Page web du master LLCER parcours TAL de l'Université Marie et Louis Pasteur, Besançon, France

2025-2026

###  Ajouter des actualités

1. Créer un fichier AAAA-MM-JJ-blabla.md dans le repertoire _actualites.
2. Ajouter l'entête, modifier la date de publication :

---
title: "Titre ici"
date: 2025-08-28
header: "Rubrique / titre court"
---

3. Ajouter le texte dessous, en format md (pour référence https://www.markdownguide.org/cheat-sheet/)

Pour ajouter une image, utiliser par exemple :

<img src="actualites/reunion-rentree.jpg" class="img w-50" alt="reunion">

où le fichier image est placé dans le même repertoire _actualites.



### Modificaitons de l'EDT

1. Prévenir les étudiants et éventuellement d'autres personnes concernées par mail.
2. Modifier le Google Sheet avec l'EDT : https://docs.google.com/spreadsheets/d/16H9HBquvyNAw6L8xw9PFsrOYwJ8_LUaPUO7i0R6b0ns/edit?usp=sharing 
3. Lancer le code python qui se trouve dans le repertoire python.

python3 edt2jekyll.py

Ce code essaye de :
- lire le google sheet 
- produire les nouvelles pages web EDT
- sychroniser le dépôt git. Vérifier que cette dernière étape a bien marché.

4. Les éventuels conflits de créneaux s'affichent en rouge à droite sur les pages web EDT. Vérifiez.



