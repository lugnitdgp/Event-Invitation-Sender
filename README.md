# Event Invitation Sender

<img width="1161" alt="screenshot" src="https://user-images.githubusercontent.com/33978990/68966550-6d9b3100-0804-11ea-919a-469d102acc69.png">

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
