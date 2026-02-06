---
layout: talpage-borne
title: "Borne d'arcade TAL - Tokeniseurs"
---

## Tokenizers à bases de règles

#### (Rule-based tokenizers)


Auteur : Pierre Mercuriali

<div class="explication">

<img src="/assets/images/tokeniseurs.png" class="rounded m-3 w-50"/>

  <p>La tokenization est la conversion d'un texte (une grosse unité de langage) 
      en unités plus petites (caractères, mots, etc.) en vue de leur traitement 
      automatique. 
      Les tokenizers de cette page fonctionnent à partir des règles suivantes :</p>
      
      <ul>
        <li>Séparation par espaces</li>
        <li>Séparation par espaces, et par les symboles de ponctuation <CODE>’'.,;?!"()-«»</CODE> </li>
        <li>Séparation à l'aide de l'expression régulière ("regex") <CODE> \w+(?:'\w+)?|[^\w\s] </CODE> </li>
      </ul>
      
<p> Le but de cette page est de tester ces différentes règles, 
      de les comparer, de voir où elles fonctionnent, et 
      où elles ne fonctionnent pas. 
  </p>


<p> <a class="btn btn-primary w-100" href="borne-d-arcade">        Revenir à la borne d'arcade        </a> </p>
</div>

<div class="terminal">
      
      <textarea id="input" rows="5" class="w-100">
      M. Jacques a déclaré : « La victoire 3-0 de l'équipe franco-allemande n'est pas due à un hasard : en effet, la S.N.C.F. a enregistré une hausse de 2,5% en 2026 ». M. Jacques a refusé d’expliquer la corrélation. D'ailleurs, son frère, O'Hara, a couru le cent mètres en 12’3. Il commente : « I'm also competing for the 5,000 meters. » Ce projet, bien que complexe, est re-pensé aujourd'hui, après la découverte de ce qu'il a qualifié de ’super-tired-syndrome’.
      </textarea>
      <br>
      <button id="tokenize">Tokénisation.</button>
  </div>
    
<div style="float: left;"> 
<fieldset class="terminal"><legend>Espaces</legend>              <p id="output1"> </p> </fieldset>
<fieldset class="terminal"><legend>Espaces + ponctuation</legend><p id="output2"> </p> </fieldset>
<fieldset class="terminal"><legend>Regex</legend>                <p id="output3"> </p> </fieldset>

</div>


{% raw %}

<script type="py">  
from pyscript import web, when
import re

def tokenize_spaces(input_text):
  TOKENS = input_text.split()
  return TOKENS

def tokenize_regex_simple(input_text):
  text   = re.sub("\n", " ", input_text)
  text = re.sub(r"([«»'\.,;\?!\"\(\)\-’])", r" \1 ", text)
  TOKENS = text.split()
  return TOKENS

def tokenize_regex(input_text):
  text   = re.sub("\n", " ", input_text)
  TOKENS = re.findall(r"\w+(?:'\w+)?|[^\w\s]", text)
  return TOKENS
  
def format_list(l):
  formatted_text = ""
  for token in l:
    formatted_text+= ' ' + '<span class="token">'+token+'</span>' 
  return formatted_text

@when("click", "#tokenize")
def handler(event):
  OUTPUT1_DIV = web.page["output1"]
  OUTPUT2_DIV = web.page["output2"]
  OUTPUT3_DIV = web.page["output3"]
  INPUT_DIV   = web.page["input"]
  INPUT_TEXT  = INPUT_DIV.value
  OUTPUT1_DIV.innerHTML = format_list(tokenize_spaces(INPUT_TEXT))
  OUTPUT2_DIV.innerHTML = format_list(tokenize_regex_simple(INPUT_TEXT))
  OUTPUT3_DIV.innerHTML = format_list(tokenize_regex(INPUT_TEXT))
    </script>    

{% endraw %}


