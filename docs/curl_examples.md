
Voici quelques commandes curl pour tester les endpoints de l'API Fisher Fans.

## Authentification (Login)
Cette commande permet d'obtenir un token JWT.
```bash
curl -X POST http://localhost:8000/v1/login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john.doe@example.com&password=password"
```

## Création d'utilisateur
Crée un nouvel utilisateur.
```bash
curl -X POST http://localhost:8000/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Doe",
        "firstname": "John",
        "email": "john.doe@example.com",
        "password": "password",
        "phone": "1234567890",
        "status": "active"
      }'
```

## Récupérer un utilisateur (GET)
Récupère les détails d'un utilisateur spécifique.
```bash
curl -X GET http://localhost:8000/v1/users/1 \
  -H "Authorization: Bearer <TOKEN>"
```

## Mise à jour d'utilisateur (PUT)
Modifie les informations d'un utilisateur.
```bash
curl -X PUT http://localhost:8000/v1/users/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
        "name": "Doe",
        "firstname": "John",
        "email": "john.doe@example.com",
        "password": "newpassword",
        "phone": "0987654321",
        "status": "active"
      }'
```

## Suppression d'utilisateur (DELETE)
Supprime un utilisateur (nécessite un token d'administrateur).
```bash
curl -X DELETE http://localhost:8000/v1/users/1 \
  -H "Authorization: Bearer <ADMIN_TOKEN>"
```

## Création d'un bateau (POST)
Crée un nouveau bateau pour l'utilisateur authentifié (vérification du permis).
```bash
curl -X POST http://localhost:8000/v1/boats/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
        "name": "Fishing Boat",
        "boat_type": "open",
        "description": "Un bateau de pêche",
        "marque": "Yamaha",
        "annee_fabrication": 2015,
        "photo_url": "http://example.com/photo.jpg",
        "permis_requis": "côtier",
        "equipements": ["GPS", "radio VHF"],
        "caution": 500.0,
        "capacity": 6,
        "couchages": 3,
        "port_attache": "Marseille",
        "latitude": 43.296482,
        "longitude": 5.36978,
        "motorisation": "diesel",
        "puissance": 150
      }'
```

## Récupérer un bateau (GET)
Récupère les détails d'un bateau spécifique.
```bash
curl -X GET http://localhost:8000/v1/boats/1 \
  -H "Authorization: Bearer <TOKEN>"
```

## Mise à jour d'un bateau (PUT)
Met à jour un bateau avec uniquement les champs modifiés.
```bash
curl -X PUT http://localhost:8000/v1/boats/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
        "name": "Fishing Boat Updated",
        "capacity": 8
      }'
```

## Suppression d'un bateau (DELETE)
Supprime un bateau existant.
```bash
curl -X DELETE http://localhost:8000/v1/boats/1 \
  -H "Authorization: Bearer <TOKEN>"
```

## Liste des bateaux de l'utilisateur (GET)
Récupère la liste des bateaux appartenant à l'utilisateur authentifié.
```bash
curl -X GET http://localhost:8000/v1/boats/me \
  -H "Authorization: Bearer <TOKEN>"
```

## Filtrage des bateaux (GET)
Liste des bateaux filtrés par paramètres (exemple : nom et année de fabrication).
```bash
curl -X GET "http://localhost:8000/v1/boats/filter?name=Fishing&annee_fabrication=2015" \
  -H "Authorization: Bearer <TOKEN>"
```

## Création d'une sortie de pêche (Trip) (POST)
Crée une nouvelle sortie de pêche.
```bash
curl -X POST http://localhost:8000/v1/trips/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
        "title": "Morning Fishing Trip",
        "description": "A relaxing morning fishing trip.",
        "nb_passenger": 4,
        "price": 100.0,
        "trip_type": "fishing",
        "pricing_type": "per_person",
        "boat_id": 1
      }'
```

## Récupération d'une sortie de pêche (GET)
Récupère les détails d'une sortie de pêche.
```bash
curl -X GET http://localhost:8000/v1/trips/1 \
  -H "Authorization: Bearer <TOKEN>"
```

## Mise à jour d'une sortie de pêche (PUT)
Met à jour une sortie de pêche existante.
```bash
curl -X PUT http://localhost:8000/v1/trips/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
        "title": "Morning Fishing Trip Updated",
        "description": "Updated description.",
        "nb_passenger": 4,
        "price": 120.0,
        "trip_type": "fishing",
        "pricing_type": "per_person",
        "boat_id": 1
      }'
```

## Suppression d'une sortie de pêche (DELETE)
Supprime une sortie de pêche existante.
```bash
curl -X DELETE http://localhost:8000/v1/trips/1 \
  -H "Authorization: Bearer <TOKEN>"
```

## Création d'une réservation (POST)
Crée une réservation pour une sortie de pêche.
```bash
curl -X POST http://localhost:8000/v1/reservations/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
        "nb_places": 2,
        "total_price": 200.0,
        "user_id": 1,
        "trip_id": 1
      }'
```

## Récupération d'une réservation (GET)
Récupère les détails d'une réservation.
```bash
curl -X GET http://localhost:8000/v1/reservations/1 \
  -H "Authorization: Bearer <TOKEN>"
```

## Mise à jour d'une réservation (PUT)
Met à jour une réservation existante.
```bash
curl -X PUT http://localhost:8000/v1/reservations/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
        "nb_places": 3,
        "total_price": 300.0,
        "user_id": 1,
        "trip_id": 1
      }'
```

## Suppression d'une réservation (DELETE)
Annule une réservation existante.
```bash
curl -X DELETE http://localhost:8000/v1/reservations/1 \
  -H "Authorization: Bearer <TOKEN>"
```

## Création d'un log (POST)
Crée une entrée dans le carnet de pêche.
```bash
curl -X POST http://localhost:8000/v1/logs/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
        "fish": "Salmon",
        "picture": "http://example.com/salmon.jpg",
        "comment": "Caught a big one!",
        "size": 5.0,
        "weight": 10.0,
        "place": "Lake",
        "kept": true,
        "user_id": 1
      }'
```

## Récupération d'un log (GET)
Récupère les détails d'une entrée du carnet de pêche.
```bash
curl -X GET http://localhost:8000/v1/logs/1 \
  -H "Authorization: Bearer <TOKEN>"
```

## Mise à jour d'un log (PUT)
Modifie une entrée du carnet de pêche.
```bash
curl -X PUT http://localhost:8000/v1/logs/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
        "fish": "Updated Salmon",
        "picture": "http://example.com/salmon_updated.jpg",
        "comment": "Updated comment",
        "size": 6.0,
        "weight": 11.0,
        "place": "Lake",
        "kept": false,
        "user_id": 1
      }'
```

## Suppression d'un log (DELETE)
Supprime une entrée du carnet de pêche.
```bash
curl -X DELETE http://localhost:8000/v1/logs/1 \
  -H "Authorization: Bearer <TOKEN>"
```
