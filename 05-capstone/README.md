# Introduce Casting Agency Capstone Project
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 
You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

# Live Web: 
* Link: "https://capstone-1-t1ig.onrender.com"

# Installation instructions:
* run ```python -m venv .venv``` to create a virtualenv in project directory
* run ```source .venv/Scripts/activate``` to active your enviroment
* run ```pip install -r requirements.txt``` to install project dependencies
* run  ```export DATABASE_URL={username}:{password}@{host}:{port}/{database_name}```
    instead "username", "password", "host", "port", "database_name" to specific name
* run ```export FLASK_APP=app.py```
* run ```flask run --reload``` in terminal

# Models:
* Movies with attributes title and release date
* Actors with attributes name, age and gender

# Endpoints:
* GET /actors and /movies
* DELETE /actors/ and /movies/
* POST /actors and /movies and
* PATCH /actors/ and /movies/

# Roles:
* Casting Assistant
    * GET /actors and /movies

* Casting Director
    * GET /actors and /movies
    * ADD /actors and DELETE /actors
    * PATCH /actors and /movies
    
* Executive Producer
    * GET /actors and /movies
    * ADD /actors and DELETE /actors
    * PATCH /actors and /movies
    * ADD /movies and DELETE /movies

# Unit Test:
* One test for success behavior of each endpoint
* One test for error behavior of each endpoint
* At least two tests of RBAC for each role

Guide to unit test:
* run  ```export DATABASE_URL_TEST={username}:{password}@{host}:{port}/{database_name_test}```
    instead "username", "password", "host", "port", "database_name_test" to specific name
* run ```createdb -U postgres castingagencytest``` to create a database named castingagencytest
* run ```python tests.py``` to run unit test


# Test by Postman tool using JWT Tokens:
* Casting Assistant: ```eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlfeHRzcklfek1sWjZKTGViRFpNYyJ9.eyJpc3MiOiJodHRwczovL2Rldi1ieml5aGk4cXdhZWt3ZDN6LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTYyMjAyMzc2ODYxOTc0Mzk5OCIsImF1ZCI6ImltYWdlIiwiaWF0IjoxNzIwMzQyNDg1LCJleHAiOjE3MjAzNzg0ODUsInNjb3BlIjoiIiwiYXpwIjoiRFZobmRPM2U1SFdsS3FENnJ6RHU2ZG1Hc1VheVhyVDAiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.JSe1ok7fdUNdIJwJxkbDpCvac-ztuP7pcXWXXJUGODkIGuAR0a2__Y_YiC7qJL4U2wJBBWDZaIb7Jp6G7rmHrTzu-nkhR1m8P40MnL04LiSQEn1awyAZneG4qPKgx8EEWtHzDB02pwtIzPk-cNbRlBThFKVhCZkLYrkbqI-M-SlrF8SxcKgC7lobJ7WU2iRqxGe6Fec3KhXUBng-GaEeWiocN8n5jJG2jGT1_obJYHtCu7tJHox8cWpH-U5ARCYi1Crnid1I_kg57TeS1xap73u4UA3wbUOcwt0iJG8tsGnsLC8gkPvgFo-yjuSc4rsqXLCryzLLVr34s4THMPxY6g```

* Casting Director: ```eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlfeHRzcklfek1sWjZKTGViRFpNYyJ9.eyJpc3MiOiJodHRwczovL2Rldi1ieml5aGk4cXdhZWt3ZDN6LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwOTQ3Nzg0MzIwNjAyMzg2NTM1NyIsImF1ZCI6ImltYWdlIiwiaWF0IjoxNzIwMzQyNTY3LCJleHAiOjE3MjAzNzg1NjcsInNjb3BlIjoiIiwiYXpwIjoiRFZobmRPM2U1SFdsS3FENnJ6RHU2ZG1Hc1VheVhyVDAiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzL2RlbGV0ZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzL3VwZGF0ZSIsInBhdGNoOm1vdmllcy91cGRhdGUiLCJwb3N0OmFjdG9ycy9jcmVhdGUiXX0.TqKvPBaOoUDrOPfg6wvApHGCiF7CtUrLSvQIA8vgQxew6bS_tKDzVbAkI6VerRETXj86s_KenqdI3vRPQmxymGCSYr12yfyzos_rAzqiTKW-cXimP_RL5kBljdOw_avVgPnJ5BiYK_KK_89VoAFrWS9J-7pVmAu7eUolUnt2UU4dLISqx5GGn8YSMTAICoMaMOiwustaRJbIENTuAB8bANl1x3WqKMNA-nJsROsgrofN8doP-08HXBOC3ceUiXByYikDR7Tbb-zyCGnbotTfS9Va1g-RkwLknxxh3_vcZM2um-fSwbXigXXGIIPz6FasAhikHGXk8u-hEIZJYVjOcA```

