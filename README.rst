==================================
Transcription Factor Target Search
==================================

This site will allow users to search for gene transcription factors and find potential target genes.

Quickstart
----------

The server and all of it's dependencies are installed on our AWS instance, so simply visit it's IP address in your browser.
For login details and the IP address, check your email.
Once you're logged in, cd into /srv/tftarget and you can begin development.


Running the Server Locally
----------------------------------------

If you have the dependencies installed, simply run ``python manage.py runserver``, then visit ``127.0.0.1:8000`` in a browser.

If you don't have the dependencies installed, start by getting Python 2.7.3.
You can `download it for free`_ from python.org.

Now, you'll need to get pip, the Python Package Manager.
For all operating systems, `these instructions`_ will suffice.
On Debian-based Linux distributions, an easier way to get pip is to run ``apt-get install python-setuptools; easy_install pip``.
Special note to Windows users:  you may need to edit your path if the instruction above don't work, see this `Stack Overflow discussion`_.

If you plan on doing any other Python projects, particularly Django ones, you should probably ``pip install virtualenv virtualenvwrapper`` and create a virtual environment for the project.
See the `documentation for virtualenvwrapper`_ if you think you'll do any other large Python projects, otherwise you can skip this step.

Now install the rest of the dependencies by running ``pip install -r requirements.txt``.


MySQL
-----

The quickstart above is sufficient for  getting a server that can run, but eventually you'll need to install MySQL and setup Django to use it.
MySQL can be downloaded from `their website`_ and installed by following the directions.
During install, you should be asked to create a password for the ``root`` user.
Do this, and don't forget the password, you will need it soon and may need it later in an emergency.
On Debian-based Linux distributions, an easier way to get MySQL is to run ``apt-get install mysql-server``.

Once MySQL is installed, you'll need to get the Python library for talking to it.
If you're on a Debian-based Linux distribution, you can install it with ``apt-get install python-mysqldb``.
Other Linux distributions should have a similar package available, but the Python MySQLdb library cannot be installed on Windows without having to edit a few files manually.
Talk to me (Joel Friedly) and I'll try to get you working on Windows.
If you're unsure whether or not your MySQLdb installation worked, open a Python interpreter and run ``import MySQLdb``.

Once the Python library is installed, you'll need to create your ``tftarget`` MySQL user.
To do this, run ``mysql -uroot -p`` and enter the root password that you picked above, then input these SQL commands at the prompt, where $PASSWORD is a new password that you choose::

    mysql> CREATE USER 'tftarget'@'localhost' IDENTIFIED BY '$PASSWORD';
    mysql> CREATE DATABASE tftarget DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
    mysql> GRANT ALL PRIVILEGES ON tftarget.* to 'tftarget'@'localhost' WITH GRANT OPTION;

MySQL should tell you that each query was ok.
Exit the MySQL prompt and now create a file in this directory called ``local_settings.py``.
Put the following lines into the file and save it, making up a secret key to use for hashing::

    import settings

    settings.DATABASES['default']['PASSWORD'] = '$PASSWORD'
    settings.SECRET_KEY = "$SECRET_KEY"

Ensure that Django has access to the MySQL database by opening a Python interpreter with ``python manage.py shell`` and then running these commands::

    >>> from search.models import Experiment
    >>> e = Experiment(species='Human', cell_line='frankencells!')
    >>> e.save()
    >>> e.delete()


Using South
'''''''''''

Databases complain whenever a table schema is changed, and anytime you make a change to a class in a models.py file it represents a change to a table schema.
South makes migrating table schemas easy, without losing your data.
Information on South can be found on `their tutorial`_, and you should already have it installed if the ``pip install -r requirements.txt`` worked.
The first thing you'll need to do is run a ``python manage.py syncdb``, and create a Django admin user by following the prompts.
Then, run this command for each app that we built, replacing $APP_NAME with the name of the app (currently we've only created one app, called ``search``)::

    $ python manage.py migrate $APP_NAME

In order to load the latest SQL dump, run these commands, giving the root user's password at the prompt each time::

    $ mysql -uroot -p tftarget < search_experiment.sql

Currently, we have a simple shell script that will run both of the above commands for you.
You can call it with::

    $ tools/reloaddb.sh

What to do if the ID's are Wrong
''''''''''''''''''''''''''''''''

If you run into errors that rows are attempting to foreign key to other rows that don't exist when you're trying to import the data, read on.
Simply drop the table with ``DROP TABLE $TABLE_NAME`` and then try to import the data again using ``mysql -uroot -p tftarget < $TABLE_NAME.sql``.
Depending on which table it was, you may need to drop some other tables first because of foreign key constraints.
The many-to-many lookup tables can always be dropped, and once those are gone, any of the others can be dropped.
The tables can be restored in any order (I think).
If this doesn't work, don't worry, we're just using fake data for now.
Do NOT do this on a production database.

How to Export the Database to a SQLdump
'''''''''''''''''''''''''''''''''''''''
::

    $ mysqldump -uroot -p tftarget search_experiment > sqldumps/search_experiment.sql


About Python
------------

The best introduction to Python that I know of is the `Python Tutorial`_ at python.org.
Other highly recommended tutorials include `Dive into Python`_ and `Learn Python the Hard Way`_.


About Django
------------

The `Django Tutorial`_ is an excellent four-part starter series on Django.
It will assume that you know at least a little Python though.


.. _download it for free: http://python.org/download/releases/2.7.3/
.. _these instructions: http://pypi.python.org/pypi/setuptools
.. _Stack Overflow discussion: http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows
.. _documentation for virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
.. _their website: http://www.mysql.com/downloads/mysql/
.. _their tutorial: http://south.readthedocs.org/en/latest/tutorial/part1.html
.. _Python Tutorial: http://docs.python.org/2/tutorial/
.. _Dive into Python: http://www.diveintopython.net/
.. _Learn Python the Hard Way: http://learnpythonthehardway.org/
.. _Django Tutorial: https://docs.djangoproject.com/en/dev/intro/tutorial01/
