---
layout: talpage
title: "Formations TAL UMLP"
---

<div class="banniere-des">
  <div class="banniere-logo gauche">
    <img src="/assets/images/logo_deptm_tal.png" alt="Département TAL - UFR SLHS - UMLP" style="max-width:130px;">
  </div>

  <div class="banniere-logo gauche">
    <img src="/assets/images/UMLP-CRIT.png" alt="CRIT - UMLP">
  </div>

  <div class="banniere-texte" href="https://mastertalumlp.github.io/formation-des.html">
    <div class="banniere-surtitre">Nouvelle formation courte</div>
    <div class="banniere-titre">Data Excellence Science</div>
    <div class="banniere-soustitre">
      Une collaboration entre <strong>Global Data Excellence</strong> et le
      <strong>Département Traitement Automatique des Langues</strong> de l’UMLP
    </div>
  </div>

  <div class="banniere-logo droite">
    <a href="https://globaldataexcellence.com/" target="_blank"><img src="/assets/fichiers/DES/GDE.png" alt="Global Data Excellence"></a>
  </div>
</div>




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

<a href="/assets/fichiers/Calendrier2025-2026.pdf" target="_blank">
  <img src="/assets/fichiers/cal2025-2026.png" alt="Calendrier universitaire 2025-2026" class="w-50">
</a>

