# ecommerce

Products can be added or can be updated using same API.
For adding new products only essential name, price and quantity needs to be sent. 
Format for bulk product addition.
[
  {
    "name": "Coca Cola 2 ltr",
    "price": 90,
    "quantity": 30
  },
  {
    "name": "Coca Cola 700ml",
    "price": 40,
    "quantity": 50
  },
  {
    "pid":"P8607F"
    "name": "Coca Cola 200ml",
    "price": 20,
    "quantity": 100
  }
]

For updating the products quantity and price pid needs to be sent.
[
  {
    "pid":"P8607F",
    "name": "Coca Cola 700ml",
    "price": 45,
    "quantity": 20
  }
]

API format for placing the order:
[
    {
        "pid": "P0850B",
        "name": "Parle G 120 gms",
        "quantity": 15,
        "price": 10
    },
    {
        "pid": "PC51FA",
        "name": "Parle G 120 gms",
        "quantity": 15,
        "price": 8
    }
]


