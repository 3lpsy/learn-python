# Setup

## Make sure virutalenv is installed

    $ virutalenv --version

### Install if not found

    $ pip3 install virtualenv


## Create Virtualenv

### Findout where python3 is

    $ which python3

If there is no output, install python3.

Take the output (the path to python3 and use it as the -p value). This makes your virtualenv use python3.

    $ cd /path/to/this/folder

    $ virtualenv venv -p /path/to/python3

Active virtualenv

    $ source venv/bin/activate

Verify python is python3

    $ python --version

Install dependencies. This command will read the list in requirements.txt

    $ (venv) pip install -r requirements.txt

# Running The App

If you look at the end of the main.py where we check if the file is being called directly (comparing '\__main__' to '\__name__'), you can see if the an argument has been passed to command. The syntax is:

    $ python main.py commandname

We have written a few commands that should be run in this order.


## View Available Commands

    $ python main.py

## Install Database

    $ python main.py setup

## Serve Database

    $ python main.py server

## If you want, we can rollback the database

    $ python main.py teardown

Comments have been written to guide you in parsing out what the code does. You can start in main.py with the comment labeled "[0]".
