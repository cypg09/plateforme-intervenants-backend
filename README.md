# Plateforme Intervenants - Backend

Pour l'API, on va utiliser FastAPI : 
[FastAPI](https://fastapi.tiangolo.com/)

## Contribuer

Attention, par défaut, il ne faut absolument rien modifier. La plupart de ces fichiers sont des fichiers de configuration, que j'ai déjà créés. 

### Fichiers modifiables 

Pour rajouter des fonctionnalités, voici les 3 seuls fichiers à modifier :
- `models.py` : Fichier qui contient les définitions de toutes les tables de la base de données : on peut rajouter de nouvelles tables ou de nouvelles colonnes aux tables existantes ;
- `crud.py` : Fichier qui contient toutes les fonctions liant python à la base de données. Guidelines : chacune de ces fonctions doivent ne faire qu'une fonctionnalité. Par exemple, une fonction peut ajouter un élément à la base de donnée ; mais une fonction ne doit pas à la fois pouvoir ajouter un élément et en modifier un. Si l'on veut faire une fonction qui a plusieurs actions (modifier un élement et en créer un autre), c'est qu'il faut la découper en plusieurs fonctions. 
- `user.py` : Fichier qui contient toutes les fonctions de l'API en dehors de la partie `register` et `login` qui se trouvent dans `auth.py`.

