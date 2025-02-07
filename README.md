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
    2. Create **.env** file in the root level of the project directory and copy all environment variables from **.env-sample** in it and fill them based on your configuration.
    3. Run `docker-compose up --build`

## Usage

## Contributing

Make comfortable to share your feedbacks with me about this project, it helps me to improve myself :)
