# PRINGO

A Warehouse service.

## Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)
- [Travis CLI](http://blog.travis-ci.com/2013-01-14-new-client/)(Continuous Deployment)
- [Heroku Toolbelt](https://toolbelt.heroku.com/) (Continuous Deployment)

## SCHEMA

Please Go to docs on port 8001 to find Schema and better views

## Swagger

Visit /api-docs/ for swagger and trying out the API endpoints

## Description

Pringo is a service for Warehouse.

## CRUD endpoint for all models

## Get info on available storages to fullfill an order

        curl -d "{"lines":[{"sku":"abc","quantity":12},{"sku":"def","quantity":2}]}" -X POST http://127.0.0.1:8000/api/v1/orders/available-storages


## Filter an order for a customer

        curl http://127.0.0.1:8000/api/v1/orders/?q=muller

1- Swagger docs at /api-docs/
2- Genral docs at port 8001
3- You can deploy on Huroku directly by specifying credentials in env file

## Initialize the project

Start the dev server for local development:

```bash
docker-compose up
```

Create a superuser to login to the admin:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```

For running Tests

```bash
docker-compose run --rm web ./manage.py test
```

for showing available routes

```bash
docker-compose run --rm web ./manage.py show_urls
```

I have added a dump.json file that contains a dump from my local database for you to easily test, but you can run the command again like the following

phone_number(user_name): eslam
Password: eslam.gbh

```bash
docker-compose run --rm web ./manage.py loaddata dump.json
```

## NOTES

- No sotrage stock withdrawing or updating done while getting the available storages due to requirments

- Faker was used to give the ability to create fixtures easily and follow dry, while its fields was also restricted to eliminate the non-deterministic tests

- Custom Idempotency middle-ware was used to give the ability to try the endpoints without adding the header, but i would use 3rd party library like django-idempotency-key in production that gives 400 for missing header

- Default caching back-end (Local memory) was used for simplicity, but would use redis or memcached in production

- While it does not have a great impact here because of the previous point, Optimistic concurrency locking was used to show the solution

- you can find all the used framework in the requirments.txt, but the core is Python 3.6, Django 2.2

## HOW TO IMPROVE

- Separation of concern for filters in case of more generic and complex features required, by using custom Django filter backend

- Index the fields properly, PostgreSQL has a very useful type of index called BRIN (Block Range Index). Under some circumstances BRIN indexes can be more efficient than B-Tree indexes, as B-Tree can get extremely BIG.

- More negative test cases and coverage

- RUN script run.sh, for production deployment specially that the service will have a worker, so it needs a separate pod with separate command

## Continuous Deployment

Deployment is automated via Travis. When builds pass on the master or qa branch, Travis will deploy that branch to Heroku. Follow these steps to enable this feature.

Initialize the production server:

```
heroku create pringo-prod --remote prod && \
    heroku addons:create newrelic:wayne --app pringo-prod && \
    heroku addons:create heroku-postgresql:hobby-dev --app pringo-prod && \
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="pringo-prod" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="pringo.config" \
        --app pringo-prod
```

Initialize the qa server:

```
heroku create pringo-qa --remote qa && \
    heroku addons:create newrelic:wayne --app pringo-qa && \
    heroku addons:create heroku-postgresql:hobby-dev --app pringo-qa && \
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="pringo-qa" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="pringo.config" \
        --app pringo-qa
```

Securely add your Heroku credentials to Travis so that it can automatically deploy your changes:

```bash
travis encrypt HEROKU_AUTH_TOKEN="$(heroku auth:token)" --add
```

Commit your changes and push to master and qa to trigger your first deploys:

```bash
git commit -a -m "ci(travis): add Heroku credentials" && \
git push origin master:qa && \
git push origin master
```

You're now ready to continuously ship!
