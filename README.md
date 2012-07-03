Redis Job Queue
===============

Requirements
------------

* [python](http://python.org)
* [redis 2.6](http://redis.io)
* [redis-py](https://github.com/andymccurdy/redis-py)

Running
-------

Start redis server:

    $ redis-server

Run 100 jobs:

    $ python main.py 100

Todo
====

* Write back to Redis on job complete and send notification to client
