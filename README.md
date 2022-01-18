# Plateforme Intervenants - Backend

Pour l'API, on va utiliser FastAPI : 
[FastAPI](https://fastapi.tiangolo.com/).

## 🤲 Contribuer

Attention, par défaut, il ne faut absolument rien modifier. La plupart de ces fichiers sont des fichiers de configuration, que j'ai déjà créés. 

### ✋ Avant de contribuer

Les best practices **doivent** être respectées afin d'assurer la maintenabilité du code.
Merci d'être au clair sur:
- Le [PEP-8](https://www.python.org/dev/peps/pep-0008/#introduction) ;
- La [documentation du code](https://realpython.com/documenting-python-code/) ;
- L'utilisation de git.

La branche principale est `main`.

Chaque personne qui veut contribuer doit : 
- Régulièrement mettre à jour son code :
```
git fetch
```
- Créer sur son ordinateur une nouvelle branche : dev/{username}/{nom_de_la_fonctionnalite_a_ajouter}
Par exemple : dev/cypg09/login
```
git branch dev/{username}/{nom_de_la_fonctionnalite_a_ajouter}
```
- Envoyer sur le repository cette nouvelle branche :
```
git --set-upstream origin dev/{username}/{nom_de_la_fonctionnalite_a_ajouter}
```
- Faire des commits atomiques [Commits atomiques](https://letmegooglethat.com/?q=git+atomic+commits) et push régulièrement
- Quand elle pense avoir fini son travail, créer une `merge request`, en mettant comme source sa branche et comme target `main`. [Plus d'information](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html). 
- **NE PAS AUTO-APPROUVER LES MERGE REQUESTS, LAISSER LE CREATEUR DU PROJET APPROUVER LUI-MÊME, SINON CA N'A PLUS D'INTERÊT !**


### ✍️ Fichiers modifiables 

Pour rajouter des fonctionnalités, voici les **3 seuls fichiers à modifier** :
- `models.py` : Fichier qui contient les définitions de toutes les tables de la base de données : on peut rajouter de nouvelles tables ou de nouvelles colonnes aux tables existantes ;
- `crud.py` : Fichier qui contient toutes les fonctions liant python à la base de données. Guidelines : chacune de ces fonctions doivent ne faire qu'une fonctionnalité. Par exemple, une fonction peut ajouter un élément à la base de donnée ; mais une fonction ne doit pas à la fois pouvoir ajouter un élément et en modifier un. Si l'on veut faire une fonction qui a plusieurs actions (modifier un élement et en créer un autre), c'est qu'il faut la découper en plusieurs fonctions. 
- `user.py` : Fichier qui contient toutes les fonctions de l'API en dehors de la partie `register` et `login` qui se trouvent dans `auth.py`.