* Executive Producer: ```eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlfeHRzcklfek1sWjZKTGViRFpNYyJ9.eyJpc3MiOiJodHRwczovL2Rldi1ieml5aGk4cXdhZWt3ZDN6LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjNmYWRmZDM3MDZlYmRhN2Q3ZjhmYjkiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTcyMDM0MjYwNywiZXhwIjoxNzIwMzc4NjA3LCJzY29wZSI6IiIsImF6cCI6IkRWaG5kTzNlNUhXbEtxRDZyekR1NmRtR3NVYXlYclQwIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycy9kZWxldGUiLCJkZWxldGU6ZHJpbmtzIiwiZGVsZXRlOm1vdmllcy9kZWxldGUiLCJnZXQ6YWN0b3JzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzL3VwZGF0ZSIsInBhdGNoOmRyaW5rcyIsInBhdGNoOm1vdmllcy91cGRhdGUiLCJwb3N0OmFjdG9ycy9jcmVhdGUiLCJwb3N0OmFjdG9ycy9uZXciLCJwb3N0OmRyaW5rcyIsInBvc3Q6bW92aWVzL2NyZWF0ZSIsInBvc3Q6bW92aWVzL25ldyJdfQ.jUf1FzFt0VP-XqTZFWtCjaM-oNJhlSAjpZeQZcmzUaD47B9eQrlFlOVVAdOyTVdWypU61xaUjsemgl31bWyzM4d4R8o2xrHY7yec5Upms3jrdl1Tf5CxugZC8uL8NPFhzb24fJmqpIrHYOwU6fA0nhK9No-9s0YIw305yuyxKXz5H24Bm0S1TtVOzjFL9l6qod2f35qvdrCZyEI_avew0kromTeQndDt8WCM6geZioiYr_D2L9OG9Xa95M8HQPNnw1Evzy9njvw0kpMLANhuLBscohqhEUZh3jcZSy4yA5qkvHPtVtEdgvvN73Pk31yzpy_AjHxh_l5LXhuyM8iFSg```

# API Endpoints Documentation

# GET /
Display a default page:

Request Arguments: None
Return: An object with a description, success key
```
{
    "description": "Welcome to Casting Agency.",
    "success": true
}
```

# GET /actors
Display all actors:

Request Arguments: None
Return: An object with a actors, success key
```
{
    "actors": [
        {
            "age": 61,
            "gender": "female",
            "id": 1,
            "movie_id": 1,
            "name": "Johnny Depp"
        },
        {
            "age": 24,
            "gender": "female",
            "id": 2,
            "movie_id": 2,
            "name": "Le Huynh Duc"
        },
    ],
    "success": true
}
```

# GET /movies
Display all movies:

Request Arguments: None
Return: An object with a movies, success key
```
{
    "movies": [
        {
            "id": 1,
            "release_year": 1997,
            "title": "Titanic"
        },
        {
            "id": 2,
            "release_year": 2003,
            "title": "The Curse of the Black Pearl"
        },
    ],
    "success": true
}
```

# POST /movies/create
Create a new movie:

Request Arguments: None
Return: An object with a movie_id, success key
```
{
    "movie_id": 1,
    "success": true
}
```

# POST /actors/create
Create a new actor:

Request Arguments: None
Return: An object with a actor_id, success key
```
{
    "actor_id": 2,
    "success": true
}
```

# PATCH /movies/update/<movie_id>
Update movie based on id:

Request Arguments: movie id
Return: An object with a movie_id, success key
```
{
    "movie_id": 1,
    "success": true
}
```

# PATCH /actors/update/<actor_id>
Update actor based on id:

Request Arguments: actor id
Return: An object with a actor_id, success key
```
{
    "actor_id": 2,
    "success": true
}
```

# DELETE /movies/delete/<movie_id>
Delete a movie based on id:

Request Arguments: movie id
Return: An object with a delete, success key
```
{
    "delete": 1,
    "success": true
}
```

# DELETE /movies/actors/<actor_id>
Deletes an actor based on id:

Request Arguments: actor id
Return: An object with a delete, success key
```
{
    "delete": 1,
    "success": true
}
```
