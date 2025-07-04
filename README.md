# Installation et configuration de l'environnement

Suivez les étapes ci-dessous pour configurer votre environnement :

1. Créez un environnement virtuel Python :

   ```bash
   python -m venv env
   ```

2. Activez l'environnement virtuel :

   ```bash
   source ./env/bin/activate
   ```

3. Pour valider la mise à jour de vos modèles :

   ```bash
   alembic -c alembic.ini revision --autogenerate -m "description of your changes"
   ```

4. Executer la mise à jour de votre base de données :

   ```bash
   alembic -c alembic.ini upgrade head
   ```

5. Lancer l'application (pour le moment):

   ```bash
   uvicorn main:app --reload
   ```
