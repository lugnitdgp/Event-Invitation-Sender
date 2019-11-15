# Event Invitation Sender

## Building instructions

**NOTE**: Rabbit MQ needs to be installed for this application to work.

For Mac OS,
```
$ brew install rabbitmq

$ export PATH=$PATH:/usr/local/sbin (may or may not be required)

$ rabbitmq-server start -detached
```

Now, follow these steps in sequence
```
$ git clone https://github.com/JayjeetAtGithub/Event-Invitation-Sender

$ cd Event-Invitation-Sender/

$ pip install -r requirements.txt

$ python manage.py migrate

$ celery -A proj worker -l info

$ python manage.py runserver
```
