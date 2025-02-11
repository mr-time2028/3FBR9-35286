# 3FBR9-35286

A booking system for a restaurant.

## Installation

- Clone the repository.

* ### Development
1. In the root level of the project directory, create a virtual environment and activate it.
2. Run `pip install -r requirements.txt` to install project's necessary packages.
3. Create a **.env** file in the root level of the project directory and copy all environment variables from **.env-sample** in it and fill them based on your configuration.
4. Run `docker-compose -f docker-compose.dev.yml up`
5. Change your work directory to the ./app and then run `./manage.py runserver` or `python3 manage.py runserver`


* ### Production
1. Run `pip install -r requirements.txt` to install project's necessary packages.
2. Run `docker-compose up --build`

## Usage
Read at `/api/schema/swagger-ui/` path

## Hints
It would have been better if I had added many things to improve the project, but I didn't succeed due to lack of time.
1. two branches (main and develop)
2. write tests (I didn't write)
3. consider database locking system for reservation
4. consider some seed data for the database

## Contributing

Make comfortable to share your feedbacks with me about this project, it helps me to improve myself :)
