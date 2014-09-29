trex
====

trex - time recording enhanced


Installation
------------

Install requirements::

    $ pip install -r requirements.txt

Configure settings, e.g.::

    $ cp trex/settings_development.py trex/settings.py
    $ $EDITOR trex/settings.py # update your settings

Create a secrets file::

    $ touch secret.key
    $ $EDITOR secret.key # insert secret to file

Create the database::

    $ python manage.py migrate

Run the server::

    $ python manage.py runserver $IP_ADDRESS:$PORT

Open your browser on $IP_ADDRESS:$PORT.


License
-------

MIT License
