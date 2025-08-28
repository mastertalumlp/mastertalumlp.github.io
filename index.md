---
layout: talpage
title: "Formations TAL UMLP"
---



## Actualités


<div class="row">

{% assign sorted_actualites = site.actualites | sort: 'date' | reverse %}
{% for actu in sorted_actualites limit:3 %}

<div class="col-sm-4 mb-3 mb-sm-0">
<div class="card">
  <div class="card-header">
    {{ actu.header }}
    <span class="badge rounded-pill bg-info text-light float-right">Publié le {{ actu.date | date: "%d/%m/%Y" }} </span>
  </div>
  <div class="card-body">
    <h4 class="card-title">{{ actu.title }}</h4>
    <p class="card-text">{{ actu.content | markdownify }}</p>
  </div>
</div>

</div>

{% endfor %}


</div>




<a class="btn btn-outline-info btn-lg m-5" href="actualites.html">Voir toutes les actualités</a>




<div class="mb-5"></div>



## Formations en Traitement Automatique des Langues (TAL) de l’Université Marie et Louis Pasteur

  Le département Traitement Automatique des Langues (TAL) assure les formations en : 
  
<h4> 
  <a class="btn btn-outline-primary btn-lg mx-5" href="master.html">Master LLCER parcours TAL</a>
  <a class="btn btn-outline-primary btn-lg mx-5" href="licence.html">Licence parcours TAL</a>
</h4>


<div class="mb-5"></div>



## Calendrier universitaire 2025-2026

<a href="assets/fichiers/Calendrier2025-2026.pdf" target="_blank">
  <img src="assets/fichiers/cal2025-2026.png" alt="Calendrier universitaire 2025-2026" class="w-50">
</a>

