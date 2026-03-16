# Medex

Medex is a B2B marketplace platform for medical procurement where healthcare institutions can request quotations for medicinal products and suppliers can respond with competitive offers. The system provides end-to-end procurement features including RFQ management, digital wallets, invoice generation with PDF rendering, product catalogs, order baskets, and role-based dashboards with analytics for suppliers and administrators.

## Setup

- Clone this repository with: `git clone https://github.com/Spounka/Medex-Frontend.git`
- Open the directory, in terminal with `cd Medex-Frontend`

### Local DEV

- Create a virtual env, example `python3 -m venv .venv`
- Source the virtual env, example `source .venv/bin/activate` on Linux
- Install dependencies with `pip3 install -r requirements.txt`
- Generate a secret key using `python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` and save the output key
- Create a `.env` file from `.env.example` and edit the values, paste your secret key into the field
- Create a super user with `python3 -m manage.py createsuperuser`
- Run with `python3 -m manage.py runserver 0.0.0.0:8000`

### Docker

- Generate a secret key using `python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` and save the output key to `.env` created from `.env.example`
- Create a `django.conf` from `django.conf.example`
- Docker build with `docker build --secret id=django,env=django.conf -t your-tag:dev .`
- Docker run with `docker run -p 8000:8000 -v .:/app --detach --name "your_name" --env-file django.your-tag:dev`

## About

This project was created for a client long ago and now I gave it a touch of modernization and pushed it for you all to see

## LICENSE

This project is under the GPL-3 License
