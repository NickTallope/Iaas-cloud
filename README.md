# YouTube Data Pipeline

Ce projet est un pipeline de données qui récupère des informations sur des chaînes YouTube spécifiques et leurs dernières vidéos, puis les stocke dans une base de données PostgreSQL.

## Table des matières

1. [Prérequis](#prérequis)
2. [Configuration](#configuration)
3. [Installation](#installation)
4. [Utilisation](#utilisation)
5. [Structure du projet](#structure-du-projet)
6. [Tester les services](#tester-les-services)
7. [Dépannage](#dépannage)

## Prérequis

- Docker et Docker Compose
- Clé API YouTube (obtenue depuis la Google Developers Console)

## Configuration

1. Clonez ce dépôt sur votre machine locale :
   ```
   git clone https://github.com/NickTallope/Iaas-cloud.git
   cd Iaas-cloud
   ```

2. Créez un fichier `.env` à la racine du projet et ajoutez votre clé API YouTube et vos identifiants:
   ```
   YOUTUBE_API_KEY=votre_clé_api_youtube
   DB_PASSWORD=123
   DB_USER=postgres
   DB_NAME=postgres
   DB_HOST=localhost
   ```

## Installation

1. Construisez les images Docker :
   ```
   make build-image
   ```

2. Lancez les services :
   ```
   make build-container
   ```

## Utilisation

Le pipeline est configuré pour s'exécuter automatiquement :
- La tâche de récupération des données s'exécute tous les jours à 18h00.
- La tâche de traitement des données s'exécute tous les jours à 18h30.

Vous pouvez également exécuter les tâches manuellement :

1. Pour la récupération des données et traitement en local:
   ```
   make docker-run
   ```

3. Pour push les images sur le cloud manuellement :

   ````
   make tag_image_retrevial
   make tag_image_processing
   ```

## Structure du projet

- `youtube-data-retrieval/`: Service de récupération des données YouTube
- `youtube-data-processing/`: Service de traitement et d'insertion des données dans la base de données
- `local_storage/`: Dossier partagé pour stocker les fichiers CSV temporaires
- `init.sql`: Script d'initialisation de la base de données
- `docker-compose.yml`: Configuration des services Docker
- `celery_config.py`: Configuration de Celery pour la planification des tâches

## Tester les services

1. Vérifiez que tous les services sont en cours d'exécution :
   ```
   docker-compose ps
   ```

2. Consultez les logs des services :
   ```
   docker-compose logs youtube-data-retrieval
   docker-compose logs youtube-data-processing
   ```

3. Vérifiez les fichiers CSV générés dans le dossier `local_storage/`.

4. Connectez-vous à la base de données PostgreSQL pour vérifier les données insérées :
   ```
   make connection-database
   ```
   Puis exécutez des requêtes SQL, par exemple :
   ```sql
   SELECT * FROM channel;
   SELECT * FROM video;
   SELECT * FROM import_task;
   ```

## Dépannage

- Si vous rencontrez des problèmes avec les permissions des fichiers, assurez-vous que les dossiers partagés ont les bonnes permissions :
  ```
  chmod -R 777 local_storage/
  ```

- En cas d'erreur liée à l'API YouTube, vérifiez que votre clé API est correcte et n'a pas atteint ses limites d'utilisation.

- Pour réinitialiser complètement le pipeline, vous pouvez supprimer tous les conteneurs et volumes, puis reconstruire :
  ```
  docker-compose down -v
  docker-compose up -d --build
  ```

## Netoyage

- Après toute utilisation, n'oubliez pas pour rendre votre dossier plus propre.

1. Stopper et supprimer toutes les images docker :
   ```
   make docker-stop
   make docker-clean
   ```
   Si les commandes ne marche pas, réutilisez celle dans le Makefile directement sur le terminal.

2. Supprimer les dossiers et fichiers obsolètes.
   ```
   make clean
   ```

Pour toute autre question ou problème, n'hésitez pas à ouvrir une issue dans le dépôt du projet.