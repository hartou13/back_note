# Docker Compose - MyAuxilium Backend

Ce projet utilise Docker Compose pour orchestrer l'application backend FastAPI et la base de données MySQL.

## Prérequis

- Docker
- Docker Compose

## Structure des services

### 🐳 Services inclus

- **backend**: Application FastAPI (port 8000)
- **mysql**: Base de données MySQL 8.0 (port 3306)

## 🚀 Démarrage rapide

### 1. Cloner le projet et se placer dans le répertoire
```bash
cd /path/to/your/project
```

### 2. Configurer les variables d'environnement
```bash
# Modifier le fichier app.env selon vos besoins
# Ce fichier sera copié dans le conteneur comme .env
nano app.env
```

### 3. Construire et démarrer les services
```bash
# Démarrer en mode détaché
docker-compose up -d

# Ou démarrer en mode interactif pour voir les logs
docker-compose up
```

### 4. Vérifier que les services fonctionnent
```bash
# Vérifier l'état des conteneurs
docker-compose ps

# Voir les logs
docker-compose logs -f backend
docker-compose logs -f mysql
```

## 📋 Commandes utiles

### Gestion des services
```bash
# Arrêter les services
docker-compose down

# Redémarrer un service spécifique
docker-compose restart backend

# Rebuilder les images
docker-compose build

# Rebuild et redémarrer
docker-compose up --build
```

### Base de données
```bash
# Accéder au shell MySQL
docker-compose exec mysql mysql -u myauxilium_user -p myauxilium

# Sauvegarder la base de données
docker-compose exec mysql mysqldump -u myauxilium_user -p myauxilium > backup.sql

# Restaurer la base de données
docker-compose exec -T mysql mysql -u myauxilium_user -p myauxilium < backup.sql
```

### Développement
```bash
# Accéder au shell du backend
docker-compose exec backend bash

# Voir les logs en temps réel
docker-compose logs -f backend

# Exécuter les migrations Alembic
docker-compose exec backend alembic upgrade head
```

## 🔧 Configuration

### Variables d'environnement

Les variables d'environnement sont configurées dans le fichier `app.env` qui est copié dans le conteneur lors du build. Modifiez ce fichier selon vos besoins :

```env
# Configuration MySQL
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DATABASE=myauxilium
MYSQL_USER=myauxilium_user
MYSQL_PASSWORD=myauxilium_password

# Configuration JWT
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRACY=86400
```

**Note importante** : Après modification du fichier `app.env`, vous devez rebuilder l'image Docker :
```bash
docker-compose build backend
```

### Ports exposés

- **Backend FastAPI**: http://localhost:8000
- **MySQL**: localhost:3306

## 🗄️ Persistance des données

Les données MySQL sont persistées dans un volume Docker nommé `mysql_data`.

## 🛠️ Dépannage

### Le backend ne se connecte pas à MySQL
```bash
# Vérifier que MySQL est en cours d'exécution
docker-compose ps mysql

# Vérifier les logs MySQL
docker-compose logs mysql

# Redémarrer les services
docker-compose restart
```

### Erreurs de build
```bash
# Nettoyer les images et rebuilder
docker-compose down
docker system prune -f
docker-compose build --no-cache
docker-compose up
```

### Réinitialiser complètement
```bash
# Arrêter et supprimer tous les conteneurs et volumes
docker-compose down -v
docker-compose up --build
```

## 🔍 Monitoring

L'application FastAPI inclut un health check accessible à :
- http://localhost:8000/health-check

## 📝 Notes importantes

1. **Sécurité** : Changez les mots de passe par défaut en production
2. **Performance** : Ajustez les ressources selon vos besoins
3. **Backup** : Sauvegardez régulièrement votre base de données
4. **Logs** : Surveillez les logs pour détecter les problèmes 