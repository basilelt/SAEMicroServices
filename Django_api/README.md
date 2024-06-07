# Microservices d'une Compagnie Aérienne

## Api Client

### Introduction
Le service Api Client gère les opérations liées aux clients, y compris l'authentification des clients et la gestion des réservations.

### Installation et Exécution

#### Utilisation de Docker

1. Construire l'image Docker :

    ```bash
    docker build -t api-client:latest .
    ```

2. Exécuter le conteneur Docker :

    ```bash
    docker run -d -p 8000:8000 --name api-client api-client:latest
    ```

#### Utilisation de Docker Compose

1. Démarrer le service avec Docker Compose :

    ```bash
    docker-compose up -d api-client
    ```

### Points de terminaison de l'API

#### 1. Inscription des clients

- **URL**: `/api/register`
- **Méthode**: `POST`
- **Corps de la requête**:
    ```json
    {
        "username": "exemple",
        "password": "motdepasse123",
        "email": "exemple@exemple.com"
    }
    ```
- **Réponse**:
    ```json
    {
        "message": "Utilisateur enregistré avec succès"
    }
    ```

#### 2. Connexion des clients

- **URL**: `/api/login`
- **Méthode**: `POST`
- **Corps de la requête**:
    ```json
    {
        "username": "exemple",
        "password": "motdepasse123"
    }
    ```
- **Réponse**:
    ```json
    {
        "token": "jeton_jwt_ici"
    }
    ```

#### 3. Réserver un vol

- **URL**: `/api/book`
- **Méthode**: `POST`
- **En-tête de la requête**: 
    ```http
    Authorization: Bearer jeton_jwt_ici
    ```
- **Corps de la requête**:
    ```json
    {
        "flight_id": "1234",
        "passenger_info": {
            "name": "John Doe",
            "passport": "A12345678"
        }
    }
    ```
- **Réponse**:
    ```json
    {
        "message": "Vol réservé avec succès",
        "booking_id": "5678"
    }
    ```

## Api Staff

### Introduction
Le service Api Staff gère les opérations liées au personnel, y compris l'authentification des employés et la gestion des informations de vol.

### Installation et Exécution

#### Utilisation de Docker

1. Construire l'image Docker :

    ```bash
    docker build -t api-staff:latest .
    ```

2. Exécuter le conteneur Docker :

    ```bash
    docker run -d -p 8001:8000 --name api-staff api-staff:latest
    ```

#### Utilisation de Docker Compose

1. Démarrer le service avec Docker Compose :

    ```bash
    docker-compose up -d api-staff
    ```

### Points de terminaison de l'API

#### 1. Connexion du personnel

- **URL**: `/api/staff/login`
- **Méthode**: `POST`
- **Corps de la requête**:
    ```json
    {
        "username": "personnel_exemple",
        "password": "motdepasse123"
    }
    ```
- **Réponse**:
    ```json
    {
        "token": "jeton_jwt_ici"
    }
    ```

#### 2. Ajouter un vol

- **URL**: `/api/staff/add-flight`
- **Méthode**: `POST`
- **En-tête de la requête**: 
    ```http
    Authorization: Bearer jeton_jwt_ici
    ```
- **Corps de la requête**:
    ```json
    {
        "flight_number": "ABC123",
        "departure": "2024-07-01T10:00:00Z",
        "arrival": "2024-07-01T14:00:00Z",
        "origin": "JFK",
        "destination": "LAX"
    }
    ```
- **Réponse**:
    ```json
    {
        "message": "Vol ajouté avec succès",
        "flight_id": "1234"
    }
    ```

#### 3. Supprimer un vol

- **URL**: `/api/staff/delete-flight`
- **Méthode**: `DELETE`
- **En-tête de la requête**: 
    ```http
    Authorization: Bearer jeton_jwt_ici
    ```
- **Corps de la requête**:
    ```json
    {
        "flight_id": "1234"
    }
    ```
- **Réponse**:
    ```json
    {
        "message": "Vol supprimé avec succès"
    }
    ```

