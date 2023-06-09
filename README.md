# Smoked Catfish Delivery API

This repository contains REST API for a Smoked Catfish Delivery service built with FastAPI.

## Database Design
<img src="https://res.cloudinary.com/dkezlmzn1/image/upload/v1681765837/api-db_veiiu0.png"/>

## Endpoints
| METHOD | ENDPOINT | FUNCTIONALITY |ACCESS|
| ------- | ----- | ------------- | ------------- |
| *POST* | ```/auth/signup/``` | _Register new user_| _All users_|
| *POST* | ```/auth/login/``` | _Login user_|_All users_|
| *POST* | ```/orders/order/``` | _Place an order_|_All users_|
| *PUT* | ```/orders/order/update/{order_id}/``` | _Update an order_|_All users_|
| *PUT* | ```/orders/order/status/{order_id}/``` | _Update order status_|_Superuser_|
| *DELETE* | ```/orders/order/delete/{order_id}/``` | _Delete/Remove an order_ |_All users_|
| *GET* | ```/orders/user/orders/``` | _Get user's orders_|_All users_|
| *GET* | ```/orders/orders/``` | _List all orders made_|_Superuser_|
| *GET* | ```/orders/orders/{order_id}/``` | _Retrieve an order_|_Superuser_|
| *GET* | ```/orders/user/order/{order_id}/``` | _Get user's specific order_|_All users_|
| *GET* | ```/docs/``` | _View API documentation_|_All users_|

<img src="https://res.cloudinary.com/dkezlmzn1/image/upload/v1681850449/Screenshot_2023-04-18_at_9.38.28_PM_rjzhsa.png"/>

<img src="https://res.cloudinary.com/dkezlmzn1/image/upload/v1681850453/Screenshot_2023-04-18_at_9.38.36_PM_ghubov.png"/>

## Tools
* FastAPI
* FastAPI JWT Auth
* Postgres
* Uvicorn
* SQLAlchemy
* Postman
* Psycopg2

Check requirements.txt for complete tools

## Installation

```bash
git clone https://github.com/johndiginee/smoked-catfish-delivery-api.git
```
```bash
python3 -m venv my_env
```
```bash
source my_env/bin/activate
```
```bash
pip install -r requirements.txt
```
Set Up your PostgreSQL database and set its URI in your database.py
```bash
engine=create_engine('postgresql://<username>:<password>@localhost:<port>/<db_name>',
    echo=True
)
```
```bash
python3 init_db.py
```
```bash
uvicorn main:app --reload
```