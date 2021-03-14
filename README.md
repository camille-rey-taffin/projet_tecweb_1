#### projet_tecweb_1
##Installation
Installer Nginx et Gunicorn
Installer les dépendances du requirements.txt:

pip3 install -r requirements.txt

Pour configurer nginx, voir la section "PRE-REQUIS ET LANCEMENT DE L’APPLICATION" du guide d'utilisation.

##Lancement
Lancer avec Gunicorn :

sh launcher_gunicorn.sh

Lancer avec Python :

python run.py


Pour des explications plus détaillées, voir la section "PRE-REQUIS ET LANCEMENT DE L’APPLICATION" du guide d'utilisation.

##tests

Les tests sur le front-end se lancent en ligne de commande :
python tests_front.py

!! Il n'y a pas besoin d'avoir lancé préalablement les serveurs. Le script de test s'occupe de lancer le backend, de faire les tests puis d'arrêter le serveur backend lancé.
