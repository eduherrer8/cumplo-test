
# Cumplo test
Desafío Tecnología Área de Desarrollo

## Table of contents
* [Environment URLS](#environment-urls)
* [Setup the project](#setup-the-project)
* [Running the stack for development](#running-the-stack-for-development)
* [Stop the project](#stop-the-project)
* [Technical memories](#technical-memories)

### Enviroment URLs

* **Testing** - https://cumplo-test-ed.herokuapp.com/


## Development

### Setup the project

1. Clone this repository:
```
$ git clone git@github.com:eduherrer8/cumplo-test.git
```

2. Build the images:
```
$ docker-compose build
```

3. Create the container for the DB:
```
$ docker-compose up -d mysql
```
4 create your .env file at the root of the project, follow the example.env

5. let the web server up and ready
```
$ docker-compose up web
```
6. Sync the migrations
```
$ docker-compose run --rm web python manage.py migrate
```
7. Create a superuser or loadd the fixtures

7.1 Create a super user
```
$ docker-compose run --rm web python manage.py createsuperuser
```
7.2 Load the fixtures
```
$ docker-compose run --rm web python manage.py loaddata cumplo_test_web/fixtures/users.json
```


### Running the stack for development

1. Open a terminal and run:
```
$ docker-compose up web
```
2. Attach into a terminal
```
$ docker-compose exec web bash
```
### Stop the project

1. To stop every container run in the terminal:
```
$ docker-compose down
```

### Technical memories


The version on the compose file for mysql is the one that was required but in the other hand heroku didn't allow me to set this version.
There are some validations on the initial dates, not as many as it should be.

Checkout the admin site, it's quite an awesome place to handle certain app behaivior, the admin site is on `https://cumplo-test-ed.herokuapp.com/admin`, as a glimpse of the capability of this site I let this admin to be the users adminstrations site

Work to the future:
- Adjust the minimum date according to the information obtained in the API.
- Use a specialize service for storing the static and media files, such as aws buckets.
- Make some testing
