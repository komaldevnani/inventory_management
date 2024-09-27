To test

curl -X POST http://localhost:8000/token/ \
-H "Content-Type: application/json" \
-d '{"username": "komal", "password": "komal0808"}'

curl -H "Authorization: Bearer your-access-token" http://localhost:8000/items/
