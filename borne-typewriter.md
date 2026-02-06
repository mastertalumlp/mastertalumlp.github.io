---
layout: talpage-borne
title: "Borne d'arcade TAL - Le singe"
---

## Le singe qui tape à la machine


Auteur : Pierre Mercuriali

<div class="explication">

    <img src="/assets/images/singe.png" class="rounded m-3 w-50" style="float: right;"/>

    <p><b>Réveillez le singe tapeur !</b></p>

    <p>Ce singe déluré reproduit les distributions de lettres du français ou de l'anglais, comme dans les textes réels - ou au hasard pour le fun. Cliquez pour voir la magie des fréquences linguistiques en action !</p>

    <p><b>Ultra-simple à jouer :</b> Choisissez le nombre de lettres (1 à 32), la distribution (uniforme, français ou anglais), puis cliquez sur "Taper..." (plein de fois). Résultat instantané dans le terminal : des mots absurdes mais distributionnellement justes.</p>

    <p><b>Expérimentez les bases du TAL :</b> Comparez le français et l'anglais, testez les poids des lettres (E adore dominer !), et comprenez d'un clic pourquoi le langage n'est pas aléatoire. Parfait pour réviser en rigolant - à vous de jouer !</p>

    <p><i>Pour aller plus loin : pensez à la loi de Zipf. Est-elle satisfaite pour ces séquences&nbsp;? A votre avis, pourquoi&nbsp;?</i></p>


<p> <a class="btn btn-primary w-100" href="borne-d-arcade">        Revenir à la borne d'arcade        </a> </p>
</div>



<div class="terminal">
      <button id="generate-button">Taper...</button>
      <input type="number" id="how-many" min="0" max="32" value="1" />
      lettre(s)...
      <select name="options" id="options">
        <option value="UN">... uniformément</option>
        <option value="FR">... française(s)</option>
        <option value="EN">... anglaise(s)</option>
      </select>
    </div>

<div id="output" class="terminal"></div>
    
{% raw %}

  <script type="py">  
from pyscript import web, when
import random
ALPHABET   = "AZERTYUIOPMLKJHGFDSQWXCVBN "
ONLYLET_FR = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'À', 'Â', 'Ä', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Î', 'Ï', 'Ñ', 'Ô', 'Ù', 'Û', 'Ü', 'Œ', 'Ÿ', ' ']
ONLYWEI_FR = [65309, 8290, 26156, 31644, 123936, 8991, 9081, 9219, 61044, 3933, 25, 49130, 22464, 52239, 41976, 22737, 9776, 54659, 61863, 59922, 52904, 13643, 5, 3216, 2476, 1334, 4139, 617, 1, 51, 471, 2656, 14803, 1970, 105, 615, 174, 1, 506, 377, 462, 9, 590, 7, 181031]
ONLYLET_EN = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ']
ONLYWEI_EN = [275701, 48853, 55056, 158086, 412160, 83534, 55279, 282657, 193926, 8880, 22281, 129919, 79929, 225026, 243143, 43248, 964, 170301, 189997, 317696, 83462, 30362, 65478, 1478, 58568, 2972, 749122]
BUFFER     = ""

@when("click", "#generate-button")
def handler(event):
  global BUFFER
  global ALPHABET
  global ONLYLET_FR
  global ONLYLET_EN
  global ONLYWEI_FR
  global ONLYWEI_EN
  OUTPUT_DIV  = web.page["output"]
  OPTIONS_DIV = web.page["options"]
  NUMBERS_DIV = web.page["how-many"]
  OPTION      = OPTIONS_DIV.value 
  NUMBER      = int(NUMBERS_DIV.value)
  if OPTION  =="UN":
    BUFFER += "".join(random.choices(ALPHABET, k = NUMBER))
  elif OPTION=="FR":
    BUFFER += "".join(random.choices(population = ONLYLET_FR, weights = ONLYWEI_FR, k = NUMBER))
  elif OPTION=="EN" :
    BUFFER += "".join(random.choices(population = ONLYLET_EN, weights = ONLYWEI_EN, k = NUMBER))
  OUTPUT_DIV.innerText = BUFFER
    </script>    
{% endraw %}

