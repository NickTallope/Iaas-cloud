# YouTube Data Pipeline

Ce projet a été effectué dans notre cursus scolaire, plus précisément dans le cours d'IaaS (Infrastructure-as-a-Service). L'objectif est de développer et de déployer un service pour récupérer et traiter les données de YouTube quotidiennement sur plusieurs chaînes YouTube.

## Contributeurs/Eleves
- Ferroni Sandro
- Gassem Aymen
- Gravejal Paul
- Mélanger Alexandre


## Configuration

- Créer un fichier .env à la racine du projet et le compléter :
   ```
   YOUTUBE_API_KEY=my_youtube_api_key
   DB_PASSWORD=my_password
   DB_USER=postgres
   DB_NAME=postgres
   DB_HOST=localhost
   ```


## Installation

- Construiser les images Docker :
   ```
   make build-image
   ```

- Lancer les services :
   ```
   make build-container
   ```


## Fonctionnement

Tous les jours, notre projet exécutera ses tâches de manière autonome en récupérant les données YouTube à 18h et en les traitant à 18h30.

Cependant, nous pouvons également tester notre code en effectuant :

- Récupération des données et traitement en local:
   ```
   make docker-run
   ```

- Push les images sur le cloud manuellement :

   ```
   make tag_image_retrevial
   make tag_image_processing
   ```


## Architecture du projet

.
├── auth.py
├── celerybeat-schedule
├── celery_config.py
├── credentials.json
├── docker-compose.yml
├── Dockerfile
├── Dockerfile-celery
├── init.sql
├── LICENSE
├── local_storage
├── main.py
├── Makefile
├── README.md
├── requirements.txt
├── storage.py
├── test.ipynb
├── youtube_api.py
├── youtube-data-processing
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── tasks.py
└── youtube-data-retrieval
    ├── auth.py
    ├── credentials.json
    ├── Dockerfile
    ├── main.py
    ├── requirements.txt
    ├── storage.py
    └── tasks.py


## Teste sur les services

- Vérifier que les services sont en cours d'exécution :
   ```
   docker-compose ps
   ```

- Consulter les logs des services :
   ```
   docker-compose logs youtube-data-retrieval
   docker-compose logs youtube-data-processing
   ```

- Connectez-vous à la base de données PostgreSQL pour vérifier les données insérées :
   ```
   make connection-database
   ```
   Puis :
   ```sql
   SELECT * FROM channel;
   SELECT * FROM video;
   SELECT * FROM import_task;
   ```

- Vérifier les fichiers CSV dans `local_storage/`.


### Réinitialiser le pipeline
  ```
  docker-compose down -v
  docker-compose up -d --build
  ```

### Netoyage

Après toute utilisation, n'oubliez pas pour rendre votre dossier plus propre.

- Stopper et supprimer toutes les images docker :
   ```
   make docker-stop
   make docker-clean
   ```
   Si les commandes ne marche pas, réutilisez celle dans le Makefile directement sur le terminal.

- Supprimer les dossiers et fichiers obsolètes.
   ```
   make clean
   ```
