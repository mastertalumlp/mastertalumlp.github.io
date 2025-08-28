---
layout: talpage
title: "Actualités"
---

# Toutes les actualités

<div class="row">


{% assign sorted_actualites = site.actualites | sort: 'date' | reverse %}
{% for actu in sorted_actualites %}

<div class="col-sm-4 mb-3 mb-sm-0">
<div class="card">
  <div class="card-header">
    {{ actu.header }} <span class="badge rounded-pill bg-info text-light float-right">Publié le {{ actu.date | date: "%d/%m/%Y" }} </span>
  </div>
  <div class="card-body">
    <h4 class="card-title">{{ actu.title }}</h4>
    <p class="card-text">{{ actu.content | markdownify }}</p>
  </div>
</div>

</div>

{% endfor %}


</div>



