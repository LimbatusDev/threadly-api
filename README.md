# Threadly
An easy way to create thread and programming it

## License

This project is not open source

## Running in development mode

First install the dependencies

    pip install -r requirements/development.txt
Then run the development server

    python manage.py runserver --settings=config.settings.development

### Running async tasks
Running redis server with docker

    docker run -d -p 6379:6379 redis

Running celery server

    celery -A config worker -l INFO
