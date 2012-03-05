Usage
-----

Make sure you have python 2.6 or later and virtualenv installed.
Create a virtualenvironment and make sure it's activated.

$ pip install -r requirements.txt
$ cd source

First we need to create a local_settings.py file in the settings folder, for convience there is a local_settings.example
with some of the default data.

$ cp settings/local_settings.example settings/local_settings.py

Edit the local_settings.py file to point to your database.

Then we need to add all the tables to the database, we use South for migrations which adds the --migrate option

$ python manage.py syncdb --migrate


To run the server:
$ python manage.py runserver 8000

If you want to use the client in development you need to start a second server on a different port because the development server only spawns one thread. So then you use one server to access the client and the other to access the API.

$ python manage.py runserver 8001


You can create an API client in the django admin under /admin/


Warnings
--------

Be carefull with using the DELETE method on the list view of a resource, doing this will remove all items !


Notes
-----

The current implementation uses a simplified authorization system, which can be extended to also include the request_method.
Also we could further change it to it being a combination of the request_method, resource_name and request_type for instance:

project list GET
project list POST
project detail PUT
profile detail DELETE
