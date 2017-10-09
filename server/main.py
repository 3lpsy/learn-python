'''
import modules
It's best practice to write imports in the following order:
1) core modules
2) big modules (like flask)
3) small modules (like flask Extensions)
4) custom modules (like our app file)
'''

# import core packages
import sys
import os
import pathlib

# import custom packages
from app import app, db, User, Post, PROJECT_PATH, DB_PATH
# go to the end of the file and start there.
'''
[10] Assuming you've looked at 1-9, then review the above import.
- The import function always looks for the module locally first. So if it finds an app.py, or a folder (with either a blank or custom __init__.py file) called app, it will import it.
- Notice we use the from modulename import specificthing, otherthing format! This is best practice
- We could import everything in app with "import app", but then we would have remember what the variable and method names are. It's better to be explicit!
- Imports are tricky sometimes. Watch out for circular import! We could not do "import main" in app.py or we would be in an infinite loop. There are ways around this, but the best approach is just to think things out before creating modules. Also, avoid cusomizing the __init__.py (if using folder modules) as you can leave it blank and use the format 'from localfolder.filename import thing'
- Also notice we've only imported things we need here.
- Finally, we've imported app from app. The app in the from portion is the name of the file, the app in the import portion is the name of flask instance. We could rename either the folder or variable but we'll keep this for now.

Now go to app.py and start at [0] there.
'''

''' ---------- The Following Methods are Here to Help With the CLI and Setup ----------- '''

# Helper Methods
# These are our commands we can run.
# This method tells the user running the app what commands they can run
def print_usage():
    print("Please enter a valid command.")
    print('$ python app.py setup # setup database')
    print('$ python app.py serve # serve app')
    print('$ python app.py teardown # destroy database')

'''
The app_setup command does the following:
 - Deletes the current database (teardown)
 - Ensures that our sqlite database_file exists
 - Creates the Database
 - adds some starting data
'''
def app_setup():
    # [1] Run python main.py setup. Make sure you have installed dependencies and are in your virtualenv as the README says.
    # Let's delete the database if it exists. Note that any data will be delete!
    # app_teardown is defined below app_setup. Typically this would mean
    # that it is undefined. Why does python know app_teardown is defined? Think
    # of what scripting is (top to bottom) and wheere the app_setup method is invoked/called.
    # [2] What does app_teardown do?
    app_teardown()
    print('Running Setup')
    # we defined our DB_PATH way up at the top
    # sqlite3 and sqlalchemy need this file to exists
    # [4] We ran app_teardown which deletes DB_PATH? Do we need to check if it exists?
    # Is this redundant (not a trick question)
    if not os.path.exists(DB_PATH):
        print('- Creating Database File', DB_PATH)
        # if it doesn't exist let's create it.
        # instead of using os.path, lets use the included pathlib library
        # it's similar to the os.path library except it's more intuitive
        pathlib.Path(DB_PATH).touch()

    # To talk to the DB from the CLI, we need to get the app context again. This is for CLI,
    # The context is always passed in routes (response/request lifecyle) so you don't need to
    # worry about it there.
    with app.app_context():
        # The 'db' variable will be explained later but know that this method just creates the tables in our database given the models we have defined in app.py
        db.create_all()
        # add some starting data
        print("- Create a anonymous User")
        anonymous = User(name="anonymous", email="anonymous@anonymous.com", password="nothashedohno!", is_deletable=False)

        guest = User(name="guest", email="guest@guest.com", password="nothashedohno!", is_deletable=False)
        print("- Create an admin User")
        admin = User(name="admin", email="admin@admin.com", password="nothashedohno!", is_deletable=False)
        db.session.add(guest)
        db.session.add(anonymous)
        db.session.add(admin)
        print("- Create a default Post")
        post = Post(title="Admin Post", body="Only Admins Are Allowed to Post!", author=admin)
        db.session.add(post)
        db.session.commit()
        # [5] Args are passsed to a class's __init__ function (the function called when classes are invoked, like ClassName(argval, somepropname=somepropval)) to create an instance of that class. For a model class (any class that inherits db.Model), arguments are always passes in the key=value format. The key corresponds to the column/property name. However, author is a relationship, not a column name (the column name is author_id). This is the cornerstone of any good ORM like SqlAlchemy, the ability to handle relationships between tables. They're extremely common. SqlAlchemy knows that when we define an author property we are really defining the author_id with the user.id. Just know that there is a lot of magic happening.
    print("Setup complete. Try serving the app")

'''
This app_serve command serves our app so it will be accessible in browser:
[6] If running this in VM, listen_on should be 0.0.0.0 if you plan on accessing it from your host's browser. When you listen on 0.0.0.0, you are telling the server/machine/VM to allow connections from the internet/outside of the machine (like from your host). If you only listen on 127.0.0.1, it means that the socket, which is bound of port 8000 here, can only be accessed internally (from the same machine). This applies to many different services. Mysql (which uses sql, like sqlite, but listens on a socket as oppsoed to simply being a file), uses this same listening structure where it can listen on localhost(127.0.0.1) or the internet. Have a server on the internet (0.0.0.0) can be a serious security risk.
'''
def app_serve():
    print('Serving Application')
    # check if database file exists, otherwise quit
    if not os.path.exists(DB_PATH):
        print('! Database file does not exists. Did you run setup?')
        sys.exit()
    # [7] Do you plan on running this in Kali and accessing it from your host? You need to change the listen_on variable below to make it accessible to the internet as discussed above. If you're running on your host, like mac, and accessing it from your host, then 127.0.0.1 (aka localhost) is fine.
    listen_on = '127.0.0.1'
    app.run(listen_on, 8000, debug=True)
    # [8] This run method binds our flask process to the port 8000. Try accessing it the browser. It will be on http://127.0.0.1:8000 if accessing it from the same machine. Otherwise, you need you vm IP and will go to http://VMIP:8000.
    # Check out [10] at the top of this file

'''
This app_teardown does the following:
- Drops our database tables through sqlalchemy. Behind the scenes it performs:
    - DROP table users
    - DROP table posts
- Deletes our database file
 '''
def app_teardown():
    print("Tearing Down App")
    # delete sqlite file
    if os.path.exists(DB_PATH):
        print('- Dropping tables')
        # [3] The db instance (defined at top) depends on the app. Look at the db and app instance and then come back. Flask apps have what is called a context. This context will described later. My question is, in the code below, what if the DB_PATH file exists, but there is not sqlite database (it's a blank file). What would happen?
        with app.app_context():
            db.drop_all()
        print('- Deleting Database File', DB_PATH)
        os.remove(DB_PATH)

'''
[0] Start Here!
- This code block is run if the file is called directly like '$ python filename.py'.
- It will always be in the format if __name__ == '__main__'
- The fact that we use __main__ and the filename is main.py does not matter. It is coincidence.
'''
if __name__ == '__main__':
    # check if any command names were added as an argument
    if len(sys.argv) > 1:
        # [1] What is argv? Print it out then exit like below
        # print(sys.argv)
        # sys.exit()
        # This is essence of debugging
        # 1) Find the line you want to look at
        # 2) Get more information about the context (print)
        # 3) Break the process
        # 4) Change the Code
        # 5) Is it fixed? Do you understand?
        # 6) Repeat
        # We're not using argparse here! We could, but let's keep it simple.
        command = sys.argv[1]
        if command == 'setup':
            app_setup()
        elif command == 'serve':
            app_serve()
        elif command == 'teardown':
            app_teardown()
        else:
            # if one of the above command names were not given through the terminal,
            # then tell our user
            print("Invalid Command", command)
            print_usage()
    else:
        print_usage()
