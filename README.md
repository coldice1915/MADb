# Casting Agency App
The Casting Agency models an app that is responsible for creating movies and managing and assigning actors to those movies. I was assigned to create a system to simplify and streamline processes.

[Link to Casting Agency App](https://casting-agency-app.herokuapp.com/)
## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

### Running the server

First ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python app.py
```

## Authentication
This app uses Auth0 to authenticate users and grant role-based permissions.

- Casting Assistant:
    - Can view actors and movies

- Casting Director: All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies

- Executive Producer: All permissions a Casting Director has and…
    - Add or delete a movie from the database

[Link](https://coldice.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=IkVswtQIez2awQnLiR5XeYh9N02WE3kF&redirect_uri=https://0.0.0.0:8080/) to Auth0 login for token.

user | pass = ca@ca.com | CastingAssistant1<br>
user | pass = cd@ca.com | CastingDirector1<br>
user | pass = ep@ca.com | ExecutiveProducer1

## API Reference

### Error Handling

Errors are returned as JSON objects in the following format:
```
{
    "error": 404, 
    "message": "resource not found", 
    "success": false
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 404: Resource Not Found
- 422: Not Processable

### Endpoints

#### Get '/'

- General
    - App homepage
- Sample: `curl http://0.0.0.0:8080`
```
Come see all our actors and movies
```

#### GET '/actors'

- General
    - Returns all actors
- Sample: `curl -H "Accept: application/json" -H "Authorization: Bearer <ACCESS TOKEN>“ http://0.0.0.0:8080/actors`
```
{
  "actors": [
    {
      "age": 51, 
      "gender": "Male", 
      "id": 1, 
      "name": "Will Smith"
    }, 
    {
      "age": 29, 
      "gender": "Female", 
      "id": 2, 
      "name": "Margot Robbie"
    }
  ], 
  "success": true
}
```

#### GET '/movies'

- General
    - Returns all movies
- Sample: `curl -H "Accept: application/json" -H "Authorization: Bearer <ACCESS TOKEN>“ http://0.0.0.0:8080/movies`
```
{
  "movies": [
    {
      "id": 1, 
      "title": "The Pursuit of Happiness", 
      "year": 2006
    }, 
    {
      "id": 2, 
      "title": "Suicide Squad", 
      "year": 2016
    }
  ], 
  "success": true
}
```

#### POST '/actors'

- General
    - Adds an actor to the database
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{“name”:”Robert Williams”,“gender”:”Male”,“age”:63}’ http://0.0.0.0:8080/actors`
```
{
  "actors": {
    "id": 3,
    "name": "Robert Williams",
    "gender": "Male",
    "age": 63
  },
  "success": true
}
```

#### POST '/movies'

- General
    - Adds a movie to the database
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"title":”Aladdin”,"year":1992}’ http://0.0.0.0:8080/movies`
```
{
  "movies": {
    "id": 3,
    "title": "Aladdin",
    "year": 1992
  },
  "success": true
}
```

#### PATCH '/actors/<int:actor_id>'

- General
    - Updates an actor
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{“name”:”Robin Williams”,“gender”:”Female”,“age”:36}’ http://0.0.0.0:8080/actors/3`
```
{
  "actors": {
    "id": 3,
    "name": "Robert Williams",
    "gender": "Female",
    "age": 36
  },
  "success": true
}
```

#### PATCH '/movies/<int:movie_id>'

- General
    - Updates a movie
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"title":”Aladdin 2”,"year":2002}’ http://0.0.0.0:8080/movies/3`
```
{
  "movies": {
    "id": 3,
    "title": "Aladdin 2",
    "year": 2002
  },
  "success": true
}
```

#### DELETE '/actors/<int:actor_id>'

- General
    - Deletes an actor
- Sample: `curl -X DELETE http://0.0.0.0:8080/actors/3`
```
{
  "id": 3,
  "success": true
}
```

#### DELETE '/movies/<int:movie_id>'

- General
    - Deletes a movie
- Sample: `curl -X DELETE http://0.0.0.0:8080/movies/3`
```
{
  "id": 3,
  "success": true
}
```


### Testing
Export the setup:
```bash
source setup.sh
```
Then run the app:
```bash
python test_app.py
```


##### Sources
Udacity