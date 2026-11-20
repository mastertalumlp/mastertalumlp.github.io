# Site web du Département TAL - Université Marie et Louis Pasteur

Site des formations en Traitement Automatique des Langues (TAL) de l'Université Marie et Louis Pasteur (UMLP), Besançon : Master LLCER parcours TAL, Licence parcours TAL, UE libres, formation courte Data Excellence Science (DES).

En ligne : https://mastertalumlp.github.io (Jekyll, hébergé sur GitHub Pages ; publication automatique à chaque `git push`).

## Organisation des fichiers

| Fichier / dossier | Contenu |
|---|---|
| `index.md` | Accueil (3 dernières actualités, liens Master / Licence, bannière DES, calendrier universitaire) |
| `master.md`, `competences.md`, `memoire.md`, `stage.md`, `regles-ia.md`, `edt.md` | Pages du Master |
| `licence.md`, `uels.md` | Pages de la Licence et des UE libres |
| `formation-des.md` | Formation courte Data Excellence Science |
| `equipe.md`, `ressources.md`, `actualites.md` | Équipe, documents, liste des actualités |
| `_actualites/` | Actualités (un fichier par actualité) et leurs images |
| `_layouts/talpage.html` | Gabarit commun : bannière, **menu de navigation**, pied de page |
| `assets/fichiers/` | Documents téléchargeables (PDF, DOCX…) |
| `assets/images/` | Images et photos |
| `py/` | Script historique de génération des emplois du temps (non publié) |

## Ajouter une actualité

1. Créer `_actualites/AAAA-MM-JJ-sujet.md` (le nom commence par la date).
2. En-tête :

```
---
title: "Titre de l'actualité"
date: 2026-11-21
header: "Rubrique / titre court"
---
```

3. Écrire le texte en Markdown (https://www.markdownguide.org/cheat-sheet/).
4. Image : placer le fichier dans `_actualites/` et l'insérer avec un chemin **absolu** :

```
<img src="/actualites/mon-image.jpg" class="img w-50" alt="description">
```

Les trois actualités les plus récentes s'affichent sur l'accueil.

## Mettre à jour les listes de mémoires et de stages

Les sujets récents figurent dans `memoire.md` et `stage.md`, au format :
`- Titre (année de soutenance, Nom I.) - organisme d'accueil (stages)`.
La base Grist du Master (table « Mémoires et stages ») sert de référence.

## Emplois du temps

Les emplois du temps sont publiés sur ADE (ENT de l'université) ; la page `edt.md` y renvoie.
Le script `py/edt2jekyll_v2_2025.py` (génération de pages EDT à partir d'un Google Sheet) n'est plus utilisé pour le site.

## Prévisualiser et publier

```bash
bundle exec jekyll serve     # http://localhost:4000
git add -A && git commit -m "..." && git push
```
