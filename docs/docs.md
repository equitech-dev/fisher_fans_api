# Fisher Fans API Documentation

## Structure des données

### User (Utilisateur)
- **Champs** : id, name, firstname, email, password, phone, picture, boat_license, insurance, company_name, siret, rcs, status, role
- **Relations** :
  - boats (1:n) - Bateaux possédés
  - trips (1:n) - Sorties organisées
  - reservations (1:n) - Réservations effectuées
  - logs (1:n) - Pages du carnet de pêche

### Boat (Bateau)
- **Champs** : id, name, description, brand, fabrication_year, photo_url, nb_passenger, nb_seat, port, latitude, longitude, motor_power, motor, license, boat_type, equipment, caution
- **Relations** :
  - owner (n:1) - Propriétaire du bateau
  - trips (1:n) - Sorties utilisant ce bateau

### Trip (Sortie)
- **Champs** : id, title, description, practical_info, trip_type, pricing_type, dates, schedules, nb_passengers, price, boat_id, organizer_id
- **Relations** :
  - boat (n:1) - Bateau utilisé
  - organizer (n:1) - Organisateur
  - reservations (1:n) - Réservations pour cette sortie

### Reservation
- **Champs** : id, trip_id, user_id, reservation_date, nb_seats, total_price
- **Relations** :
  - trip (n:1) - Sortie réservée
  - user (n:1) - Utilisateur ayant réservé

### Log (Carnet de pêche)
- **Champs** : id, fish_name, picture_url, comment, size, weight, location, catch_date, released, user_id
- **Relations** :
  - user (n:1) - Propriétaire du carnet

## Routes API

### Users (/v1/users)
- **POST /** : Création d'un utilisateur
- **GET /{id}** : Obtenir les détails d'un utilisateur
- **GET /{id}/profile** : Obtenir le profil complet (bateaux, sorties, réservations, logs)
- **PUT /{id}** : Modifier un utilisateur
- **DELETE /{id}** : Supprimer un utilisateur (admin uniquement)

### Boats (/v1/boats)
- **POST /** : Ajouter un nouveau bateau
- **GET /filter** : Filtrer les bateaux selon plusieurs critères
- **GET /{id}** : Obtenir les détails d'un bateau
- **PUT /{id}** : Modifier un bateau
- **DELETE /{id}** : Supprimer un bateau

### Trips (/v1/trips)
- **POST /** : Créer une nouvelle sortie
- **GET /filter** : Filtrer les sorties selon plusieurs critères
- **GET /{id}** : Obtenir les détails d'une sortie
- **PUT /{id}** : Modifier une sortie
- **DELETE /{id}** : Supprimer une sortie

### Reservations (/v1/reservations)
- **POST /** : Créer une nouvelle réservation
- **GET /filter** : Filtrer les réservations
- **GET /{id}** : Obtenir les détails d'une réservation
- **PUT /{id}** : Modifier une réservation
- **DELETE /{id}** : Supprimer une réservation

### Logs (/v1/logs)
- **POST /** : Ajouter une page au carnet
- **GET /filter** : Filtrer les pages du carnet
- **GET /{id}** : Obtenir une page spécifique
- **PUT /{id}** : Modifier une page
- **DELETE /{id}** : Supprimer une page

## Règles métier principales

### Gestion des utilisateurs
- Mot de passe hashé
- Rôles : user et admin
- Statuts : particulier et professionnel

### Gestion des bateaux
- Vérification de la propriété pour modifications
- Types de bateaux et équipements standardisés
- Localisation géographique

### Gestion des sorties
- Vérification de la propriété du bateau
- Respect des capacités du bateau
- Dates et horaires multiples possibles
- Types de tarification : global ou par personne

### Gestion des réservations
- Vérification des places disponibles
- Calcul automatique du prix total
- Dates de réservation valides

### Gestion du carnet de pêche
- Propriété des entrées
- Informations détaillées sur les prises
- Gestion des photos

## Sécurité
- Authentification par JWT
- Validation des droits d'accès
- Protection des routes sensibles