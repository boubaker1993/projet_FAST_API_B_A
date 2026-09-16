# API FastAPI - Olist

## Description

Cette API permet d'interroger les données du dataset Brazilian E-Commerce Public Dataset by Olist stockées dans MongoDB.

L'API utilise :

- Python
- FastAPI
- MongoDB
- PyMongo

## Installer les dépendances :

pip install -r requirements.txt

## Configuration

Créer un fichier `.env` :

MONGODB_URI="mongodb+srv://..."

## Lancer l'API

python -m uvicorn main:app --reload

L'API est disponible sur :

http://127.0.0.1:8000

Documentation Swagger :

http://127.0.0.1:8000/docs

## Endpoint

### GET /produits-review-olist

Retourne les informations concernant les commandes livrées :

- order_id
- customer_id
- zipcode
- product_id
- product_category
- price
- review_score

## Exemple

GET /produits-review-olist

Réponse :

{
    "order_id": "...",
    "customer_id": "...",
    "zipcode": 12345,
    "product_id": "...",
    "product_category": "...",
    "price": 29.99,
    "review_score": 5
}

## Base MongoDB

Database :

OLIST

Collections :

- orders
- customers
- order_items
- products
- order_reviews"# projet_FAST_API_B_A" 
