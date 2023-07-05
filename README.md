# APIs avec FastAPI - Datascientest
## Présentation
Pour cette évaluation, nous allons nous placer dans la peau d'une entreprise qui crée des questionnaires via une application pour Smartphone ou pour navigateur Web. Pour simplifier l'architecture de ces différents produits, l'entreprise veut mettre en place une API. Celle-ci a pour but d'interroger une base de données pour retourner une série de questions.

## Modèle de données
L'application utilise une base de données SQLite. Le modèle de données est le suivant :
![DS - fastapi.png](data%2FDS-fastapi.png)

## Installation
```bash
git clone
cd fastApi-datascientest
pip install -r requirements.txt
cp .env.example .env
## installation de la base de données via test_install
python ./setup.py 
```
Vous pouvez personnaliser le fichier .env avec vos propres paramètres.

## Lancement
```bash
python main.py
```

## Tests
J'ai utilisé une approche TDD, donc vous avez 100% de code coverage et vous pouvez lancer les tests avec la commande suivante : 
```bash
pytest -v
```

## Documentation
Vous pouvez accéder à la documentation de l'API via l'URL suivante : http://localhost:8000/docs
